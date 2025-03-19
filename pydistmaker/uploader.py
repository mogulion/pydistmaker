"""Artifactory上传模块"""

import os
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, List

import requests
from requests.auth import HTTPBasicAuth


class ArtifactoryUploader:
    """Artifactory上传器"""
    
    def __init__(self, config: Dict[str, Any], project_name: str, version: str, output_dir: str):
        """初始化上传器
        
        Args:
            config: Artifactory配置
            project_name: 项目名称
            version: 项目版本
            output_dir: 输出目录
        """
        self.config = config
        self.project_name = project_name
        self.version = version
        self.output_dir = output_dir
        
        # 验证配置
        self._validate_config()
    
    def _validate_config(self) -> None:
        """验证Artifactory配置
        
        Raises:
            ValueError: 配置无效
        """
        required_fields = ["url", "repository", "username", "password"]
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Artifactory配置缺少必要字段: {field}")
        
        # 确保URL不以斜杠结尾
        if self.config["url"].endswith("/"):
            self.config["url"] = self.config["url"][:-1]
    
    def upload(self) -> Dict[str, Any]:
        """上传编译产物到Artifactory
        
        Returns:
            上传结果信息
        
        Raises:
            Exception: 上传失败
        """
        print(f"开始上传编译产物到Artifactory: {self.config['url']}")
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 打包输出目录
            zip_path = self._create_package(temp_dir)
            
            # 上传到Artifactory
            result = self._upload_to_artifactory(zip_path)
            
            print(f"上传成功: {result['uri']}")
            return result
    
    def _create_package(self, temp_dir: str) -> str:
        """创建打包文件
        
        Args:
            temp_dir: 临时目录
            
        Returns:
            打包文件路径
        """
        print("打包编译产物...")
        
        # 创建ZIP文件
        zip_filename = f"{self.project_name}-{self.version}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加输出目录中的所有文件
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.output_dir)
                    zipf.write(file_path, arcname)
        
        print(f"打包完成: {zip_path}")
        return zip_path
    
    def _upload_to_artifactory(self, zip_path: str) -> Dict[str, Any]:
        """上传到Artifactory
        
        Args:
            zip_path: 打包文件路径
            
        Returns:
            上传结果信息
            
        Raises:
            Exception: 上传失败
        """
        # 构建上传URL
        filename = os.path.basename(zip_path)
        artifact_path = f"{self.project_name}/{self.version}/{filename}"
        
        # 如果配置了路径前缀，则添加
        if "path_prefix" in self.config and self.config["path_prefix"]:
            path_prefix = self.config["path_prefix"]
            # 确保路径前缀不以斜杠开头或结尾
            if path_prefix.startswith("/"):
                path_prefix = path_prefix[1:]
            if path_prefix.endswith("/"):
                path_prefix = path_prefix[:-1]
            artifact_path = f"{path_prefix}/{artifact_path}"
        
        upload_url = f"{self.config['url']}/artifactory/{self.config['repository']}/{artifact_path}"
        
        # 准备认证信息
        auth = HTTPBasicAuth(self.config["username"], self.config["password"])
        
        # 准备请求头
        headers = {
            "X-Checksum-Deploy": "true"
        }
        
        # 添加自定义属性
        if "properties" in self.config and self.config["properties"]:
            props = [f"{k}={v}" for k, v in self.config["properties"].items()]
            headers["X-JFrog-Art-Api"] = ";".join(props)
        
        # 上传文件
        print(f"上传文件到: {upload_url}")
        with open(zip_path, "rb") as f:
            response = requests.put(
                upload_url,
                auth=auth,
                headers=headers,
                data=f
            )
        
        # 检查响应
        if response.status_code not in [200, 201]:
            raise Exception(f"上传失败: {response.status_code} - {response.text}")
        
        # 解析响应
        result = response.json()
        result["url"] = upload_url
        
        return result


def upload_to_artifactory(config_path: str) -> None:
    """上传编译产物到Artifactory
    
    Args:
        config_path: 配置文件路径
    
    Raises:
        Exception: 上传失败
    """
    from pydistmaker.config import load_config
    
    try:
        # 加载配置
        config = load_config(config_path)
        
        # 检查是否配置了Artifactory
        if not hasattr(config, "artifactory") or not config.artifactory:
            raise ValueError("未配置Artifactory信息，请先在配置文件中添加artifactory部分")
        
        # 检查输出目录是否存在
        output_dir = os.path.join(os.getcwd(), config.project.output_dir)
        if not os.path.exists(output_dir):
            raise ValueError(f"输出目录不存在: {output_dir}，请先执行打包命令")
        
        # 创建上传器并执行上传
        uploader = ArtifactoryUploader(
            config.artifactory.model_dump(),
            config.project.name,
            config.project.version,
            output_dir
        )
        uploader.upload()
        
        print("上传完成")
        
    except Exception as e:
        print(f"上传失败: {e}")
        raise
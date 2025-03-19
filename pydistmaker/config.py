"""配置文件处理模块"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

import jsonschema
from pydantic import BaseModel, Field, field_validator

from pydistmaker.schema import generate_schema


class ProjectConfig(BaseModel):
    """项目配置"""
    name: str = Field(..., description="项目名称")
    version: str = Field(..., description="版本号（SemVer格式）")
    entries: List[str] = Field(..., description="入口脚本路径列表")
    output_dir: str = Field("dist", description="输出目录路径")

    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """验证版本号格式"""
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError("版本号必须符合SemVer格式 (例如: 1.0.0)")
        return v

    @field_validator('entries')
    @classmethod
    def validate_entries(cls, v: List[str]) -> List[str]:
        """验证入口脚本路径"""
        if not v:
            raise ValueError("至少需要一个入口脚本")
        return v


class NuitkaConfig(BaseModel):
    """Nuitka配置"""
    modules: Optional[List[str]] = Field(None, description="需要编译的核心模块")
    lto: bool = Field(True, description="启用链接时优化")
    jobs: int = Field(4, description="并行编译线程数", ge=1)
    standalone: bool = Field(True, description="生成独立可执行文件")
    plugins: Optional[List[str]] = Field(None, description="启用的插件列表")
    include_packages: Optional[List[str]] = Field(None, description="包含的包列表")
    extra_args: Optional[List[str]] = Field(None, description="额外的Nuitka命令行参数")


class PyInstallerConfig(BaseModel):
    """PyInstaller配置"""
    mode: str = Field("onedir", description="打包模式")
    bin_dir: str = Field("bin", description="依赖二进制文件存放目录")
    hidden_imports: Optional[List[str]] = Field(None, description="显式指定隐藏导入模块")
    add_data: Optional[List[str]] = Field(None, description="添加额外资源文件")
    runtime_tmpdir: Optional[str] = Field(None, description="设置运行时临时目录")
    icon: Optional[str] = Field(None, description="设置可执行文件图标")
    extra_args: Optional[List[str]] = Field(None, description="额外的PyInstaller命令行参数")

    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v: str) -> str:
        """验证打包模式"""
        if v not in ["onedir", "onefile"]:
            raise ValueError("打包模式必须是 'onedir' 或 'onefile'")
        return v


class DistMakerConfig(BaseModel):
    """PyDistMaker配置"""
    project: ProjectConfig
    nuitka: Optional[NuitkaConfig] = Field(default_factory=NuitkaConfig)
    pyinstaller: Optional[PyInstallerConfig] = Field(default_factory=PyInstallerConfig)


def load_config(config_path: str) -> DistMakerConfig:
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        解析后的配置对象
        
    Raises:
        FileNotFoundError: 配置文件不存在
        jsonschema.exceptions.ValidationError: 配置文件格式错误
        json.JSONDecodeError: 配置文件不是有效的JSON
    """
    config_path = os.path.abspath(config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    # 验证配置文件格式
    schema = generate_schema()
    jsonschema.validate(config_data, schema)
    
    # 转换为Pydantic模型
    return DistMakerConfig.model_validate(config_data)


def generate_default_config() -> Dict[str, Any]:
    """生成默认配置
    
    Returns:
        默认配置字典
    """
    return {
        "$schema": "py-packager-schema.json",
        "project": {
            "name": "myapp",
            "version": "1.0.0",
            "entries": ["src/main.py"],
            "output_dir": "dist"
        },
        "nuitka": {
            "modules": ["core/*.py"],
            "lto": True,
            "jobs": 4,
            "standalone": True,
            "plugins": [],
            "include_packages": []
        },
        "pyinstaller": {
            "mode": "onedir",
            "bin_dir": "bin",
            "hidden_imports": [],
            "add_data": []
        }
    }


def save_config(config: Dict[str, Any], output_path: str) -> None:
    """保存配置到文件
    
    Args:
        config: 配置字典
        output_path: 输出文件路径
    """
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"配置文件已保存到: {output_path}")


def save_schema(output_path: str) -> None:
    """保存JSON Schema到文件
    
    Args:
        output_path: 输出文件路径
    """
    schema = generate_schema()
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    
    print(f"Schema文件已保存到: {output_path}")
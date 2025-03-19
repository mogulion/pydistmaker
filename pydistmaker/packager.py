"""核心打包逻辑模块"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from pydistmaker.config import DistMakerConfig


class DistMaker:
    """打包器核心类"""
    
    def __init__(self, config: DistMakerConfig):
        """初始化打包器
        
        Args:
            config: 打包配置
        """
        self.config = config
        self.project_dir = os.getcwd()
        self.output_dir = os.path.join(self.project_dir, config.project.output_dir)
        self.temp_dir = os.path.join(self.output_dir, "_temp")
        self.nuitka_output_dir = os.path.join(self.temp_dir, "nuitka_output")
        self.pyinstaller_output_dir = os.path.join(self.temp_dir, "pyinstaller_output")
        
    def build(self) -> None:
        """执行打包流程"""
        print(f"开始打包项目: {self.config.project.name} v{self.config.project.version}")
        
        # 准备输出目录
        self._prepare_directories()
        
        # 编译核心模块
        if self.config.nuitka and self.config.nuitka.modules:
            self._compile_core_modules()
        
        # 打包入口脚本
        self._package_entries()
        
        # 整理输出目录
        self._organize_output()
        
        # 清理临时文件
        self._cleanup()
        
        print(f"打包完成，输出目录: {self.output_dir}")
    
    def _prepare_directories(self) -> None:
        """准备输出目录"""
        # 创建临时目录
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.nuitka_output_dir, exist_ok=True)
        os.makedirs(self.pyinstaller_output_dir, exist_ok=True)
        
        # 清空输出目录（保留临时目录）
        for item in os.listdir(self.output_dir):
            item_path = os.path.join(self.output_dir, item)
            if item != "_temp" and os.path.exists(item_path):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
    
    def _compile_core_modules(self) -> None:
        """使用Nuitka编译核心模块"""
        print("使用Nuitka编译核心模块...")
        
        for module_pattern in self.config.nuitka.modules:
            # 解析模块路径模式
            import glob
            module_paths = glob.glob(module_pattern, recursive=True)
            
            for module_path in module_paths:
                if not os.path.exists(module_path):
                    print(f"警告: 模块路径不存在: {module_path}")
                    continue
                
                print(f"编译模块: {module_path}")
                self._run_nuitka(module_path)
    
    def _run_nuitka(self, module_path: str) -> None:
        """运行Nuitka编译指定模块
        
        Args:
            module_path: 模块路径
        """
        cmd = [sys.executable, "-m", "nuitka"]
        
        # 添加Nuitka配置参数
        if self.config.nuitka.lto:
            cmd.append("--lto=yes")
        
        cmd.append(f"--jobs={self.config.nuitka.jobs}")
        
        if self.config.nuitka.standalone:
            cmd.append("--standalone")
        
        # 添加插件
        if self.config.nuitka.plugins:
            for plugin in self.config.nuitka.plugins:
                cmd.append(f"--plugin-enable={plugin}")
        
        # 添加包含的包
        if self.config.nuitka.include_packages:
            for package in self.config.nuitka.include_packages:
                cmd.append(f"--include-package={package}")
        
        # 添加额外参数
        if self.config.nuitka.extra_args:
            cmd.extend(self.config.nuitka.extra_args)
        
        # 设置输出目录
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        output_dir = os.path.join(self.nuitka_output_dir, module_name)
        cmd.append(f"--output-dir={output_dir}")
        
        # 添加模块路径
        cmd.append(module_path)
        
        # 执行命令
        try:
            subprocess.run(cmd, check=True)
            print(f"模块 {module_path} 编译成功")
        except subprocess.CalledProcessError as e:
            print(f"模块 {module_path} 编译失败: {e}")
            raise
    
    def _package_entries(self) -> None:
        """使用PyInstaller打包入口脚本"""
        print("使用PyInstaller打包入口脚本...")
        
        for entry in self.config.project.entries:
            if not os.path.exists(entry):
                print(f"警告: 入口脚本不存在: {entry}")
                continue
            
            print(f"打包入口脚本: {entry}")
            self._run_pyinstaller(entry)
    
    def _run_pyinstaller(self, entry_path: str) -> None:
        """运行PyInstaller打包指定入口脚本
        
        Args:
            entry_path: 入口脚本路径
        """
        cmd = [sys.executable, "-m", "PyInstaller"]
        
        # 设置打包模式
        if self.config.pyinstaller.mode == "onedir":
            cmd.append("--onedir")
        else:
            cmd.append("--onefile")
        
        # 设置名称
        entry_name = os.path.splitext(os.path.basename(entry_path))[0]
        cmd.append(f"--name={entry_name}")
        
        # 设置输出目录
        entry_output_dir = os.path.join(self.pyinstaller_output_dir, entry_name)
        cmd.append(f"--distpath={entry_output_dir}")
        cmd.append(f"--workpath={os.path.join(self.temp_dir, 'pyinstaller_work')}")
        cmd.append("--noconfirm")
        
        # 添加隐藏导入
        if self.config.pyinstaller.hidden_imports:
            for hidden_import in self.config.pyinstaller.hidden_imports:
                cmd.append(f"--hidden-import={hidden_import}")
        
        # 添加额外资源文件
        if self.config.pyinstaller.add_data:
            for data in self.config.pyinstaller.add_data:
                cmd.append(f"--add-data={data}")
        
        # 设置运行时临时目录
        if self.config.pyinstaller.runtime_tmpdir:
            cmd.append(f"--runtime-tmpdir={self.config.pyinstaller.runtime_tmpdir}")
        
        # 设置图标
        if self.config.pyinstaller.icon and os.path.exists(self.config.pyinstaller.icon):
            cmd.append(f"--icon={self.config.pyinstaller.icon}")
        
        # 添加额外参数
        if self.config.pyinstaller.extra_args:
            cmd.extend(self.config.pyinstaller.extra_args)
        
        # 添加入口脚本路径
        cmd.append(entry_path)
        
        # 执行命令
        try:
            subprocess.run(cmd, check=True)
            print(f"入口脚本 {entry_path} 打包成功")
        except subprocess.CalledProcessError as e:
            print(f"入口脚本 {entry_path} 打包失败: {e}")
            raise
    
    def _organize_output(self) -> None:
        """整理输出目录结构"""
        print("整理输出目录结构...")
        
        # 创建bin目录
        bin_dir = os.path.join(self.output_dir, self.config.pyinstaller.bin_dir)
        os.makedirs(bin_dir, exist_ok=True)
        
        # 处理每个入口脚本的输出
        for entry in self.config.project.entries:
            entry_name = os.path.splitext(os.path.basename(entry))[0]
            entry_output_dir = os.path.join(self.pyinstaller_output_dir, entry_name, entry_name)
            
            if not os.path.exists(entry_output_dir):
                print(f"警告: 入口脚本输出目录不存在: {entry_output_dir}")
                continue
            
            # 复制可执行文件到输出根目录
            exe_name = f"{entry_name}.exe" if sys.platform == "win32" else entry_name
            exe_path = os.path.join(entry_output_dir, exe_name)
            if os.path.exists(exe_path):
                shutil.copy2(exe_path, self.output_dir)
            
            # 复制依赖文件到bin目录
            for item in os.listdir(entry_output_dir):
                item_path = os.path.join(entry_output_dir, item)
                if item != exe_name:  # 排除可执行文件
                    if os.path.isdir(item_path):
                        shutil.copytree(item_path, os.path.join(bin_dir, item), dirs_exist_ok=True)
                    else:
                        shutil.copy2(item_path, bin_dir)
        
        # 生成MANIFEST文件
        self._generate_manifest()
    
    def _generate_manifest(self) -> None:
        """生成MANIFEST文件"""
        manifest_path = os.path.join(self.output_dir, "MANIFEST.json")
        
        manifest = {
            "name": self.config.project.name,
            "version": self.config.project.version,
            "entries": [os.path.basename(entry) for entry in self.config.project.entries],
            "bin_dir": self.config.pyinstaller.bin_dir,
            "packager": "PyDistMaker",
            "packager_version": "0.1.0"
        }
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            import json
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"MANIFEST文件已生成: {manifest_path}")
    
    def _cleanup(self) -> None:
        """清理临时文件"""
        print("清理临时文件...")
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def build(config_path: str) -> None:
    """执行打包流程
    
    Args:
        config_path: 配置文件路径
    """
    from pydistmaker.config import load_config
    
    try:
        # 加载配置
        config = load_config(config_path)
        
        # 创建打包器并执行打包
        packager = DistMaker(config)
        packager.build()
        
    except Exception as e:
        print(f"打包失败: {e}")
        raise
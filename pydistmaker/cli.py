"""命令行接口模块"""

import os
import sys
from typing import Optional

import click

from pydistmaker.config import (
    generate_default_config,
    save_config,
    save_schema,
    load_config
)
from pydistmaker.packager import build as run_build
from pydistmaker.uploader import upload_to_artifactory as run_upload


@click.group()
@click.version_option()
def cli():
    """PyDistMaker - Python应用打包工具
    
    结合Nuitka和PyInstaller优势的Python打包工具，
    支持多入口脚本打包、onedir模式和灵活的配置选项。
    """
    pass


@cli.command()
@click.option('--output', '-o', default='pydistmaker.json', help='输出配置文件路径')
@click.option('--schema', '-s', is_flag=True, help='同时生成JSON Schema文件')
def init(output: str, schema: bool):
    """初始化配置文件"""
    config = generate_default_config()
    save_config(config, output)
    
    if schema:
        schema_path = os.path.join(os.path.dirname(output), 'py-packager-schema.json')
        save_schema(schema_path)


@cli.command()
@click.option('--config', '-c', default='pydistmaker.json', help='配置文件路径')
@click.option('--mode', '-m', type=click.Choice(['nuitka_only', 'pyinstaller_only', 'mixed']), 
              help='编译模式: nuitka_only(仅Nuitka), pyinstaller_only(仅PyInstaller), mixed(混合模式)')
def build(config: str, mode: str):
    """执行打包流程"""
    try:
        run_build(config, mode)
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', default='pydistmaker.json', help='配置文件路径')
@click.option('--strict', '-s', is_flag=True, help='严格模式（检查文件路径是否存在）')
def verify(config: str, strict: bool):
    """验证配置文件有效性"""
    try:
        # 加载配置文件
        config_obj = load_config(config)
        
        # 严格模式下检查文件路径
        if strict:
            # 检查入口脚本
            for entry in config_obj.project.entries:
                if not os.path.exists(entry):
                    click.echo(f"警告: 入口脚本不存在: {entry}", err=True)
            
            # 检查Nuitka模块
            if config_obj.nuitka and config_obj.nuitka.modules:
                for module_pattern in config_obj.nuitka.modules:
                    import glob
                    module_paths = glob.glob(module_pattern, recursive=True)
                    if not module_paths:
                        click.echo(f"警告: 未找到匹配的模块: {module_pattern}", err=True)
            
            # 检查图标文件
            if config_obj.pyinstaller and config_obj.pyinstaller.icon:
                if not os.path.exists(config_obj.pyinstaller.icon):
                    click.echo(f"警告: 图标文件不存在: {config_obj.pyinstaller.icon}", err=True)
        
        click.echo(f"配置文件 {config} 验证通过")
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', default='pydistmaker.json', help='配置文件路径')
@click.option('--build', '-b', is_flag=True, help='先执行打包再上传')
@click.option('--mode', '-m', type=click.Choice(['nuitka_only', 'pyinstaller_only', 'mixed']), 
              help='编译模式: nuitka_only(仅Nuitka), pyinstaller_only(仅PyInstaller), mixed(混合模式)')
def upload(config: str, build: bool, mode: str):
    """上传编译产物到Artifactory"""
    try:
        # 如果指定了先打包，则先执行打包流程
        if build:
            run_build(config, mode)
        
        # 执行上传
        run_upload(config)
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


def main():
    """主入口函数"""
    cli()


if __name__ == "__main__":
    main()
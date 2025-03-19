"""JSON Schema 生成模块"""

from typing import Dict, Any


def generate_schema() -> Dict[str, Any]:
    """生成 PyDistMaker 配置文件的 JSON Schema
    
    Returns:
        JSON Schema 字典
    """
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "PyDistMaker Configuration",
        "description": "PyDistMaker 配置文件格式",
        "type": "object",
        "required": ["project"],
        "properties": {
            "$schema": {
                "type": "string",
                "description": "JSON Schema 文件路径"
            },
            "project": {
                "type": "object",
                "required": ["name", "version", "entries"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "项目名称"
                    },
                    "version": {
                        "type": "string",
                        "description": "版本号（SemVer格式）",
                        "pattern": "^\\d+\\.\\d+\\.\\d+$"
                    },
                    "entries": {
                        "type": "array",
                        "description": "入口脚本路径列表",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 1
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "输出目录路径",
                        "default": "dist"
                    }
                }
            },
            "nuitka": {
                "type": "object",
                "properties": {
                    "modules": {
                        "type": "array",
                        "description": "需要编译的核心模块",
                        "items": {
                            "type": "string"
                        }
                    },
                    "lto": {
                        "type": "boolean",
                        "description": "启用链接时优化",
                        "default": True
                    },
                    "jobs": {
                        "type": "integer",
                        "description": "并行编译线程数",
                        "minimum": 1,
                        "default": 4
                    },
                    "standalone": {
                        "type": "boolean",
                        "description": "生成独立可执行文件",
                        "default": True
                    },
                    "plugins": {
                        "type": "array",
                        "description": "启用的插件列表",
                        "items": {
                            "type": "string"
                        }
                    },
                    "include_packages": {
                        "type": "array",
                        "description": "包含的包列表",
                        "items": {
                            "type": "string"
                        }
                    },
                    "extra_args": {
                        "type": "array",
                        "description": "额外的 Nuitka 命令行参数",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            },
            "pyinstaller": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "description": "打包模式",
                        "enum": ["onedir", "onefile"],
                        "default": "onedir"
                    },
                    "bin_dir": {
                        "type": "string",
                        "description": "依赖二进制文件存放目录",
                        "default": "bin"
                    },
                    "hidden_imports": {
                        "type": "array",
                        "description": "显式指定隐藏导入模块",
                        "items": {
                            "type": "string"
                        }
                    },
                    "add_data": {
                        "type": "array",
                        "description": "添加额外资源文件",
                        "items": {
                            "type": "string"
                        }
                    },
                    "runtime_tmpdir": {
                        "type": "string",
                        "description": "设置运行时临时目录"
                    },
                    "icon": {
                        "type": "string",
                        "description": "设置可执行文件图标"
                    },
                    "extra_args": {
                        "type": "array",
                        "description": "额外的 PyInstaller 命令行参数",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
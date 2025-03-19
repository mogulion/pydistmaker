# PyDistMaker - Python应用打包工具

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

PyDistMaker是一个结合Nuitka和PyInstaller优势的Python打包工具，支持多入口脚本打包、onedir模式和灵活的配置选项。

## 特性

- **混合编译打包**：结合Nuitka和PyInstaller的优势，提供更高效的打包方案
- **多入口脚本支持**：一次配置，同时打包多个可执行文件
- **onedir模式**：生成结构清晰的目录式应用
- **灵活配置**：提供丰富的配置选项，满足各种打包需求
- **跨平台支持**：支持Windows、macOS和Linux平台

## 安装

使用pip安装PyDistMaker：

```bash
pip install pydistmaker
```

## 快速开始

### 1. 初始化配置文件

```bash
pydistmaker init --output=pydistmaker.json
```

可选参数：
- `--output, -o`：指定配置文件输出路径，默认为`pydistmaker.json`
- `--schema, -s`：同时生成JSON Schema文件

### 2. 修改配置文件

根据项目需求调整配置文件：

```json
{
  "$schema": "pydistmaker-schema.json",
  "project": {
    "name": "myapp",
    "version": "1.0.0",
    "entries": ["src/main.py", "src/cli.py"],
    "output_dir": "dist"
  },
  "nuitka": {
    "modules": ["core/*.py"],
    "lto": true,
    "jobs": 4,
    "standalone": true,
    "plugins": ["tk-inter", "numpy"],
    "include_packages": []
  },
  "pyinstaller": {
    "mode": "onedir",
    "bin_dir": "bin",
    "hidden_imports": ["encodings"],
    "add_data": ["assets/*:assets"]
  }
}
```

### 3. 执行打包

```bash
pydistmaker build --config=pydistmaker.json
```

可选参数：
- `--config, -c`：指定配置文件路径，默认为`pydistmaker.json`

### 4. 验证配置文件

```bash
pydistmaker verify --config=pydistmaker.json --strict
```

可选参数：
- `--config, -c`：指定配置文件路径，默认为`pydistmaker.json`
- `--strict, -s`：启用严格模式，检查文件路径是否存在

## 配置文件说明

### 项目配置 (project)

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `name` | 字符串 | 项目名称 | - |
| `version` | 字符串 | 版本号（SemVer格式） | - |
| `entries` | 字符串数组 | 入口脚本路径列表 | - |
| `output_dir` | 字符串 | 输出目录路径 | `dist` |

### Nuitka配置 (nuitka)

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `modules` | 字符串数组 | 需要编译的核心模块 | `[]` |
| `lto` | 布尔值 | 启用链接时优化 | `true` |
| `jobs` | 整数 | 并行编译线程数 | `4` |
| `standalone` | 布尔值 | 生成独立可执行文件 | `true` |
| `plugins` | 字符串数组 | 启用的插件列表 | `[]` |
| `include_packages` | 字符串数组 | 包含的包列表 | `[]` |
| `extra_args` | 字符串数组 | 额外的Nuitka命令行参数 | `null` |

### PyInstaller配置 (pyinstaller)

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `mode` | 字符串 | 打包模式（`onedir`或`onefile`） | `onedir` |
| `bin_dir` | 字符串 | 依赖二进制文件存放目录 | `bin` |
| `hidden_imports` | 字符串数组 | 隐藏导入模块列表 | `[]` |
| `add_data` | 字符串数组 | 额外资源文件列表 | `[]` |
| `icon` | 字符串 | 可执行文件图标路径 | `null` |
| `runtime_tmpdir` | 字符串 | 运行时临时目录 | `null` |

## 输出目录结构

使用`onedir`模式打包后，输出目录结构如下：

```
dist/
├── main.exe
├── cli.exe
└── bin/
    ├── lib1.dll
    ├── lib2.so
    └── ...
```

## 混合编译打包流程

1. 入口文件分析
2. Nuitka编译核心模块，生成.pyd/.so文件
3. 依赖分析，生成依赖图谱
4. PyInstaller打包，生成可执行文件
5. 安全加固处理
6. 整理输出目录
7. 生成MANIFEST文件

## 跨平台支持

- **路径处理**：统一使用POSIX格式路径，在Windows上自动转换为反斜杠
- **平台专属参数**：
  - Windows：支持Signtool签名
  - macOS：支持codesign签名
  - Linux：支持GPG签名

## 命令行参考

| 命令 | 功能 | 参数示例 |
|------|------|----------|
| `pydistmaker build` | 执行打包流程 | `--config=config.json` |
| `pydistmaker init` | 生成配置模板 | `--output=custom_config.json` |
| `pydistmaker verify` | 验证配置文件有效性 | `--strict` |

## 许可证

[MIT License](LICENSE) © mogulion
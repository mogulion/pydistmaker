# PyDistMaker - 混合模式示例

本示例展示如何使用PyDistMaker的混合模式进行打包，结合Nuitka和PyInstaller的优势。

## 配置文件说明

`pydistmaker.json`文件配置了使用混合模式进行打包的设置：

```json
{
  "$schema": "pydistmaker-schema.json",
  "build_mode": "mixed",
  "project": {
    "name": "myapp",
    "version": "1.0.0",
    "entries": ["src/main.py", "src/cli.py"],
    "output_dir": "dist"
  },
  "nuitka": {
    "modules": ["src/core/*.py", "src/utils/*.py"],
    "lto": true,
    "jobs": 4,
    "standalone": true,
    "plugins": ["numpy", "pandas"],
    "include_packages": ["numpy", "pandas"]
  },
  "pyinstaller": {
    "mode": "onedir",
    "bin_dir": "bin",
    "hidden_imports": ["encodings", "numpy", "pandas"],
    "add_data": ["assets/*:assets"],
    "icon": "assets/icon.ico"
  },
  "artifactory": {
    "url": "https://artifactory.iav.com",
    "repository": "tools-iav-cn",
    "username": "${ARTIFACTORY_USERNAME}",
    "password": "${ARTIFACTORY_PASSWORD}",
    "path_prefix": "python-apps",
    "properties": {
      "app.type": "python",
      "app.name": "myapp",
      "build.type": "mixed-mode"
    }
  }
}
```

## 关键配置项

- `build_mode`: 设置为`mixed`，表示使用混合模式打包
- `nuitka.modules`: 指定需要使用Nuitka编译的核心模块
- `pyinstaller.mode`: 设置为`onedir`，生成目录式应用
- `pyinstaller.hidden_imports`: 指定需要显式导入的模块

## 混合模式工作流程

1. 使用Nuitka编译核心模块（`src/core/*.py`和`src/utils/*.py`）
2. 使用PyInstaller打包入口脚本（`src/main.py`和`src/cli.py`）
3. 整合编译产物，生成最终的可执行文件和依赖库

## 使用方法

### 1. 执行打包

```bash
pydistmaker build --config=pydistmaker.json
```

### 2. 上传到Artifactory

```bash
pydistmaker upload --config=pydistmaker.json --build
```

## 输出目录结构

使用混合模式打包后，输出目录结构如下：

```
dist/
├── main.exe
├── cli.exe
└── bin/
    ├── core/
    │   └── processor.pyd
    ├── utils/
    │   └── helper.pyd
    ├── lib1.dll
    ├── lib2.so
    └── ...
```
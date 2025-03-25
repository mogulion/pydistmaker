# PyDistMaker - PyInstaller模式示例

本示例展示如何使用PyDistMaker的PyInstaller模式进行打包。

## 配置文件说明

`pydistmaker.json`文件配置了仅使用PyInstaller进行打包的设置：

```json
{
  "$schema": "pydistmaker-schema.json",
  "build_mode": "pyinstaller_only",
  "project": {
    "name": "myapp",
    "version": "1.0.0",
    "entries": ["src/main.py", "src/cli.py"],
    "output_dir": "dist"
  },
  "pyinstaller": {
    "mode": "onedir",
    "bin_dir": "bin",
    "hidden_imports": ["encodings", "pandas", "numpy"],
    "add_data": ["assets/*:assets", "config/*.json:config"],
    "icon": "assets/icon.ico",
    "runtime_tmpdir": "./tmp",
    "extra_args": ["--clean", "--log-level=INFO"]
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
      "build.type": "pyinstaller-only"
    }
  }
}
```

## 关键配置项

- `build_mode`: 设置为`pyinstaller_only`，表示仅使用PyInstaller打包
- `project.entries`: 指定入口脚本路径，支持多个入口
- `pyinstaller.mode`: 设置为`onedir`，生成目录式应用
- `pyinstaller.hidden_imports`: 指定需要显式导入的模块
- `pyinstaller.add_data`: 添加额外资源文件

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
# PyDistMaker - Nuitka模式示例

本示例展示如何使用PyDistMaker的Nuitka模式进行打包。

## 配置文件说明

`pydistmaker.json`文件配置了仅使用Nuitka进行打包的设置：

```json
{
  "$schema": "pydistmaker-schema.json",
  "build_mode": "nuitka_only",
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
    "plugins": ["numpy", "pandas", "tk-inter"],
    "include_packages": ["numpy", "pandas"],
    "extra_args": ["--follow-imports", "--enable-plugin=anti-bloat"]
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
      "build.type": "nuitka-only"
    }
  }
}
```

## 关键配置项

- `build_mode`: 设置为`nuitka_only`，表示仅使用Nuitka打包
- `project.entries`: 指定入口脚本路径，支持多个入口
- `nuitka.modules`: 指定需要编译的核心模块，支持通配符
- `nuitka.plugins`: 启用的Nuitka插件列表
- `nuitka.include_packages`: 需要包含的Python包

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

使用Nuitka打包后，输出目录结构如下：

```
dist/
├── main.exe
├── cli.exe
└── lib/
    ├── numpy.pyd
    ├── pandas.pyd
    └── ...
```
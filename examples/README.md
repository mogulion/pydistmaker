# PyDistMaker 示例应用

这是一个用于演示 PyDistMaker 打包工具的示例应用程序。

## 项目结构

```
.
├── assets/          # 资源文件
│   └── icon.svg     # 应用图标
├── config/          # 配置文件
│   └── settings.json # 应用配置
├── core/            # 核心处理模块
│   ├── __init__.py
│   └── processor.py # 文件处理器
├── data/            # 示例数据
│   ├── sample.json  # JSON示例
│   └── sample.txt   # 文本示例
├── utils/           # 工具模块
│   ├── __init__.py
│   └── helpers.py   # 辅助函数
├── cli.py           # 命令行接口
├── main.py          # 主程序入口
└── README.md        # 本文件
```

## 使用方法

### 命令行方式

```bash
# 处理文本文件
python cli.py process -i data/sample.txt -o output/result.txt

# 处理JSON文件
python cli.py process -i data/sample.json -o output/result.json --json
```

### 主程序方式

```bash
# 处理文本文件
python main.py -i data/sample.txt -o output/result.txt

# 处理JSON文件
python main.py -i data/sample.json -o output/result.json --json
```

## 打包说明

此示例项目可以使用 PyDistMaker 以三种不同的模式进行打包：

1. PyInstaller 模式
2. Nuitka 模式
3. 混合模式

请参考项目根目录下的各个示例配置文件：

- `examples/pyinstaller_only/pydistmaker.json`
- `examples/nuitka_only/pydistmaker.json`
- `examples/mixed_mode/pydistmaker.json`
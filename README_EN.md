# PyDistMaker - Python Application Packaging Tool

[English](./README_EN.md) | [中文](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

PyDistMaker is a Python packaging tool that combines the advantages of Nuitka and PyInstaller, supporting multi-entry script packaging, onedir mode, and flexible configuration options.

## Features

- **Hybrid Compilation Packaging**: Combines the advantages of Nuitka and PyInstaller to provide a more efficient packaging solution
- **Multi-Entry Script Support**: Configure once, package multiple executables simultaneously
- **Onedir Mode**: Generate applications with a clear directory structure
- **Flexible Configuration**: Provides rich configuration options to meet various packaging needs
- **Cross-Platform Support**: Supports Windows, macOS, and Linux platforms

## Installation

Install PyDistMaker using pip:

```bash
pip install pydistmaker
```

## Quick Start

### 1. Initialize Configuration File

```bash
pydistmaker init --output=pydistmaker.json
```

Optional parameters:
- `--output, -o`: Specify the configuration file output path, default is `pydistmaker.json`
- `--schema, -s`: Generate JSON Schema file simultaneously

### 2. Modify Configuration File

Adjust the configuration file according to project requirements:

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
  },
  "artifactory": {
    "url": "https://artifactory.example.com",
    "repository": "my-repo",
    "username": "username",
    "password": "password",
    "path_prefix": "python-apps",
    "properties": {
      "app.type": "python",
      "app.name": "myapp"
    }
  }
}
```

### 3. Execute Packaging

```bash
pydistmaker build --config=pydistmaker.json
```

Optional parameters:
- `--config, -c`: Specify the configuration file path, default is `pydistmaker.json`

### 4. Verify Configuration File

```bash
pydistmaker verify --config=pydistmaker.json --strict
```

Optional parameters:
- `--config, -c`: Specify the configuration file path, default is `pydistmaker.json`
- `--strict, -s`: Enable strict mode, check if file paths exist

### 5. Upload to Artifactory

Upload compilation artifacts to Artifactory repository:

```bash
pydistmaker upload --config=pydistmaker.json --build
```

Optional parameters:
- `--config, -c`: Specify the configuration file path, default is `pydistmaker.json`
- `--build, -b`: Execute packaging before uploading
- `--mode, -m`: Compilation mode, available values are `nuitka_only`, `pyinstaller_only`, `mixed`

Upload feature description:
- The `artifactory` section must be added to the configuration file before uploading
- Files in the output directory will be automatically packaged as a ZIP file during upload
- Upload path format: `{path_prefix}/{project_name}/{version}/{project_name}-{version}.zip`
- Support for adding custom properties to uploaded artifacts

## Configuration File Description

### Project Configuration (project)

| Field | Type | Description | Default Value |
|------|------|------|--------|
| `name` | String | Project name | - |
| `version` | String | Version number (SemVer format) | - |
| `entries` | String Array | Entry script path list | - |
| `output_dir` | String | Output directory path | `dist` |

### Nuitka Configuration (nuitka)

| Field | Type | Description | Default Value |
|------|------|------|--------|
| `modules` | String Array | Core modules to compile | `[]` |
| `lto` | Boolean | Enable link-time optimization | `true` |
| `jobs` | Integer | Number of parallel compilation threads | `4` |
| `standalone` | Boolean | Generate standalone executable | `true` |
| `plugins` | String Array | List of enabled plugins | `[]` |
| `include_packages` | String Array | List of included packages | `[]` |
| `extra_args` | String Array | Additional Nuitka command line arguments | `null` |

### PyInstaller Configuration (pyinstaller)

| Field | Type | Description | Default Value |
|------|------|------|--------|
| `mode` | String | Packaging mode (`onedir` or `onefile`) | `onedir` |
| `bin_dir` | String | Directory for dependent binary files | `bin` |
| `hidden_imports` | String Array | List of hidden import modules | `[]` |
| `add_data` | String Array | List of additional resource files | `[]` |
| `icon` | String | Executable file icon path | `null` |
| `runtime_tmpdir` | String | Runtime temporary directory | `null` |

### Artifactory Configuration (artifactory)

| Field | Type | Description | Default Value |
|------|------|------|--------|
| `url` | String | Artifactory server URL | - |
| `repository` | String | Repository name | - |
| `username` | String | Username | - |
| `password` | String | Password | - |
| `path_prefix` | String | Path prefix (optional) | `null` |
| `properties` | Object | Custom properties (optional) | `null` |

## Output Directory Structure

After packaging with `onedir` mode, the output directory structure is as follows:

```
dist/
├── main.exe
├── cli.exe
└── bin/
    ├── lib1.dll
    ├── lib2.so
    └── ...
```

## Hybrid Compilation Packaging Process

1. Entry file analysis
2. Nuitka compilation of core modules, generating .pyd/.so files
3. Dependency analysis, generating dependency graph
4. PyInstaller packaging, generating executable files
5. Security hardening processing
6. Organizing output directory
7. Generating MANIFEST file

## Cross-Platform Support

- **Path Processing**: Uniformly use POSIX format paths, automatically convert to backslashes on Windows
- **Platform-Specific Parameters**:
  - Windows: Support for Signtool signing
  - macOS: Support for codesign signing
  - Linux: Support for GPG signing

## Command Line Reference

| Command | Function | Parameter Example |
|------|------|----------|
| `pydistmaker build` | Execute packaging process | `--config=config.json` |
| `pydistmaker init` | Generate configuration template | `--output=custom_config.json` |
| `pydistmaker verify` | Verify configuration file validity | `--strict` |
| `pydistmaker upload` | Upload artifacts to Artifactory | `--build --mode=mixed` |

## License

[MIT License](LICENSE) © mogulion
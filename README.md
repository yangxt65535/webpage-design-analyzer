# webpage-design-analyzer

提供本地图片，通过调用视觉模型 API，生成前端页面的设计文档。

## 环境要求

本项目使用 uv 管理，uv 是一个基于 Rust 开发的高性能 Python 包管理器，可通过以下方式安装：

```bash
# Bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 运行项目

### 安装项目

建设中

### 源码运行

#### 运行步骤

1. 克隆本仓库

2. 从 `.env.template` 复制一个 `.env` 文件，将个人的 OPENAI 或兼容 API 信息填入 `.env` 文件。

    ```
    OPENAI_API_URL=YOUR_API_BASE
    OPENAI_API_KEY=YOUR_API_KEY
    MODEL=YOUR_MODEL  # MODEL为选填项，默认使用 gpt-4.1-mini
    ```

3. 直接运行命令，uv 将自动使用虚拟环境。初次运行时会在当前目录自动创建虚拟环境并安装依赖。

    ```bash
    uv analyzer.py [IMAGE_PATH]
    ```

#### 参数说明

- `IMAGE_PATH`：要分析的图片文件路径（支持JPG/PNG等常见格式）

#### 输出

页面开发方案将会输出到**与输入文件同名的 Markdown文件**，包含：

1. 页面布局分析
2. 内容与功能描述
3. 公共样式表格

## FAQ

- uv 通过识别 `pyproject.toml` 与 `.python-version` 中的相关字段使用特定的 Python 版本。项目默认使用 Python 3.11，如遇版本问题，可直接修改相关字段，也可以使用 uv 的 Python 多版本功能：

  ```bash
  uv python install 3.11
  uv python list
  ```
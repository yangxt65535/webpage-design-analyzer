# Web 设计图分析 MCP 服务器

Python实现的MCP服务器，提供本地图片绝对路径，通过调用视觉模型 API，生成前端页面的设计文档。

## API

### Tools

- analyze_image_tool
  - 通过调用视觉大模型 API，分析页面设计图，制定开发方案
  - Input: `image_path`(string) 图片在设备上的绝对路径
  - Return (string): Markdown 格式输出的页面开发方案

## 启动服务

项目使用 uv 管理，uv 是一个基于 Rust 开发的高性能 Python 包、项目管理器，通过以下方式安装：

```bash
# Bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

uv 通过识别 `pyproject.toml` 与 `.python-version` 中的相关字段使用特定的 Python 版本。项目默认使用 Python 3.11，如遇版本问题，可直接修改相关字段，也可以使用 uv 的 Python 多版本功能：

```bash
uv python install 3.11
uv python list
```

在支持 MCP 的客户端中，通过以下方式引入：

```json
{
  "key": "DesignAnalysis",
  "description": "调用视觉模型API服务分析网页设计图内容，并返回AI的分析结果",
  "command": "uv",
  "args": [
    "--directory",
    "C:\\ABSOLUTE\\PATH\\TO\\PROJECT\\FOLDER",
    "run",
    "image_analysis_service.py"
  ],
  "env": {
    "OPENAI_API_URL": "YOUR_API_URL",
    "OPENAI_API_KEY": "sk-YOU_API_KEY"
  }
}
```

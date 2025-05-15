import base64
import os
import requests

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
    
class ImageAnalysisService:
    FE_EXPERT_PROMPT = """
        你是一个专业的前端开发工程师，你的工作是仔细观察提供的前端页面设计图，分析其内容细节、样式布局等关键信息，输出设计文档。以下是设计要求：
        1.应用要与设计图内容、布局上保持一致；
        2.关注背景颜色、字号字色、margin、padding等样式；
        3.标题、正文与设计图中的完全一致；
        使用 Markdown 语法输出，不要包含在代码块中，符合以下结构：
        1. 布局：将页面分块并总结每个分块的功能
        2. 内容与功能：对于每个分块，描述其内容和功能细节
        3. 公共样式：以表格形式列出公共样式，包括字体、颜色、间距等
        """
    
    def __init__(self):
        self.api_base = os.getenv("OPENAI_API_URL")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        
        if not self.api_base or not self.api_key:
            raise ValueError("请设置环境变量 OPENAI_API_URL 和 OPENAI_API_KEY")

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_image(self, image_path):
        try:
            image_base64 = self.encode_image_to_base64(image_path)
        except:
            return "无法读取图片，请检查图片路径是否正确。"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.FE_EXPERT_PROMPT
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "根据这张前端页面设计图，分析页面内容、布局与样式。"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(self.api_base, json=data, headers=headers)
        response.raise_for_status()
        
        # 解析完整响应，提取分析结果
        result = ""
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0].get("message", {}).get("content", "")
        
        return result

service = ImageAnalysisService()

mcp = FastMCP("image_analysis_service")

@mcp.tool()
async def analyze_image_tool(image_path: str):
    """
    调用视觉模型API服务分析网页设计图内容，并返回AI的分析结果
    Args:
        image_path: string, 要分析的图片绝对路径
    
    Returns: 
        string, AI对图片的分析结果
    """
    return service.analyze_image(image_path)
    
    # 启动服务
if __name__ == "__main__":
    mcp.run(transport='stdio')
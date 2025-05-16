import base64
import os
import requests
import argparse
from PIL import Image
from dotenv import load_dotenv

class WebpageDesignAnalyzer:
    FE_EXPERT_SYSTEM_PROMPT = """
        你是一个专业的前端开发工程师，你的工作是仔细观察提供的前端页面设计图，分析其内容细节、样式布局等关键信息，输出设计文档。以下是设计要求：
        1.应用要与设计图内容、布局上保持一致；
        2.关注背景颜色、字号字色、margin、padding等样式；
        3.标题、正文与设计图中的完全一致；
        使用 Markdown 语法输出，不要包含在代码块中，符合以下结构：
        1. 布局：将页面分块并总结每个分块的功能
        2. 内容与功能：对于每个分块，描述其内容和功能细节
        3. 公共样式：以表格形式列出公共样式，包括字体、颜色、间距等
        """
    FE_EXPERT_USER_PROMPT = "根据这张前端页面设计图，分析页面内容、布局与样式。"
    
    def __init__(self):
        load_dotenv()
        self.api_base = os.getenv("OPENAI_API_URL")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        
        if not self.api_base or not self.api_key:
            raise ValueError("请设置环境变量 OPENAI_API_URL 和 OPENAI_API_KEY")

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def generate_request(self, image_base64):
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
                    "content": self.FE_EXPERT_SYSTEM_PROMPT
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
                            "text": self.FE_EXPERT_USER_PROMPT
                        }
                    ]
                }
            ]
        }
        
        return headers, data

    def analyze_image(self, image_path):
        try:
            image_base64 = self.encode_image_to_base64(image_path)
        except:
            return "无法读取图片，请检查图片路径是否正确。"
        
        headers, data = self.generate_request(image_base64)
        response = requests.post(self.api_base, json=data, headers=headers)
        response.raise_for_status()
        
        # 解析完整响应，提取分析结果
        result = ""
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0].get("message", {}).get("content", "")
        
        return result

def validate_image_file(image_path):
    """验证文件是否为有效的图片文件"""
    if not os.path.exists(image_path):
        raise ValueError(f"文件不存在: {image_path}")
    
    try:
        with Image.open(image_path) as img:
            img.verify()  # 验证图片完整性
    except Exception as e:
        raise ValueError(f"无效的图片文件: {str(e)}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='网页设计图分析工具')
    parser.add_argument('image_path', type=str, help='要分析的图片路径')
    args = parser.parse_args()

    analyzer = WebpageDesignAnalyzer()
    
    try:
        validate_image_file(args.image_path)
        print("正在分析图片，请稍候...")
        result = analyzer.analyze_image(args.image_path)
        output_path = os.path.splitext(args.image_path)[0] + ".md"
        print(f"分析完成，输出到{output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
    except ValueError as e:
        print(f"错误: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()

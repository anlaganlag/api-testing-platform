from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our book generator
from src.enhanced_book_generator_fixed import EnhancedBookGenerator

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path = self.path.rstrip('/')
        if self.path == '':
            self.path = '/'
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>书籍生成 API</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding: 20px; font-family: "Microsoft YaHei", "Hiragino Sans GB", "Heiti SC", sans-serif; }
                .container { max-width: 800px; margin: 0 auto; }
                .form-group { margin-bottom: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="mb-4">教材生成器</h1>
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">生成样例章节</h5>
                        <form action="/api/generate" method="POST">
                            <div class="form-group">
                                <label for="excel_path">Excel 路径:</label>
                                <input type="text" class="form-control" id="excel_path" name="excel_path" value="data/book_outline.xlsx">
                            </div>
                            <div class="form-group">
                                <label for="provider">API 提供商:</label>
                                <select class="form-control" id="provider" name="provider">
                                    <option value="all">所有提供商</option>
                                    <option value="deepseek">DeepSeek</option>
                                    <option value="gemini">Gemini</option>
                                    <option value="openrouter">OpenRouter</option>
                                    <option value="siliconflow">SiliconFlow</option>
                                    <option value="ark">Ark</option>
                                    <option value="dashscope">灵积（DashScope）</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="chapter_index">章节索引:</label>
                                <input type="number" class="form-control" id="chapter_index" name="chapter_index" value="0">
                            </div>
                            <button type="submit" class="btn btn-primary">生成样例章节</button>
                        </form>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">API 文档</h5>
                        <p>此 API 允许您基于 Excel 大纲生成书籍内容。</p>
                        <h6>接口:</h6>
                        <ul>
                            <li><code>POST /api/generate</code> - 生成样例章节</li>
                        </ul>
                        <h6>参数:</h6>
                        <ul>
                            <li><code>excel_path</code> - Excel 大纲文件路径</li>
                            <li><code>provider</code> - 使用的 API 提供商 (deepseek, gemini, openrouter, siliconflow, ark, dashscope, all)</li>
                            <li><code>chapter_index</code> - 要生成的章节索引 (从 0 开始)</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode('utf-8'))
        return
    
    def do_POST(self):
        if self.path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            
            excel_path = form_data.get('excel_path', ['data/book_outline.xlsx'])[0]
            provider = form_data.get('provider', ['all'])[0]
            chapter_index = int(form_data.get('chapter_index', ['0'])[0])
            
            try:
                # Initialize the generator
                generator = EnhancedBookGenerator(excel_path, provider=provider)
                
                # Generate a sample chapter
                success = generator.generate_sample_chapter(chapter_index)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                response = {
                    'success': success,
                    'message': '章节生成成功！' if success else '章节生成失败'
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                response = {
                    'success': False,
                    'message': f'错误: {str(e)}'
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {
                'success': False,
                'message': '未找到请求的接口'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 
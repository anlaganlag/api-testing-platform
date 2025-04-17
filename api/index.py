from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
import sys
import tempfile
import uuid
from threading import Lock
from time import sleep

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our book generator
from src.enhanced_book_generator_fixed import EnhancedBookGenerator

# 添加全局状态存储
GENERATION_STATUS = {}
status_lock = Lock()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/download':
            # 处理下载请求
            book_id = self.path.split('=')[-1]
            file_path = GENERATION_STATUS.get(book_id, {}).get('file_path')
            
            if file_path and os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="generated_book_{book_id}.docx"')
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "File not found")
                return

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
                .progress { height: 20px; margin: 10px 0; }
                #uploadProgress, #generateProgress { width: 0%; transition: width 0.3s; }
                .hidden { display: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="mb-4">教材生成器</h1>
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">上传书籍大纲</h5>
                        <form id="uploadForm" enctype="multipart/form-data">
                            <div class="form-group">
                                <input type="file" class="form-control" id="excelFile" name="excel_file" accept=".xlsx">
                            </div>
                            <button type="submit" class="btn btn-primary">上传文件</button>
                        </form>
                        <div class="progress">
                            <div id="uploadProgress" class="progress-bar" role="progressbar"></div>
                        </div>
                    </div>
                </div>
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">生成样例章节</h5>
                        <form id="generateForm">
                            <div class="progress">
                                <div id="generateProgress" class="progress-bar" role="progressbar"></div>
                            </div>
                            <div id="downloadSection" class="hidden">
                                <a id="downloadLink" class="btn btn-success">下载书籍</a>
                            </div>
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
            <script>
                // 文件上传处理
                document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData();
                    formData.append('excel_file', document.getElementById('excelFile').files[0]);

                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    document.getElementById('excel_path').value = result.file_path;
                });

                // 生成处理
                document.getElementById('generateForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        body: new URLSearchParams(formData)
                    });
                    
                    const { book_id } = await response.json();
                    checkStatus(book_id);
                });

                async function checkStatus(book_id) {
                    const res = await fetch(`/api/status?book_id=${book_id}`);
                    const { progress, status, download_url } = await res.json();
                    
                    document.getElementById('generateProgress').style.width = `${progress}%`;
                    
                    if (status === 'completed') {
                        document.getElementById('downloadSection').classList.remove('hidden');
                        document.getElementById('downloadLink').href = download_url;
                    } else if (status === 'processing') {
                        setTimeout(() => checkStatus(book_id), 1000);
                    }
                }
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode('utf-8'))
        return
    
    def do_POST(self):
        if self.path == '/api/upload':
            # 处理文件上传
            content_type = self.headers['Content-Type']
            if not content_type.startswith('multipart/form-data'):
                return self.send_error(400, "Bad request")
            
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, 'uploaded_file.xlsx')
            
            # 解析文件上传
            content = self.rfile.read(int(self.headers['Content-Length']))
            with open(file_path, 'wb') as f:
                f.write(content.split(b'\r\n\r\n')[1].split(b'\r\n--')[0])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'file_path': file_path}).encode())
            return

        elif self.path == '/api/generate':
            # 修改生成逻辑
            book_id = str(uuid.uuid4())
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            
            # 初始化状态
            with status_lock:
                GENERATION_STATUS[book_id] = {
                    'progress': 0,
                    'status': 'processing',
                    'file_path': None
                }

            # 启动后台生成任务
            def generate_task():
                try:
                    generator = EnhancedBookGenerator(
                        form_data['excel_path'][0],
                        provider=form_data.get('provider', ['all'])[0]
                    )
                    
                    # 生成章节并更新进度
                    total_chapters = len(generator.outline_data)
                    for i in range(total_chapters):
                        generator.generate_sample_chapter(i)
                        with status_lock:
                            GENERATION_STATUS[book_id]['progress'] = (i+1)/total_chapters*100
                        sleep(0.5)  # 模拟生成时间
                    
                    # 保存生成结果
                    output_path = os.path.join(tempfile.gettempdir(), f'book_{book_id}.docx')
                    generator.save_book(output_path)
                    
                    with status_lock:
                        GENERATION_STATUS[book_id].update({
                            'status': 'completed',
                            'file_path': output_path
                        })
                        
                except Exception as e:
                    with status_lock:
                        GENERATION_STATUS[book_id]['status'] = 'error'
                        GENERATION_STATUS[book_id]['error'] = str(e)

            # 启动后台线程
            import threading
            threading.Thread(target=generate_task).start()

            # 返回生成ID
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'book_id': book_id}).encode())
            return

        elif self.path == '/api/status':
            # 添加状态查询接口
            book_id = parse_qs(self.path.split('?')[-1]).get('book_id', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = GENERATION_STATUS.get(book_id, {})
            response = {
                'progress': status.get('progress', 0),
                'status': status.get('status', 'not_found'),
                'download_url': f'/download?book_id={book_id}' if status.get('file_path') else None
            }
            self.wfile.write(json.dumps(response).encode())
            return

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {
                'success': False,
                'message': '未找到请求的接口'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 
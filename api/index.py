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
        if self.path.startswith('/download'):
            # 处理下载请求
            query_string = self.path.split('?')
            book_id = ''
            
            if len(query_string) > 1:
                params = parse_qs(query_string[1])
                book_id = params.get('book_id', [''])[0]
            
            file_path = GENERATION_STATUS.get(book_id, {}).get('file_path')
            
            if file_path and os.path.exists(file_path):
                self.send_response(200)
                
                # 根据文件类型设置Content-Type
                if file_path.endswith('.docx'):
                    self.send_header('Content-type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    filename = f"generated_book_{book_id}.docx"
                elif file_path.endswith('.md'):
                    self.send_header('Content-type', 'text/markdown')
                    filename = f"generated_chapter_{book_id}.md"
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                    filename = f"generated_file_{book_id}{os.path.splitext(file_path)[1]}"
                
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
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
                            <div class="form-group">
                                <input type="hidden" id="excel_path" name="excel_path" value="">
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
                // 禁用生成按钮直到文件上传成功
                document.addEventListener('DOMContentLoaded', function() {
                    document.querySelector('#generateForm button[type="submit"]').disabled = true;
                });
                
                // 文件上传处理
                document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData();
                    const fileInput = document.getElementById('excelFile');
                    
                    if (!fileInput.files || fileInput.files.length === 0) {
                        alert('请选择一个Excel文件');
                        return;
                    }
                    
                    // 显示上传进度
                    const progressBar = document.getElementById('uploadProgress');
                    progressBar.style.width = '50%';
                    
                    try {
                        formData.append('excel_file', fileInput.files[0]);
                        
                        const response = await fetch('/api/upload', {
                            method: 'POST',
                            body: formData
                        });
                        
                        progressBar.style.width = '100%';
                        
                        if (!response.ok) {
                            throw new Error('上传失败: ' + response.status);
                        }
                        
                        let result;
                        try {
                            result = await response.json();
                        } catch (parseError) {
                            console.error('解析上传响应失败:', await response.text());
                            throw new Error('服务器返回了无效数据');
                        }
                        
                        if (result && result.success) {
                            // 存储文件路径到隐藏字段
                            document.getElementById('excel_path').value = result.file_path;
                            alert('文件上传成功，可以开始生成书籍');
                            // 启用生成按钮
                            document.querySelector('#generateForm button[type="submit"]').disabled = false;
                        } else {
                            throw new Error(result.message || '上传失败');
                        }
                    } catch (error) {
                        console.error('上传错误:', error);
                        progressBar.style.width = '0%';
                        alert('上传出错: ' + error.message);
                    }
                });

                // 生成处理
                document.getElementById('generateForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const excelPath = document.getElementById('excel_path').value;
                    if (!excelPath) {
                        alert('请先上传Excel文件');
                        return;
                    }
                    
                    const formData = new FormData(e.target);
                    
                    try {
                        const response = await fetch('/api/generate', {
                            method: 'POST',
                            body: new URLSearchParams(formData)
                        });
                        
                        if (!response.ok) {
                            throw new Error('生成请求失败');
                        }
                        
                        const data = await response.json();
                        if (data.book_id) {
                            checkStatus(data.book_id);
                        } else {
                            alert('生成请求发送失败');
                        }
                    } catch (error) {
                        console.error('生成错误:', error);
                        alert('生成请求出错，请重试');
                    }
                });

                async function checkStatus(book_id) {
                    try {
                        const response = await fetch(`/api/status?book_id=${book_id}`);
                        if (!response.ok) {
                            throw new Error('状态查询失败');
                        }
                        
                        let data;
                        try {
                            data = await response.json();
                        } catch (parseError) {
                            console.error('解析JSON失败', await response.text());
                            alert('服务器返回了无效数据，查看控制台了解详情');
                            return;
                        }
                        
                        const progressBar = document.getElementById('generateProgress');
                        progressBar.style.width = `${data.progress}%`;
                        
                        if (data.status === 'completed') {
                            document.getElementById('downloadSection').classList.remove('hidden');
                            document.getElementById('downloadLink').href = data.download_url;
                            alert('书籍生成完成，可以下载了！');
                        } else if (data.status === 'processing') {
                            setTimeout(() => checkStatus(book_id), 1000);
                        } else if (data.status === 'error') {
                            alert('生成过程中出错: ' + (data.error || '未知错误'));
                        }
                    } catch (error) {
                        console.error('状态查询错误:', error);
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
            try:
                content_type = self.headers['Content-Type']
                if not content_type or not content_type.startswith('multipart/form-data'):
                    return self.send_error(400, "错误的请求格式，需要multipart/form-data")
                
                # 解析边界
                boundary = content_type.split('=')[1].strip()
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # 创建临时目录
                temp_dir = tempfile.mkdtemp()
                file_path = os.path.join(temp_dir, 'uploaded_file.xlsx')
                
                # 简化的multipart解析
                file_data_start = post_data.find(b'\r\n\r\n') + 4
                file_data_end = post_data.rfind(b'\r\n--' + boundary.encode() + b'--')
                if file_data_start > 0 and file_data_end > 0:
                    file_data = post_data[file_data_start:file_data_end]
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                
                # 返回成功响应
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                response = {
                    'success': True,
                    'file_path': file_path,
                    'message': '文件上传成功'
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                response = {
                    'success': False,
                    'message': f'上传文件错误: {str(e)}'
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
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
                    
                    # 加载大纲以获取章节数
                    generator.load_outline()
                    
                    # 生成章节并更新进度
                    chapter_index = int(form_data.get('chapter_index', ['0'])[0])
                    
                    # 仅生成单个章节，而不是全部
                    success = generator.generate_sample_chapter(chapter_index)
                    
                    with status_lock:
                        if success:
                            # 获取生成的文件路径
                            is_production = os.environ.get('VERCEL') == '1'
                            if is_production:
                                output_dir = "/tmp/output"
                            else:
                                output_dir = "output"
                                
                            # 查找生成的markdown文件
                            import glob
                            md_files = glob.glob(os.path.join(output_dir, "*.md"))
                            if md_files:
                                newest_file = max(md_files, key=os.path.getmtime)
                                GENERATION_STATUS[book_id].update({
                                    'status': 'completed',
                                    'file_path': newest_file,
                                    'progress': 100
                                })
                            else:
                                raise Exception("未找到生成的文件")
                        else:
                            raise Exception("章节生成失败")
                        
                except Exception as e:
                    with status_lock:
                        GENERATION_STATUS[book_id]['status'] = 'error'
                        GENERATION_STATUS[book_id]['error'] = str(e)
                        print(f"生成错误: {str(e)}")  # 调试输出

            # 启动后台线程
            import threading
            threading.Thread(target=generate_task).start()

            # 返回生成ID
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'book_id': book_id}, ensure_ascii=False).encode('utf-8'))
            return

        elif self.path == '/api/status':
            # 添加状态查询接口
            query_string = self.path.split('?')
            book_id = ''
            
            if len(query_string) > 1:
                params = parse_qs(query_string[1])
                book_id = params.get('book_id', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            status = GENERATION_STATUS.get(book_id, {})
            response = {
                'progress': status.get('progress', 0),
                'status': status.get('status', 'not_found'),
                'download_url': f'/download?book_id={book_id}' if status.get('file_path') else None
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
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
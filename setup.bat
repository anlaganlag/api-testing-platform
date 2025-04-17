@echo off

:: Install Python and pip
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python 3 first.
    pause
    exit /b
)

:: Install project dependencies
pip install -r requirements.txt

:: Set up environment variables
if not exist ".env" (
    echo Creating .env file...
    (
        echo # API Configurations
        echo;
        echo # DeepSeek
        echo DEEPSEEK_API_KEY=your_deepseek_api_key_here
        echo DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
        echo DEEPSEEK_API_MODEL=deepseek-reasoner
        echo;
        echo # Gemini
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models
        echo GEMINI_API_MODEL=gemini-2.0-flash-lite
        echo;
        echo # OpenRouter.ai
        echo OPENROUTER_API_KEY=your_openrouter_api_key_here
        echo OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
        echo OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
        echo;
        echo # Siliconflow
        echo SILICONFLOW_API_KEY=your_siliconflow_api_key_here
        echo SILICONFLOW_API_URL=https://api.siliconflow.cn/v1/chat/completions
        echo SILICONFLOW_MODEL=deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
        echo;
        echo # Ark
        echo ARK_API_KEY=your_ark_api_key_here
        echo ARK_API_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
        echo ARK_MODEL=deepseek-r1-distill-qwen-7b-250120
        echo;
        echo # DASHSCOP
        echo DASHSCOPE_API_KEY=your_dashscope_api_key_here
        echo DASHSCOP_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
        echo DASHSCOP_MODEL=deepseek-r1-distill-qwen-7b-250120
        echo;
        echo # Optional Configuration
        echo TEMPERATURE=0.7
        echo MAX_TOKENS=10000
    ) > .env
) else (
    echo .env file already exists.
)

echo Project environment setup complete.
pause
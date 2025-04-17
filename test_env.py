from dotenv import load_dotenv
import os
import requests
from time import time
from tabulate import tabulate
from openai import OpenAI

# Load environment variables
load_dotenv()

# |Gemini      │ ✅       │ 1.01s           │ Hello World      │
# │ OpenRouter  │ ✅       │ 2.22s           │ Hello World! 😊  │
# │ DeepSeek    │ ✅       │ 5.94s           │ Hello World!     │
# │ Siliconflow │ ✅       │ 12.54s          │ Hello World!     │
# │ Ark         │ ✅       │ 6.69s           │ Hello World.     │

# Test API configurations
providers = [
    ("Gemini", "GEMINI_API_KEY"),
    ("OpenRouter", "OPENROUTER_API_KEY"),
    ("DeepSeek", "DEEPSEEK_API_KEY"),
    ("Siliconflow", "SILICONFLOW_API_KEY"),
    ("Ark", "ARK_API_KEY"),
    ("DASHSCOP", "DASHSCOPE_API_KEY")
]

print("Testing API configurations:\n")
for name, key in providers:
    api_key = os.getenv(key)
    print(f"{name}:")
    print(f"API Key: {api_key[:5]}...{api_key[-5:] if api_key else ''}")
    print(f"Status: {'Present' if api_key else 'Missing'}\n")

# Test DeepSeek specific configurations
print("\nTesting DeepSeek specific configurations:")
print(f"API URL: {os.getenv('DEEPSEEK_API_URL')}")
print(f"Model: {os.getenv('DEEPSEEK_API_MODEL')}")

def test_gemini(key):
    try:
        start = time()
        model = os.getenv("GEMINI_API_MODEL", "gemini-2.0-flash-lite")
        base_url = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models")
        url = f"{base_url}/{model}:generateContent"
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            params={"key": key},
            json={"contents": [{"parts": [{"text": "Say 'Hello World'"}]}]}
        )
        return {
            "status": response.ok,
            "response": response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', ''),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

def test_openrouter(key):
    try:
        start = time()
        model = os.getenv("OPENROUTER_MODEL", "google/palm-2")
        url = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
        
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "HTTP-Referer": "https://github.com/user/repo",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Say 'Hello World'"}]
            }
        )
        return {
            "status": response.ok,
            "response": response.json().get('choices', [{}])[0].get('message', {}).get('content', ''),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

def test_deepseek(key):
    try:
        start = time()
        response = requests.post(
            os.getenv("DEEPSEEK_API_URL"),
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": os.getenv("DEEPSEEK_API_MODEL"),
                "messages": [{"role": "user", "content": "Say 'Hello World'"}]
            }
        )
        return {
            "status": response.ok,
            "response": response.json().get('choices', [{}])[0].get('message', {}).get('content', ''),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

def test_siliconflow(key):
    try:
        start = time()
        response = requests.post(
            os.getenv("SILICONFLOW_API_URL"),
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": os.getenv("SILICONFLOW_MODEL"),
                "messages": [{"role": "user", "content": "Say 'Hello World'"}]
            }
        )
        return {
            "status": response.ok,
            "response": response.json().get('choices', [{}])[0].get('message', {}).get('content', ''),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

def test_ark(key):
    try:
        start = time()
        response = requests.post(
            os.getenv("ARK_API_URL"),
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": os.getenv("ARK_MODEL"),
                "messages": [{"role": "user", "content": "Say 'Hello World'"}]
            }
        )
        return {
            "status": response.ok,
            "response": response.json().get('choices', [{}])[0].get('message', {}).get('content', ''),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

def test_dashscop(key):
    try:
        start = time()
        
        client = OpenAI(
            api_key=key,
            base_url=os.getenv("DASHSCOP_API_URL")
        )

        completion = client.chat.completions.create(
            model=os.getenv("DASHSCOP_MODEL").replace("-250120", ""),
            messages=[
                {"role": "user", "content": "Say 'Hello World'"}
            ]
        )
        
        return {
            "status": True,
            "response": completion.choices[0].message.content.strip(),
            "time": time() - start
        }
    except Exception as e:
        return {"status": False, "error": str(e), "time": time() - start}

results = []

# Test Gemini
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    result = test_gemini(gemini_key)
    results.append([
        "Gemini",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Test OpenRouter
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_key:
    result = test_openrouter(openrouter_key)
    results.append([
        "OpenRouter",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Test DeepSeek
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
if deepseek_key and os.getenv("DEEPSEEK_API_URL") and os.getenv("DEEPSEEK_API_MODEL"):
    result = test_deepseek(deepseek_key)
    results.append([
        "DeepSeek",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Test Siliconflow
siliconflow_key = os.getenv("SILICONFLOW_API_KEY")
if siliconflow_key and os.getenv("SILICONFLOW_API_URL") and os.getenv("SILICONFLOW_MODEL"):
    result = test_siliconflow(siliconflow_key)
    results.append([
        "Siliconflow",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Test Ark
ark_key = os.getenv("ARK_API_KEY")
if ark_key and os.getenv("ARK_API_URL") and os.getenv("ARK_MODEL"):
    result = test_ark(ark_key)
    results.append([
        "Ark",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Test DASHSCOP
dashscop_key = os.getenv("DASHSCOPE_API_KEY")
if dashscop_key and os.getenv("DASHSCOP_API_URL") and os.getenv("DASHSCOP_MODEL"):
    result = test_dashscop(dashscop_key)
    results.append([
        "DASHSCOP",
        "✅" if result['status'] else "❌",
        f"{result['time']:.2f}s",
        result.get('response', result.get('error', 'Unknown error'))
    ])

# Print results table
print("\nAPI Test Results:")
print(tabulate(
    results,
    headers=["Provider", "Status", "Response Time", "Response/Error"],
    tablefmt="rounded_outline"
))

# Add main function to test a specific provider
if __name__ == "__main__":
    import argparse
    
    # Create command line argument parser
    parser = argparse.ArgumentParser(description="Test API provider configurations")
    parser.add_argument("--provider", "-p", choices=["all", "gemini", "openrouter", "deepseek", "siliconflow", "ark", "dashscop"],
                        default="all", help="API provider to test (default: all)")
    
    args = parser.parse_args()
    provider = args.provider
    
    if provider == "all":
        # The tests are already run when the module is imported
        pass
    elif provider == "gemini":
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            print("\nTesting Gemini API:")
            result = test_gemini(gemini_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("Gemini API key not found in environment variables")
    elif provider == "openrouter":
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            print("\nTesting OpenRouter API:")
            result = test_openrouter(openrouter_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("OpenRouter API key not found in environment variables")
    elif provider == "deepseek":
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key and os.getenv("DEEPSEEK_API_URL") and os.getenv("DEEPSEEK_API_MODEL"):
            print("\nTesting DeepSeek API:")
            result = test_deepseek(deepseek_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("DeepSeek API configuration not complete in environment variables")
    elif provider == "siliconflow":
        siliconflow_key = os.getenv("SILICONFLOW_API_KEY")
        if siliconflow_key and os.getenv("SILICONFLOW_API_URL") and os.getenv("SILICONFLOW_MODEL"):
            print("\nTesting Siliconflow API:")
            result = test_siliconflow(siliconflow_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("Siliconflow API configuration not complete in environment variables")
    elif provider == "ark":
        ark_key = os.getenv("ARK_API_KEY")
        if ark_key and os.getenv("ARK_API_URL") and os.getenv("ARK_MODEL"):
            print("\nTesting Ark API:")
            result = test_ark(ark_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("Ark API configuration not complete in environment variables")
    elif provider == "dashscop":
        dashscop_key = os.getenv("DASHSCOPE_API_KEY")
        if dashscop_key and os.getenv("DASHSCOP_API_URL") and os.getenv("DASHSCOP_MODEL"):
            print("\nTesting DASHSCOP API:")
            result = test_dashscop(dashscop_key)
            print(f"Status: {'✅ Success' if result['status'] else '❌ Failed'}")
            print(f"Response time: {result['time']:.2f}s")
            print(f"Response: {result.get('response', result.get('error', 'Unknown error'))}")
        else:
            print("DASHSCOP API configuration not complete in environment variables") 
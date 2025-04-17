import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Siliconflow configuration


# Example model from Siliconflow
import requests

url = os.getenv("SILICONFLOW_API_URL")

payload = {
    "model": os.getenv("SILICONFLOW_MODEL"),
    "messages": [
        {
            "role": "user",
            "content": "hello world"
        }
    ],
    "stream": False,
    "max_tokens": 512,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {"type": "text"},
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "<string>",
                "name": "<string>",
                "parameters": {},
                "strict": False
            }
        }
    ]
}
headers = {
    "Authorization": f"Bearer {os.getenv('SILICONFLOW_API_KEY')}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
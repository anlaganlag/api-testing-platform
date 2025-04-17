import os
from openai import OpenAI

# OpenRouter configuration
client = OpenAI(
    # Add your OpenRouter API key here
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    # Additional headers required by OpenRouter
    default_headers={
        "HTTP-Referer": "https://github.com/user/repo" # Recommended by OpenRouter for tracking
    }
)

# Example models: 
# - "anthropic/claude-3-opus"
# - "anthropic/claude-3-sonnet"
# - "google/gemini-pro" 
# - "meta-llama/llama-3-70b-instruct"
# Check https://openrouter.ai/docs for the full list of available models

completion = client.chat.completions.create(
    model="deepseek/deepseek-r1-distill-qwen-14b:free", # Replace with your preferred model
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'What can you tell me about OpenRouter?'}
    ]
)

print(completion.choices[0].message.content)
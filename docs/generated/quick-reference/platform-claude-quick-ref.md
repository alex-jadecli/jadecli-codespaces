# Claude API Quick Reference

Using the Claude API for AI-powered applications.

## Models

```
Smartest:    claude-opus-4-5-20251101        (most capable, ~200K context)
Smart:       claude-sonnet-4-5-20250929      (balanced speed/quality)
Fast:        claude-haiku-4-5-20251001       (cost-effective, fast)
```

## Basic API Call (Python)

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

print(message.content[0].text)
```

## Multi-turn Conversation

```python
messages = [
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
    {"role": "user", "content": "Double that result"}
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

## Tool Use (Function Calling)

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in SF?"}
    ]
)

# Check if Claude wants to use a tool
if response.stop_reason == "tool_use":
    tool_use = response.content[1]  # ToolUse block
    print(f"Tool: {tool_use.name}")
    print(f"Input: {tool_use.input}")
```

## Vision (Image Input)

```python
import base64

# From file
with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)

# Or from URL
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/image.jpg"
                    }
                },
                {"type": "text", "text": "Describe this"}
            ]
        }
    ]
)
```

## Streaming

```python
response = client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a poem"}
    ]
)

# Iterate over events
for text in response.text_stream:
    print(text, end="", flush=True)
```

## System Prompts

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant. Keep responses concise.",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)
```

## Batch API (Asynchronous)

```python
# Process many requests efficiently
requests = [
    {
        "custom_id": "request-1",
        "params": {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": "Say hi"}]
        }
    }
]

batch = client.beta.batch_processing.batches.create(
    requests=requests
)

# Poll for completion
import time
while True:
    batch = client.beta.batch_processing.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(10)

# Get results
for result in client.beta.batch_processing.batches.results(batch.id):
    print(result)
```

## Error Handling

```python
from anthropic import APIError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    print("Rate limited, retry later")
except APIError as e:
    print(f"API error: {e}")
```

## Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model` | Model ID (required) | - |
| `max_tokens` | Max output tokens | - |
| `messages` | Conversation history | - |
| `system` | System instruction | Optional |
| `temperature` | Randomness (0-1) | 1 |
| `top_p` | Diversity (0-1) | 1 |
| `stop_sequences` | Stop generation | Optional |

## Token Counting

```python
import anthropic

response = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "user", "content": "How many tokens?"}
    ]
)

print(f"Input tokens: {response.input_tokens}")
```

## Cost Estimation

```
Claude 3.5 Sonnet:
- Input:  $3 / 1M tokens
- Output: $15 / 1M tokens

Claude 3 Haiku (fast):
- Input:  $0.25 / 1M tokens
- Output: $1.25 / 1M tokens
```

---

**API Reference:** https://docs.anthropic.com/
**Cookbook (Patterns):** See docs/platform-claude/cookbooks.md

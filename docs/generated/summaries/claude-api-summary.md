# Claude API Summary

Optimized for LLM consumption. Essential Claude API concepts for implementation.

## Core Concepts

**Models Available:**
- `claude-opus-4-5-20251101` - Most capable (~200K context)
- `claude-sonnet-4-5-20250929` - Balanced (best for most uses)
- `claude-haiku-4-5-20251001` - Fast and cheap

**Pricing (approx):**
- Sonnet: $3 input / $15 output per 1M tokens
- Haiku: $0.25 input / $1.25 output per 1M tokens

**Context Window:** 200,000 tokens (can process 20K+ word documents)

---

## API Architecture

**Stateless Design:** Each request includes full conversation history. Server doesn't maintain state.

**Message Format:**
```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1024
}
```

**Response:**
```json
{
  "content": [
    {"type": "text", "text": "Response here"}
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 100
  }
}
```

---

## Key Capabilities

### 1. Text Generation
- Summarization, writing, analysis, translation
- Natural language conversations
- Code generation

### 2. Tool Use (Function Calling)
- Define tools (functions) Claude can use
- Claude chooses when/how to use tools
- Useful for: API calls, database queries, external data

**Example:**
```python
tools = [{
    "name": "get_weather",
    "description": "Get weather for location",
    "input_schema": {...}
}]

response = client.messages.create(
    tools=tools,
    messages=[...]
)

if response.stop_reason == "tool_use":
    tool_call = response.content[1]
    # Execute tool_call.input, then continue conversation
```

### 3. Vision (Image Understanding)
- Analyze images (JPEG, PNG, GIF, WebP)
- Describe, OCR, identify objects
- Max 20MB per image

### 4. Streaming
- Real-time token-by-token output
- Better UX for long responses
- Useful for chat applications

### 5. Batch Processing
- Process many requests asynchronously
- Lower cost (50% discount)
- Results within 24 hours

---

## Common Patterns

**Pattern 1: Simple Chat**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.content[0].text)
```

**Pattern 2: Multi-turn Conversation**
```python
messages = [
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "4"},
    {"role": "user", "content": "Double it"}
]
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=messages
)
```

**Pattern 3: System Prompt (Instructions)**
```python
response = client.messages.create(
    system="You are a Python expert.",
    messages=[...],
    model="claude-sonnet-4-5-20250929"
)
```

**Pattern 4: Tool Use**
```python
# Define tools
tools = [{"name": "...", "description": "...", "input_schema": {...}}]

# Request with tools
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    tools=tools,
    messages=[...]
)

# Check if tool was used
if response.stop_reason == "tool_use":
    tool_use = next(
        (block for block in response.content if block.type == "tool_use"),
        None
    )
    result = execute_tool(tool_use.name, tool_use.input)

    # Continue conversation with tool result
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
        ]
    })
```

**Pattern 5: Streaming**
```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    messages=[...]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Pattern 6: Vision**
```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}
            },
            {"type": "text", "text": "What's in this image?"}
        ]
    }]
)
```

---

## Parameters Reference

| Parameter | Type | Purpose | Default |
|-----------|------|---------|---------|
| `model` | string | Model ID | - |
| `messages` | array | Conversation history | - |
| `max_tokens` | int | Max output tokens | - |
| `system` | string | System instruction | Optional |
| `temperature` | float | Randomness (0-1) | 1 |
| `top_p` | float | Diversity (0-1) | 1 |
| `stop_sequences` | array | Stop generation | Optional |
| `tools` | array | Available functions | Optional |

---

## Token Counting

```python
response = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[...]
)
print(f"Tokens: {response.input_tokens}")
```

**Typical Costs:**
- Simple Q&A: 100-500 tokens ($0.003 - $0.015)
- Document analysis: 1K-5K tokens ($0.03 - $0.15)
- Code generation: 500-2K tokens ($0.02 - $0.06)

---

## Error Handling

```python
from anthropic import APIError, RateLimitError, APIStatusError

try:
    response = client.messages.create(...)
except RateLimitError:
    # Retry with exponential backoff
    time.sleep(2 ** retry_count)
except APIStatusError as e:
    # Handle specific HTTP errors
    print(f"Error {e.status_code}: {e.message}")
except APIError as e:
    # Generic API error
    print(f"API Error: {e}")
```

---

## Best Practices

1. **Use appropriate model:** Haiku for simple tasks, Sonnet for balanced, Opus for complex
2. **Set max_tokens:** Prevents runaway costs
3. **Add system prompts:** Shapes Claude's behavior
4. **Handle streaming:** Better UX for long outputs
5. **Use tools for external data:** Don't hardcode API calls in prompts
6. **Cache large documents:** Use prompt caching for cost savings
7. **Batch process:** 50% discount for non-urgent requests

---

## Common Use Cases

- **RAG:** Retrieval-augmented generation (search + Claude)
- **Agents:** Claude with tools making decisions
- **Code review:** Analyze pull requests
- **Content generation:** Write marketing copy, articles
- **Data analysis:** Summarize and extract insights
- **Customer support:** Chatbots and automation

---

## Token Count: ~950 tokens

Used for: Decision trees, implementation guides, pattern selection.

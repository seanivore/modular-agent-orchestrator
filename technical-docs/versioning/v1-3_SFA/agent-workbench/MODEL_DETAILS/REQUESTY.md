# Requesty Models 

They all use the same API key and OpenAI API endpoint. Just indicate what model to use in the request. 
[Documentation](https://docs.requesty.ai/quickstart#using-our-openai-sdk)

## Gemini 2.5 Pro 
- google/gemini-2.5-pro-exp-03-25

Context Window: 1,048,576 tokens
Vision: No
Caching: No
Tools: No
Input Price: $0.00/M 
Output Price: $0.00/M 
Output Max Tokens: 65,536

## Requesty Example (Using Gemini but Swap In Any Other Model)

```python
import os
import openai
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
ROUTER_API_KEY = os.getenv("ROUTER_API_KEY")

if ROUTER_API_KEY is None:
    raise ValueError("ROUTER_API_KEY not found. Please check your .env file.")

try:
    # Initialize OpenAI client
    client = openai.OpenAI(
        api_key=ROUTER_API_KEY,
        base_url="https://router.requesty.ai/v1",
        default_headers={"Authorization": f"Bearer {ROUTER_API_KEY}"}
    )

    # Example request
    response = client.chat.completions.create(
        model="google/gemini-2.5-pro-exp-03-25",
        messages=[{"role": "user", "content": "Hello, who are you?"}]
    )

    # Check if the response is successful
    if not response.choices:
        raise Exception("No response choices found.")

    # Print the result
    print(response.choices[0].message.content)

except openai.OpenAIError as e:
    print(f"OpenAI API error: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## Sonnet 3.7 
- anthropic/claude-3-7-sonnet-latest
- vertex/anthropic/claude-3-7-sonnet-latest
- vertex/anthropic/claude-3-7-sonnet-latest@us-east5

Context Window: 200,000 tokens
Vision: No
Caching: Yes
Tools: Yes
Input Price: $3.00/M 
Output Price: $15.00/M 
Output Max Tokens: 64,000
Output Beta Tokens: 128,000

(Vertex doesn't save your data and use it for training)

```python
    # Example request
    response = client.chat.completions.create(
        model="anthropic/claude-3-7-sonnet-latest",
        messages=[{"role": "user", "content": "Hello, who are you?"}]
    )
```
```python
    # Example request
    response = client.chat.completions.create(
        model="vertex/anthropic/claude-3-7-sonnet",
        messages=[{"role": "user", "content": "Hello, who are you?"}]
    )
```


## GPT 4.1 for Image Generation  
- openai/gpt-4.1-nano
- openai/gpt-4.1-mini

Context Window: 1,047,576 tokens	
Vision: Yes
Nano Input Price: $0.10/M
Nano Output Price: $0.40/M 
Mini Input Price: $0.400/M 
Mini Output Price: $1.600/M 
Image Input Price: $10.00/M 
Image Output Price: $40.00/M 
Image Max Tokens: 32,768

```python
   # Example request
    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=[{"role": "user", "content": "Hello, who are you?"}]
    )
```

```python
   # Example request
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[{"role": "user", "content": "Hello, who are you?"}]
    )
```

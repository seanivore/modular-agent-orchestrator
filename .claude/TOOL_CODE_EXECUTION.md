# **TOOL** Code Execution Tool 

*This feature requires the `anthropic-beta:` `code-execution-2025-05-22` beta header*

- Execute Python code in a secure, sandboxed environment 
- Analyze data, create visualizations, perform complex calculations 
- Process uploaded files directly within the API conversation 

## Supported Models

The code execution tool is available on:

* Claude Opus 4 (`claude-opus-4-20250514`)
* Claude Sonnet 4 (`claude-sonnet-4-20250514`)
* Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`)
* Claude Haiku 3.5 (`claude-3-5-haiku-latest`)

## Quick Start

Here's a simple example that asks Claude to perform a calculation:


```bash 
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: code-execution-2025-05-22" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-20250514",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
            }
        ],
        "tools": [{
            "type": "code_execution_20250522",
            "name": "code_execution"
        }]
    }'
```

```python 
import anthropic

client = anthropic.Anthropic(
    default_headers={
        "anthropic-beta": "code-execution-2025-05-22"
    }
)

response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
    }],
    tools=[{
        "type": "code_execution_20250522",
        "name": "code_execution"
    }]
)

print(response)
```

## Add Code Execution To Your API Request 

1. Claude evaluates whether code execution would help answer your question
2. Claude writes and executes Python code in a secure sandbox environment
3. Code execution may occur multiple times throughout a single request
4. Claude provides results with any generated charts, calculations, or analysis

## Tool Definition; Requires No Additional Parameters 

```json JSON
{
  "type": "code_execution_20250522",
  "name": "code_execution"
}
```

## Response Format Example 

```json
{
  "role": "assistant",
  "container": {
    "id": "container_011CPR5CNjB747bTd36fQLFk",
    "expires_at": "2025-05-23T21:13:31.749448Z"
  },
  "content": [
    {
      "type": "text",
      "text": "I'll calculate the mean and standard deviation for you."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01A2B3C4D5E6F7G8H9I0J1K2",
      "name": "code_execution",
      "input": {
        "code": "import numpy as np\ndata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nmean = np.mean(data)\nstd = np.std(data)\nprint(f\"Mean: {mean}\")\nprint(f\"Standard deviation: {std}\")"
      }
    },
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_01A2B3C4D5E6F7G8H9I0J1K2",
      "content": {
        "type": "code_execution_result",
        "stdout": "Mean: 5.5\nStandard deviation: 2.8722813232690143\n",
        "stderr": "",
        "return_code": 0
      }
    },
    {
      "type": "text",
      "text": "The mean of the dataset is 5.5 and the standard deviation is approximately 2.87."
    }
  ],
  "id": "msg_01BqK2v4FnRs4xTjgL8EuZxz",
  "model": "claude-opus-4-20250514",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 45,
    "output_tokens": 187,
  }
}
```

### Code Execution Results Include 

- `stdout`: Output from print statements and successful execution
- `stderr`: Error messages if code execution fails
- `return_code` (0 for success, non-zero for failure)

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_01ABC123",
  "content": {
    "type": "code_execution_result",
    "stdout": "",
    "stderr": "NameError: name 'undefined_variable' is not defined",
    "return_code": 1
  }
}
```

### Errors Show `code_execution_tool_result_error`

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_01VfmxgZ46TiHbmXgy928hQR",
  "content": {
    "type": "code_execution_tool_result_error",
    "error_code": "unavailable"
  }
}
```

#### Error Handling 

- `unavailable`: The code execution tool is unavailable
- `code_execution_exceeded`: Execution time exceeded the maximum allowed
- `container_expired`: The container is expired and not available

#### `pause_turn` Stop Reason

The response may include a `pause_turn` stop reason, which indicates that the API paused a long-running turn. You may provide the response back as-is in a subsequent request to let Claude continue its turn, or modify the content if you wish to interrupt the conversation.

## Working with Files in Code Execution

*Using the Files API with Code Execution requires two `anthropic-beta`: `code-execution-2025-05-22,files-api-2025-04-14` beta headers*

- Analyze Files API uploads 
- Read, process, generate data insights 
- Pass multiple files per request 

### Supported Python File Types 

- CSV
- Excel (.xlsx, .xls)
- JSON
- XML
- Images (JPEG, PNG, GIF, WebP)
- Text files (.txt, .md, .py, etc)

### Loading File For Execution 

1. **Upload file** using Files API 
2. **Reference file** in message using the `container_upload` content block
3. **Include code execution tool** in your API request

```python 
import anthropic

client = anthropic.Anthropic(
    default_headers={
        "anthropic-beta": "code-execution-2025-05-22,files-api-2025-04-14"
    }
)

# Upload a file
file_object = client.beta.files.upload(
    file=open("data.csv", "rb"),
)

# Use the file_id with code execution
response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this CSV data"},
            {"type": "container_upload", "file_id": file_object.id}
        ]
    }],
    tools=[{
        "type": "code_execution_20250522",
        "name": "code_execution"
    }]
)
```

### Retrieving Executed Files Via Files API 

```python
from anthropic import Anthropic

# Initialize with both beta headers
client = Anthropic(
    default_headers={
        "anthropic-beta": "code-execution-2025-05-22,files-api-2025-04-14"
    }
)

# Request code execution that creates files
response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Create a matplotlib visualization and save it as output.png"
    }],
    tools=[{
        "type": "code_execution_20250522",
        "name": "code_execution"
    }]
)

# Extract file IDs from the response
def extract_file_ids(response):
    file_ids = []
    for item in response.content:
        if item.type == 'code_execution_tool_result':
            content_item = item.content
            if content_item.get('type') == 'code_execution_result':
                for file in content_item.get('content', []):
                    file_ids.append(file['file_id'])
    return file_ids

# Download the created files
for file_id in extract_file_ids(response):
    file_metadata = client.beta.files.retrieve_metadata(file_id)
    file_content = client.beta.files.download(file_id)
    file_content.write_to_file(file_metadata.filename)
    print(f"Downloaded: {file_metadata.filename}")
```  

## Execution In Secure Python-Specific Container Environment 

### Runtime Environment

- **Python version**: 3.11.12
- **Operating system**: Linux-based container
- **Architecture**: x86\_64 (AMD64)

### Resource Limits

- **Memory**: 1GiB RAM
- **Disk space**: 5GiB workspace storage
- **CPU**: 1 CPU

### Networking Security

- **Internet access**: Completely disabled for security
- **External connections**: No outbound network requests permitted
- **Sandbox isolation**: Full isolation from host system and other containers
- **File access**: Limited to workspace directory only
- **Expiration**: Containers expire 1 hour after creation

### Pre-Installed Sandboxed Python Environment Libraries

- **Data Science**: pandas, numpy, scipy, scikit-learn, statsmodels
- **Visualization**: matplotlib, seaborn
- **File Processing**: pyarrow, openpyxl, xlrd, pillow
- **Math & Computing**: sympy, mpmath
- **Utilities**: tqdm, python-dateutil, pytz, joblib

## Multiple API Requests Reuse Container Via ID

*This maintains created files between requests.*

```python
import os
from anthropic import Anthropic

# Initialize the client with beta headers
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    default_headers={
        "anthropic-beta": "code-execution-2025-05-22"
    }
)

# First request: Create a file with a random number
response1 = client.beta.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Write a file with a random number and save it to '/tmp/number.txt'"
    }],
    tools=[{
        "type": "code_execution_20250522",
        "name": "code_execution"
    }]
)

# Extract the container ID from the first response
container_id = response1.container.id

# Second request: Reuse the container to read the file
response2 = client.beta.messages.create(
    container=container_id,  # Reuse the same container
    model="claude-opus-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Read the number from '/tmp/number.txt' and calculate its square"
    }],
    tools=[{
        "type": "code_execution_20250522",
        "name": "code_execution"
    }]
)
```

## Enable Streaming To Receive Code Executions Events As They Occur 

```javascript
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "code_execution"}}

// Code execution streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"code\":\"import pandas as pd\\ndf = pd.read_csv('data.csv')\\nprint(df.head())\"}"}}

// Pause while code executes

// Execution results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "code_execution_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"stdout": "   A  B  C\n0  1  2  3\n1  4  5  6", "stderr": ""}}}
```

## Batch Requests 

- Make Code Execution tool calls through messages Batches API
- Priced the same as regular Messages API requests 

## Usage Pricing 

- Tracked separately from token usage 
- Execution time is a minimum of 5 minutes 
- Files in request means time is billed even if the tool is not used due to files being preloaded to the container 

**Pricing**: \$0.05 per session-hour.


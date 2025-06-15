# **TOOL** Files API Documentation 

*This feature requires the `anthropic-beta:` `files-api-2025-04-14` beta header*

- Upload and manage files to use with the Anthropic API without re-uploading content with each request 
- Useful when using the code execution tool to provide inputs (e.g. datasets and documents) and then download outputs (e.g. charts)
- Prevent having to continually re-upload frequently used documents and images across multiple API calls 

## Simple Create-Once Approach

  - **Upload files** to our secure storage and receive a unique `file_id`
  - **Download files** that are created from the code execution tool
  - **Reference files** in Messages requests using the `file_id` instead of re-uploading content
  - **Manage your files** with list, retrieve, and delete operations

## Upload File 

```python
import anthropic

client = anthropic.Anthropic()
client.beta.files.upload(
  file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
)
``` 

## File In Message Via `file_id`

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please summarize this document for me."
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
                    }
                }
            ]
        }
    ],
    betas=["files-api-2025-04-14"],
)
print(response)
```

## File Types & Content Blocks 

| File Type        | MIME Type                                            | Content Block Type | Use Case                            |
| :--------------- | :--------------------------------------------------- | :----------------- | :---------------------------------- |
| PDF              | `application/pdf`                                    | `document`         | Text analysis, document processing  |
| Plain text       | `text/plain`                                         | `document`         | Text analysis, processing           |
| Images           | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image`            | Image analysis, visual tasks        |
| Datasets, others | Varies                                               | `container_upload` | Analyze data, create visualizations |

### `document` Block

```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
  },
  "title": "Document Title", // Optional
  "context": "Context about the document", // Optional  
  "citations": {"enabled": true} // Optional, enables citations
}
```

### `image` Block

```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w"
  }
}
```

## Managing files

### List files

```python
import anthropic

client = anthropic.Anthropic()
files = client.beta.files.list()
```

### Get Specific File's Metadata 

```python
import anthropic

client = anthropic.Anthropic()
file = client.beta.files.retrieve_metadata("file_011CNha8iCJcU1wXNR6q4V8w")
```

### Delete File From Workspace 

```python 
import anthropic

client = anthropic.Anthropic()
result = client.beta.files.delete("file_011CNha8iCJcU1wXNR6q4V8w")
```

### Downloading Only Files Created By Code Execution Tool 

```python
import anthropic

client = anthropic.Anthropic()
file_content = client.beta.files.download("file_011CNha8iCJcU1wXNR6q4V8w")

# Save to file
with open("downloaded_file.txt", "w") as f:
    f.write(file_content.decode('utf-8'))
```

## Storage & Limits

  - **Maximum file size:** 500 MB per file
  - **Total storage:** 100 GB per organization

- Files live in API key's workspace 
- Other API keys can use files created another API key in same workspace
- Files persist until you delete them
- Deleted files cannot be recovered
- Files are inaccessible via the API shortly after deletion 
- May persist in active `Messages` API calls and associated tool uses after deletion 

## Error handling

  - **File not found (404):** 
    - The specified `file_id` doesn't exist 
    - Or you don't have access to it
  - **Invalid file type (400):** 
    - The file type doesn't match the content block type 
    - E.g., using an image file in a document block
  - **Exceeds context window size (400):** 
    - The file is larger than the context window size 
    - E.g. using a 500 MB plaintext file in a `/v1/messages` request
  - **Invalid filename (400):** 
    - Filename doesn't meet the length requirements (1-255 characters) 
    - Or contains forbidden characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, or unicode characters 0-31)
  - **File too large (413):** File exceeds the 500 MB limit
  - **Storage limit exceeded (403):** Your organization has reached the 100 GB storage limit

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "File not found: file_011CNha8iCJcU1wXNR6q4V8w"
  }
}
```

## Usage and billing

File API operations are **free**:

* Uploading files
* Downloading files
* Listing files
* Getting file metadata
* Deleting files

File content used in `Messages` requests are priced as input tokens. You can only download files created by the code execution tool.
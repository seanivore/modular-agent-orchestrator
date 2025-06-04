# AI Voice Marketing Research Index Generator

## Overview
This workflow automates the process of creating a structured index for AI Voice Marketing research documents. It processes research materials related to Brand AI, voice marketing strategies, personas, and customer types, organizing them into searchable categories for easy client access through their website.

## Workflow Phases

### Task 1: Initial Document Processing
- Reviews initial set of documents from the document list
- Creates preliminary category entries
- Marks processed documents in DOCUMENT_LIST.md

### Task 2: Category Development
- Processes additional documents
- Expands existing categories
- Updates category relationships

### Task 3: Content Organization
- Continues document review
- Refines category structure
- Maintains document tracking

### Task 4: Category Enhancement
- Reviews remaining documents
- Further develops category relationships
- Updates category listings

### Task 5: Final Organization
- Completes document processing
- Finalizes category structure
- Ensures all documents are properly indexed

## Usage

To run the workflow, execute:

```bash
./sfa_agent.py -w index.sh
```

## Input Files
- `INDEX_USE_CASE_DIRECTIONS.md`: Contains workflow directions
- `DOCUMENT_LIST.md`: List of documents to be processed
- `CATEGORY_LISTS.md`: Category structure and relationships

## Expected Outputs

The workflow will update two main files:

1. `DOCUMENT_LIST.md`
   - Tracked documents with completion status
   - Cross-referenced documents

2. `CATEGORY_LISTS.md`
   - Organized category structure
   - Document references within categories
   - Cross-category relationships
   - Searchable index entries

## Location
Working directory: `/Users/seanivore/Development/single-file-agents/use-case/index/`

## Notes
- Uses Anthropic's text editing tool for file modifications
- Maintains document integrity by editing in place
- Creates a progressive, organized index structure
- Designed for easy website integration
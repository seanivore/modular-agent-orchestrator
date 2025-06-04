# Tag Content Workflow

## Overview
This workflow helps prepare markdown files for publishing on a Jekyll-powered GitHub Pages website by automatically adding YAML Front Matter sections. It processes markdown files to include appropriate tags, categories, and content types based on predefined lists.

## What it Does
- Reads markdown files from a specified directory
- Adds YAML Front Matter sections above H1 headings
- Assigns appropriate tags, categories, and content types from provided lists
- Updates files in place without creating new output files
- Processes approximately 60+ files in batches of 5 files per phase

## Phases
The workflow operates in multiple phases, processing 5 files per phase:

1. **Initial Setup Phase**
   - Reads the FRONT_MATTER_TASK.md for instructions
   - Reviews available tags, categories, and content types
   - Identifies first batch of files to process

2. **Processing Phases (Multiple)**
   - Each phase handles 5 files
   - Adds YAML Front Matter to selected files
   - Updates files in place
   - Reviews progress and adjusts workflow as needed

3. **Verification Phase**
   - Confirms all files have been processed
   - Validates Front Matter formatting
   - Updates task tracking document

## Usage

Run the workflow using the Single-File Agent command:

```bash
python sfa_main.py --workflow tag-content
```

## Input/Output

### Inputs
- Source markdown files (approximately 60+ files)
- FRONT_MATTER_TASK.md containing:
  - Task instructions
  - List of files to process
  - Available tags, categories, and content types
  - Example formatting

### Outputs
- Updated markdown files with added YAML Front Matter
- No new files are created
- Updates to the task tracking document in FRONT_MATTER_TASK.md

## Working Directory
```
/Users/seanivore/Development/single-file-agents/use-case/tag-content/
```

## Notes
- Files are processed in batches of 5 to maintain quality control
- The workflow automatically adjusts after each batch
- Original files are modified in place
- Progress is tracked in the task document
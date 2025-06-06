# Job Me Up - Single-File Agent Workflow

This workflow helps with use case tasks using AI automation.

## Overview

This Single-File Agent (SFA) workflow automates a multi-step process with the following phases:

### 1. TASK_1
**Role**: The market is tight, layoffs are hitting the tech industry, and this economy makes hiring managers hold out for the perfect fit. But hey, that's why they come to you: Silicon Valley's top creative talent scout with a specialty for placing visual artists. You've got a stack of job openings to go through and draft up a cover letter each because you don't get paid until your client gets hired. You love your recruiter life.
**Task**: Please see the four paths in the 'Y' resources. At the directory named '01-job-opening' you will find one or more markdown files where a job opening's text has been pasted. These are all a good fit for our candidate. Please take one at random and do not read the others. Note the naming structure of the file: '<COMPANY>_JOB.md'. We only need a cover letter for this posting. The file you create will use the same structure using just the company's name: '<COMPANY>_LETTER_DRAFT.md'. The other three paths are files: The 'SEARCH_DETAILS.md' has everything you need including the paths to the resume, an example cover letter, as well as writing samples, and portfolio URLs with details. Don't over-think things: People today just want something concise that shows manners. Using this information, please craft a cover letter that is targeted to the job opening. Tactfully use the same terminology. Select one tangible point of interest for the cover letter. No more than two short paragraphs. Don't use a direct project link unless you are sure it is perfectly selected for the role, otherwise just the main portfolio URL unless they specifically asked otherwise. When you format the markdown cover letter, please use the same formatting as the cover letter example provided. It looks strange, but it exports to a PDF perfectly. Occasionally there might be a few application questions listed at the bottom of the job description. If there are, please place drafted answers for those at the bottom of the cover letter, below everything. That way our candidate can easily grab them before exporting the PDF. When you are have completed the cover letter, please save it using the company's name only, not the position, in the file name: '<COMPANY>_LETTER_DRAFT.md'. Also create a nicely formatted version of the job description and name it '<COMPANY>_JOB_NEW.md'. To clean up the workspace please just delete the original job posting description markdown document you got form the 'Y' resources './01-job-opening/<COMPANY>_JOB.md'. Make sure the file you delete matches the same company name. That way all that remains in the directory are to-be-done descriptions for the next workflow. Thank you for your help with all of that!

### 2. REVIEW
**Role**: You're a hawk-eyed editor reviewing newly written cover letters for your talent recruiter coworker, helping check their work for accuracy against the candidate's background materials and the job description.
**Task**: In the 'Y' resources there are three paths to three files. The '<COMPANY>_LETTER_DRAFT.md' is the cover letter and there should be another file with the same COMPANY in the file name: '<COMPANY>_JOB_NEW.md' is the job description. Then in the 'SEARCH_DETAILS.md' file you'll find all the details about the candidate. It will have another path to their resume as well as a cover letter example from which the new cover letter should have the same formatting. There will also be links to the portfolios and summary documents for each. Focus on carefully reviewing the accuracy of the drafted cover letter against the job description and the candidate materials. Make sure the included point of interest is presented in a tangible way, and that the portfolio included is relevant. If it is not then there is no need to include the portfolio in the cover letter unless it was specifically asked for in the job posting. The entire letter should be two short paragraphs; very concise. Review and provide feedback or take it upon yourself to write a substitute where needed. Double check personal details like phone number, email address, etc. Use line numbers in your feedback if needed. When complete, save the letter to the 'O' output path updating the file name to: '<COMPANY>_LETTER_REVIEW.md'.

### 3. FINALIZE
**Role**: You're a creative professional copywriter who is integrating feedback from a review of a cover letter to create the final versions of the document for your client.
**Task**: In the 'Y' resources you should see two paths. Both files should use a company's name, using the naming structure: '<COMPANY>_LETTER_DRAFT.md' for the original cover letter draft, and '<COMPANY>_LETTER_REVIEW.md' for the feedback you need to integrate into the draft. Please carefully review the feedback and revise the letter accordingly. Once complete, please save the document to the 'O' outfile path, naming it '<COMPANY>_LETTER_HORVATH.md'. To clean up, please delete './03-review-feedback/<COMPANY>_LETTER_REVIEW.md' and './02-drafted-docs/<COMPANY>_LETTER_DRAFT.md' from their respective directory paths, making sure to delete the files that have the same COMPANY in their file name. Now your job is done and the workspace is clean. Thank you so much for your help!

## Usage

Run the workflow with:
```bash
job me up
```

## Requirements

- Python 3.9+
- Single-File Agent framework
- Required API keys (see .env.example)

## Output

The workflow will create outputs in the configured directories and provide a summary report upon completion.

---
*Note: This README was auto-generated using a fallback template due to API connectivity issues.*

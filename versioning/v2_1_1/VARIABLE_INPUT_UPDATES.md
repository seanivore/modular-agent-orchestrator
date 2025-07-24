# Strategy Review & Branch Decision-Making Implementation 

## Goal

Combine (1) strategy review for optimization, (2) current issues troubleshooting, and (3) implementation of branch decision-making into one update; the solution should make things simpler and allow for more complex workflows. 

## Overview 

1. Review token-count tool [Token Counter Tool](#token-counter-tool)
2. Review sketched branch decision-making workflow. [Decision-Making JSON Object Updates](#decision-making-json-object-updates)
3. Prepare real-life branching workflow example to consider. [WIP Test Cases](#wip-test-cases)

Propose comprehensive solution where, as part of the output tool, Claude must use the token-count tool to ensure the document is under 5k tokens, and then use a decision-making tool to choose between a path to trigger completion of the loop, phase, or workflow. 

## SFA Token Counter Updated 

Removed words. Updated math. Centered bottom. Removed other two lines below that were redundant. Keepin' it simple. 

```bash
             Token Usage    
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Tokens         ┃ Count  ┃ Cost        ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
│ Input          │ 36,861 │ – $0.110583 │
│ Output         │ 6,837  │ – $0.102555 │
│ Cached Savings │ 13,270 │ + $0.035829 │
│ Phase          │ 43,698 │ – $0.177309 │
│ Grand Total    │ 73,346 │ – $0.483731 │
└────────────────┴────────┴─────────────┘
         Phase 4/4 completed
```

## Token Counter Tool

```bash
cd /Users/seanivore/Development/single-file-agents/agent-workbench/TOOL_TOKEN_COUNTER
python3 token_counter_V2.py --text "This is a test message to count tokens"
python3 token_counter_V2.py --file /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/voice-persona-scripts.md
python3 token_counter_V2.py --dir /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/
```

### **TERMINAL OUTPUT THAT DESPERATELY NEEDS YOU TO MAKE IT PRETTY**

```bash
> ~/Dev/single-file-agents/a/TOOL_TOKEN_COUNTER > python3 token_counter_V2.py --dir /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/
Newer token counting approach not available: Messages.count_tokens() got an unexpected keyword argument 'content'
Older token counting approach not available: No module named 'anthropic.tokenizer'
WARNING: Using approximate token counting (fallback method)
Scanning directory: /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/
--------------------------------------------------
Token count for /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/voice-persona-strategy.md: 1021 tokens
✅ voice-persona-strategy.md: 1021 tokens
Token count for /Users/seanivore/Development/voice-mkt-sfa/ai-voice-telemarketing/marketing-findings/persona-with-strategy/voice-persona-scripts.md: 7274 tokens
✅ voice-persona-scripts.md: 7274 tokens

All files are within the recommended token limit.
```

## Decision-Making JSON Object Updates 

Note on variable labels: the 'X_PATH' doesn't need to only have paths, it could have URLs. And then 'Y_PATH' could have the decision options. Should we rename those? I initially had changed ALL of them, but idk I pretty much have these memorized so I don't feel strongly either way except for these "will make things clearer" items. If we change any naming we could also rename 'Z' and 'O' to either be one of the two letters and then 'Z_PATH' or 'O_PATH' accordingly. I guess the only reason I even leave 'Z' as an option is because I feel like there was some kind of conflict with something being called 'O' and 'O_PATH' the one time, but I cannot remember what or where that happened. 

```JSON
{
    "carrots-script.sh": [
        {
        "TASK_1": [
            {
            "S": ["sfa_agent.py"],
            "U": "Description of the agent.",
            "X": "See the resource file named 'DOC_1'. Please review it and complete the requested research at the URL provided. Identify one core tactical approach from each, and then create a simple, easy to read, document. You may do more research if need. If you do, include sources.",
            "X_PATH": [
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS.md",
                "https://github.com/carrots-ai/mcp-get-carrots-fast/"
            ],
            "Y": "When complete, save the document appending 'DRAFT_1' to the end of the file name and then make a decision according to what you believe the document needs most next, before it gets a final review.",
            "Y_PATH": [
                "1. More research",
                "2. More examples",
                "3. Simplify language"
            ],
            "Z": [
                "Detailed Next Steps",
                "Updated Document"
            ],
            "O": [
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_1.md",
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/decision_1.json"
            ]
            }
            ]
        },
        {
        "DECISION_1": [
            {
            "S": ["sfa_agent.py"],
            "U": "Description of research agent.",
            "X": "Check the resources for two files. Review 'decision_1.json' for a description of research to be completed. Detail your findings in 'CARROTS_DRAFT_1.md'.",
            "X_PATH": [
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/decision_1.json",
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_1.md"
            ],
            "Y": "After you are finished, save the document appending 'DRAFT_2' to the end of the file and send it for final review.",
            "Y_PATH": [],
            "Z": "Document prepared for final review",
            "O": "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_2.md"
            }
            ]
        },
        {
        "DECISION_2": [
            {
            "S": ["sfa_agent.py"],
            "U": "Description of research agent.",
            "X": "Check the resources for two files. Review 'decision_2.json' for a description of examples to add to the document 'CARROTS_DRAFT_1.md'.",
            "X_PATH": [
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/decision_2.json",
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_1.md"
            ],
            "Y": "After you are finished, save the document appending 'DRAFT_2' to the end of the file and send it for final review.",
            "Y_PATH": [],
            "Z": "Document prepared for final review",
            "O": "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_2.md"
            }
            ]
        },
        {
        "DECISION_3": [
            {
            "S": ["sfa_agent.py"],
            "U": "Description of research agent.",
            "X": "Check the resources for two files. Review 'decision_3.json' for a description of the major edits the document 'CARROTS_DRAFT_1.md' needs.",
            "X_PATH": [
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/decision_3.json",
                "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_1.md"
            ],
            "Y": "After you are finished, save the document appending 'DRAFT_2' to the end of the file and send it for final review.",
            "Y_PATH": [],
            "Z": "Document prepared for final review",
            "O": "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_2.md"
            }
            ]
        },
        {
        "REVIEW_TASK": [
            {
            "S": ["sfa_agent.py"],
            "U": "Description of research agent.",
            "X": "At the 'X_PATH' find 'CARROTS_DRAFT_2.md'. Review the document for accuracy and completeness.",
            "X_PATH": ["/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_DRAFT_2.md"],
            "Y": "After you are finished, save the document appending 'FINAL' to the end of the file and send it for final review.",
            "Y_PATH": [],
            "Z": "Final document",
            "O": "/Users/seanivore/Development/single-file-agents/use-case/carrots/CARROTS_FINAL.md"
            }
            ]
        }
    ],  
        "A": "best doc update",
        "F": "User/seanivore/Development/single-file-agents/use-case/best-doc-update/"
}
```

### Create a new phase resolution system: 

```bash
   # Example pseudocode for the bash script
   DECISION=$(cat $PREVIOUS_OUTPUT | jq .decision)
   
   if [ "$DECISION" == "1" ]; then
     # Run revision branch
     python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 1
   elif [ "$DECISION" == "2" ]; then
     # Run publishing branch
     python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 2
   fi
```

## Hard-Coded Information 

When figuring out the updated JSON, look at a solid one — try `/Users/seanivore/Development/single-file-agents/use-case/research-combine-report/research-combine-report-config.json` — and Sean will identify things that might make more sense to move to the directions inside the agent's python script. Obviously we started with as close to nothing in that script as possible but there are a few things that are getting repetitive. 

No tables should ever be used. Note about max length. 

Please don't waste tokens and loops reading files that are not needed & use `read_multiple_files` whenever possible.

Use `search_files` tool very rarely. Consider the following: If there is a typo in the file name, you will likely be able to find the correct file just by intuiting what of the other files in that directory has a file name that is similar. Do not assume the file is in the wrong directory; this happens very rarely because a file name type is small and harder to catch, but an incorrect path in a task workflow is huge and almost guaranteed to be caught before running the workflow.

### Considerations 

In there a way to have an internal hard-coded note about missing content when working on a subsequent phase or reviewing? It would be cool if we could use make_decision so Claude could pick up the other AI's mistake/slack and create the missing work on the fly? It is kind of silly to mention "only 1 of the three social media posts were created". If it is possible, we can do it in a way that let's Claude use their best judgement when creating the missing work, in case it is a situation where they don't have the same resources as the other AI. 

## WIP Test Cases 

There are just thing I'm working on still with the research for Cliff about the AI Voice Telemarketing strategies and a client in the Home Service industry. I'm including them here — along with a few other to-be-completed below this — for when we need test cases to build. I'll just have to grab paths and such. 

FIND THEM HERE: `/Users/seanivore/Development/single-file-agents/agent-workbench/BUILD_UPDATES.md`


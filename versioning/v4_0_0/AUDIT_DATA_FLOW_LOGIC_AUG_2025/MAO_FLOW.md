# Flow of Data Through Mao 

## Overview 

- The docs all say that the flow is this: 

"User Goal" --> "Conversation Bridge" --> "Natural Language Processing" --> "Core" --> "JSON Workflow Creation" --> "Model Selection" --> "Execution" --> "Results" --> "Caching"

- But to really clean up the hardcoded categories in the code, I need to better understand what is actually happening and where 
- So I'm going to write it out in normal language that includes what information is conveyed and where 

IMO, this feels very overly complex. The workflow JSON is just simple variables which are just parts of a prompt request. 

### Goal 

The `core.py` file is where we started and we found so many categories. They hardcoded them as "suggestions" for the AI but the AI does not need suggestions. We went to `conversation_bridge.py` and found the same grouping. 

Once we understand what the logic should be, and what the file's current logic is, then we can clean up all the files in the flow. 

### Deliverable

**AI knows the variables. They are able to have a conversation with the user and fill in the blanks. We do not want anything more complicated than that. The only categorical grouping we want is for analytics. NO SUGGESTIONS. We also need to be aware of launching multi-lingual; none of these prefabs would make any sense in a multi-lingual environment.**

The secondary benefit of doing this is that we'll have a really nice diagram. 

## 1. The Chat 
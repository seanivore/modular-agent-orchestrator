Find updates at Mao-v4 Documentation Batch Groupings in the Memory MCP. 

Entire codebase is added to Project Knowledge. 

My desperate and slowly fading attempts at fixing documentation: 

documentation/doc_prep_guide.md 

I think you'll want to have a good think and look it over to help me make a POA. There are a lot of resources so I think they'll have to be taken in phases. Here are my thoughts. 

Phase 1: 

Start by focusing on the text only. Tell the story and use 03_USER_FLOW.md as inspiration and a guide. Be comprehensive. Do not use m-dashes, emojis, and this should be primarily sentence form. The Anthropic docs are 60-80% text, but only 10-30% bullet points. Note that the way AI writes bullet points is TOO PERFECT to the point of them not being very helpful to read through as a human -- you all always make them exactly the same length, like 3 words, and it looks pretty but isn't helpful that way. Also if you did look at the Anthropic docs you'd see that they don't use bullet points like that either, they use it as a way to group information, not tell a story as LLMs seem to. PLEASE REMEMBER THESE GUIDELINES. Also do not directly delete my writing -- just indicate how you'd like to edit things, please. Hopefully my writing will give you a good head start on this phase. 

Phase 1 Flow -- 

Look to #2 for help here, and also #11. First I'd recommend deciding on the number of and name of files -- when changing that note that they all have contents pasted in them to be condensed and made into documentation info. 

Then #1 here. Which I think should be the next step, going in the order listed in the prep guide by starting with 03_USER_FLOW.md and the other few "main architecture" files. 

Then #3 here. Then the ending files to wrap up loose ends. 

Then #4 here. Only after that would I say it is time to write the first three. I'm not even sure we'll really have those perfected until the very end. 

Once those are cleaned up I'd like to review. 

Phase 2: 

After we have written docs with spaces for code architecture, I would recommend only going through these batch by batch. Taking the code you find and other helpful info, and placing it into the documentation. 

Look to #6 and #8 first -- they should be the most helpful. 

Scan through #9 -- I saw a dependency matrix and a UI integration map for sure but probably other gems. 

Scan through #10 -- make sure we have all that these implementation required included. 

All that remains is #7 -- details for every single page. I'm not sure how to handle these but I sort of think it might be worth going through them by group for sure. 

With those resources you should be able to find and integrate a lot of code snippets and architecture section into the cleaned up written part. 

Obviously a good point for me to review again. 

Phase 3: 

I think then we just need to decide if anything is missing. 

Also revisit #3 and #4. 

Then we need to focus on visual aids. I have the following from my list of intriguing  visuals. 

- Tool architecture diagrams
- Extension ecosystem map
- System architecture diagrams (Mermaid)
- Data flow visualizations
- Integration touchpoint maps
- Performance metrics dashboards
- Security and privacy flow charts
- User journey flow diagram
- Scalability demonstration charts
- Orchestrator communication flow diagram showing component information passing
- Cross-session state management showing memory state persistence flow
- Tool integration data exchange flow chart showing how 'button snippets' are created and used
- Flow chart showing analytics trigger points and data flow 

Phase 4: 

Lastly I'm curious about ways to check things. Might we be able to create a script that checks if the code snippets (particularly from CC) in the doc are the same as in the codebase? And then any other scripts that would help us review them? 

Publish. I have a directory set up to publish already but the Jekyll theme needs adjusting before we can share and celebrate. 
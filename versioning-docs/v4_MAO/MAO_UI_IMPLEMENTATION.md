# Mao Application UI/UX Design  

## Where We Are At 

  1. We learned Claude Code used TypeScript and Node.js to create their beautiful terminal application UI. 
  2. Then we created a SPEC.md document to execute and have Claude Code build the UI foundation, and never got around to it. 
  3. Yesterday we spent the past 30 hours finishing up auditing and almost all of the remaining code implementation. 
  4. After that, I asked AI to see if SPEC.md needed an update based that implementation; it turned out very meh.
  5. Around the same time we created a `./typescript-terminal-playground/` and played around with some characters. Nothing too deep yet. 
  6. Most importantly, I analyzed Claude Code's typography because it is so intentional and psychological; lots of good info. 
  7. Also, I think we need really clear copywriting protocol guidelines to be able to use the helpful `ui_terminal.py` information. 

### What We Need To Do 

  - It is time to take in all of this information 
  - Review all of the documents 
  - Double check the new technical documentation additions 
  - Study our beautiful visual brand identify document 
  - Have a good think about it all 
  - Oh and also review the `memory` MCP server project state updates tagged with 'Mao-v4'

With all of that information and progress, I'm pretty excited that the results are going to be way better than the SPEC.md that we never even got around to executing. Can't wait for you to see the visual brand identify information, it is some serious detective work, and genius on their part. 

### Our Output  
  
  1. A new, better than ever, and more complete `mao_ui_terminal_spec.md` that we can execute in Claude Code to build the strongest, most solid and thought out UI foundation possible. 
  2. And then a document that walks me through any prep. work to do before running the SPEC, and then details regarding `MAO_UI_TERMINAL_IMPLEMENTATION.md` in terms of things that need to be done that are unrelated to the UI Foundation being created, as well as what our first steps should be once the UI Foundation is created. 

### File Clean Up 

Then I'm going to delete all of these other files that are no longer needed. We'll only have one other, this our third important file, `6_MAO_VISUAL_IDENTITY.md`, though we may want to reconsider if it actually needs to be in the technical documentation as it is now. Oh, though I guess it should be because eventually we'll want to use it to create a web and then mobile UI as well. 

## Context Priming 

I mentioned having a good think already, but I'll lay out context and then our documents to review in order from this point. 

  1. Check out the project state updates tagged with `Mao-v4` in our `memory` MCP server tool to get a sense of the project state. 
  2. Explore the technical documentation to see if there is anything in there related to our UI task's at hand that might not be on our radar. 
  3. We should also make notes of what of our task at hand needs to be added to those same technical documentation files. 

   - `./versioning-docs/technical-documentation/0_TECH_DOC_CONTENTS.md`
   - `./versioning-docs/technical-documentation/1_MAO_OVERVIEW.md`
   - `./versioning-docs/technical-documentation/2_MAO_SYSTEM_FILES.md`
   - `./versioning-docs/technical-documentation/3_MAO_ARCHITECTURE.md`
   - `./versioning-docs/technical-documentation/4_MAO_EXTENSION_GUIDE.md`
   - `./versioning-docs/technical-documentation/5_MAO_PROTECTION_RULES.md`
   - `./versioning-docs/technical-documentation/7_MAO_USER_GUIDE.md`

## Our Documents 

1. `./versioning-docs/technical-documentation/6_MAO_VISUAL_IDENTITY.md` <-- Brilliant 
2. `./versioning-docs/v4_MAO/ORIGINAL_UI_SPEC_GUIDE.md` <-- Given to me to work through when executing the SPEC 
   - `./interfaces/terminal/` <-- First few files it required we have prepared
   - `./interfaces/ui_terminal.py` <-- The original UI files 
3. `./versioning-docs/v4_MAO/UI_TERMINAL_NOTES.md` <-- Collection of all implementation details for UI documents 
4. Compare and contrast the next two SPEC documents 
   - `./versioning-docs/v4_MAO/mao_ui_spec_v1.md` <-- I *think* this is the original SPEC 
   - `./versioning-docs/v4_MAO/mao_ui_spec_v2.md` <-- Because this one seems to lose the structure a bit 
5. `./typescript-terminal-playground/` <-- Playground directory of files 

## Next Steps 

That was a lot of information! Thankful for the rad GitHub integration putting the entire codebase in our Project Knowledge Base files for you to review them that way. 

When we create the next files, please create them as artifacts to save on tokens. Then tell me if you have a filename and location you'd like me to use when I copy them over. 

### Copywriting Guidelines 

First and foremost, as it seems like we'll want it to be part of the SPEC, we need to figure out how we want to communicate how the `ui_terminal.py` file is going to be used to inform the actual UI information that needs to be created. Obviously we'll want them to create that in a new file so we can keep the original `ui_terminal.py` file as a reference. Better yet, if they can somehow use the `ui_terminal.py` in a modular way to inform their work, it would allow for easy updates. Like perhaps if there was a "translation" explainer we proposed. And then that would be used for each thing in that file. Meaning in the future if there is new information from new tools, etc. it can be added to the `ui_terminal.py` file, and then, while it isn't "plug-and-play", use that to inform the final UI copywriting file. 

Those are my thoughts! LMK what you think. 

### UI Foundation SPEC 

- Once we have a decision for how to handle the copywriting, please write a new SPEC document. 
- I have placed some of the best SPEC documents as templates in our ai_docs directory in this repo. Check them out. 
  - `./.claude/ai-docs/SPEC_TEMPLATES/ui_component_spec.md`
  - `./.claude/ai-docs/SPEC_TEMPLATES/workflow_ios_spec.md`
  - Those are my two favorites, but there are two more in there if you wanted. 

### Comprehensive Implementation Guide 

- After that we should be breezing right through the rest of this. Please create for us a new implementation guide. 
  - Anything that needs to be done before running the SPEC 
  - Anything that needs to be done or added to the codebase 
  - What the next steps are after the SPEC creates our UI Foundation 
- Please do not put any timelines or estimates in the document, and go easy on the emojis and fancy stuff in the formatting. It makes my ADHD brain have trouble reading it at times. 

- That reminds me I added a fun new rule: 
  - It is 'Mao' not 'MAO' (this encourages proper pronunciation)
  - Don't use m-dashes; use semicolons (it is how people recognize AI writing)
  - We don't use emojis in UI; not a huge fan of them in docs but eh 
  - Don't put a header in bold in the docs; save that for non-header text that needs to be seen 

### Visual Brand Identity 

Finally, while nothing necessarily needs to be done here, it also seems like after all of this work we might be able to flesh out the visuals even more than we already have. FYC! (FYC = For Your Consideration) 
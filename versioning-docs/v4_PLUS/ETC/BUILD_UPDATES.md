# Build Updates

## Fist Save On Tokens 

1. Content fingerprinting and better caching for reference materials
2. previous conversation pruning attempt went too far - we'll need to find the right balance where context is preserved within phases but not unnecessarily carried between them

### Other Token Saving Ideas 

1. **Model Delegation Strategy**: Use Haiku or Gemini for specific phases (like integrating feedback) to reduce Claude costs

2. **More Aggressive Caching**:
   - Cache job descriptions once read
   - Cache any reference materials
   - Store "decisions" in a cache so they don't have to be re-analyzed
   - Add content fingerprinting to detect when files haven't actually changed

3. **LiteLLM Integration**: Great idea to enable multi-model routing based on task type

4. **Workflow Optimizations**:
   - Split phases more intelligently (research → draft → refine)
   - Use tools that summarize content before sending to Claude
   - Prune conversation history more aggressively during long interactions

5. **Hybrid Approach**: 
   - Use Claude for creative work and complex thinking
   - Use cheaper models for integration/implementation tasks
   - Potentially use OpenAI or Gemini where they perform well at lower cost


## Tooling 

### Media Processing Tools (right up your alley as a designer! 🎨):
- Image optimization and resizing tools
- Design asset metadata managers

- Color palette extractors
- SVG manipulation tools
- Font analyzers

### Development Tools (for the coding side 💻):
- Git operation helpers (commit, branch, merge)
- Code quality checkers
- Documentation generators
- Dependency analyzers
- Test generators

### Project Management Tools (for keeping things organized 📊):
- Task trackers and updaters (like your task_reporting tool!)
- Time tracking tools
- Resource usage monitors
- Progress visualizers
- Team communication helpers

### Data Processing Tools (for handling information 📈):
- CSV/JSON/XML parsers
- Data validators
- Format converters
- Data visualization generators
- Analytics reporters

### AI/ML Integration Tools (the fun experimental stuff! 🤖):
- Model performance monitors
- Prompt template managers
- Training data processors
- Output validators
- Chain-of-thought analyzers

## Agent Feature Updates

### Messaging, Communication, and Collaboration 

Next update I'd like to focus on being able to pull in other agents to work in parallel or with each other in sync. 

I pasted a bit of python from OpenAI below, but then I found this LiteLLM docs and omg you can either use the SDK to put the tool to call HUNDREDS of other models from our python code. Or, as I would eventually like to find a company to stay with that offers paid API with lots of models, and I signed up and put $25 or so in Requesty, but I've yet to see anything about it being as powerful as this LiteLLM tool, you can use them as the central service. 

https://docs.litellm.ai/ 

I even looked at their pricing for Gemini 2.5 Pro and it was free. 1M token input window is crazy. I'm starting to realize that Anthropic is the only one not lowering prices and things like indexing our SFA research documents cost almost $5 and they only did FIVE OF 60 DOCUMENTS. Crazy. 

Ideally we'll create something with . 

Here is another . There is a  and they provide deep feedback for serious business decisions and strategy. It's created by the original creator of the basic SFA, IndyDevDan, and is open source. 



Just Prompt `` 

I also want to think about them being able to chat each other but also ME while working in a flow. 


### Youtube Transcript Downloader 

Youtube Transcript Downloader for when they do a search and videos come up in the results. Build into the hardcoded directions to output the transcript using a super-brief [SEARCH_QUERY]_VIDEO.md at the Downloads folder. 

## Use-Cases 

### New Use-Cases to Build  

- Research Micro-grants: https://github.com/nayafia/microgrants
- Research all other grants 

### Build to Fix 

Using a document of documentation feedback and another of best-practices for technical documentation, we need our $CLAUD documentation to be updated. The feedback and the best-practices are composed of a list of items that need to be added or need to be improved. Because documentation is very large the flow has been an issue to run thus far. 

Use-case [doc-write-best](../use-case/doc-write-best/)

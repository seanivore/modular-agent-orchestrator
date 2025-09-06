
## 9. Improving Mao Agents' UI and UX, Improves Human UX 

### Core Objectives 

  1. Illustrate strategic elimination of logistical decision making tools for agents 
  2. Achieving 100% Cross Compatibility of Models and Providers by Sidestepping SDK 
  3. Providing Mao agents with the same conveniences humans are used to 

### Complete Removal of Agent in Facilitating Workflow 

* **In previous agentic app builds the agents helped keep the workflow moving**

  - Agents were strangely resistant to helping; refused to use a 'task complete' tool 
  - Stricter language got fewer successful workflows; slightly better when we acted like it was a favor for us 
  - We added logic to end phase when deliverables were saved; suddenly we had token overage and the ignored errors 
  - Then we formalized things; only able to exit by altering workflow 
    - Count your deliverable tokens and save it, or edit it if it is too long, or keep working if they wanted 
    - We thought 'gracious worked, so maybe more respect via control will work'; then they would not count tokens 

* **Today's agent philosophy is NO THINKING about anything other than the task** 

  1. All 'logistical' tools were removed 
  2. We create a write_file tool that auto-saves as they work 
  3. The token counter is live as they work in the file 
  4. There is no other action; to finish they must hand off DIRECTLY to Mao 

  - As a result, by design, the same simple parts of their task that they *would* do previously, is now the only thing they can do 
  - It is magically and shifts all decisions about creating truly dynamic workflows is in Mao's digital hands 

* **Simplifying tools doubled as a way to create 100% cross compatibility** 

  1. When Mao plans a workflow, the necessary tools are identified and intention defined 
  2. Mao then creates a "human button" or rather, just a code snippet for tool operation 
  3. They get another snippet button to call Mao to hand in their deliverable 

  - This results in *COMPLETELY* sidestepping any use of other model or provider's SDK 
  - The modular build is completely versatile 
  - When a new model comes out 
    - Ask Mao to create a small JSON object and file it away 
    - It is instantly available for you in the app 

  - Now, this is how all of our modular configuration files work 
    - You "plug-and-play" or perhaps "drop-in-file" for instant access 
    - In addition to models, this is for tools, providers, CLI commands, memories you create for Mao, your User preferences 
    - Even analytics and app settings are set up this way 

  - Hopefully this illustrates just how powerful Mao App is when it comes to longevity and versatility 
  - In designing the app, we completely avoided all of the parts of the AI industry that are constantly changing 
  - Instead we made those variables actual variables you change like plugging in a Nintendo cartridge, without the blowing 

### The Result of Allowing Agents Nothing But the Task in their Context 

* **Executed agents are provided details of their task**

  - This includes the goal, directions, deliverable, resources, and tools 
    - Their context window contains no other information except for what we need them to do, ensuring higher fidelity results 
    - The use code snippets to use the tools, and when done, they use one to call Mao in 

* **Then they meet Mao directly to hand over their assets so that Mao can save them in the *FREE TO USE* Files API**
  
  - Mao then assesses the work, decides what the next phase of the dynamic workflow will be
    - This creates a much more *natural creative process* more akin to how a human works through a project 
    - It allows space for changing minds, following a new idea, and thus, is a stronger process for *producing innovative work* 

# Storytelling Mao's Value

Illustrating the values and principles learned, leading into the success story.

## Goals 

- Show values by telling the brand story 
- Explain the technical architecture at multiple levels 
- Structure the documentation so that it is similar to the actual user journey 

## AI Industry's Non-Negotiables Obstacles (Problem)

* The industry will not stop changing
  - Who is the AI; models, their abilities, limitations, pricing, etc. 
  - Who gives you AI access; providers, cloud, self-hosted, etc. 
  - What AI can do; skills, tools, intelligence, reasoning ability, decision making, etc. 
  - How do you interact with AI; prompting, prompt strategy, phrasing, context, memory, etc. 
  - Medium to collaborate with AI; app, CLI, API, built-in commands, settings, etc.  
  - Data needed about AI; behavior, performance, accuracy, etc. 
* Don't build what AI will end up evolving into 
* Stop thinking about applications, programming, even code, in the old way 

## Accepting Those Absolutes & Moving On (Solution)

### 1. Evergreen Value 

* Explain the solution 
  - Our philosophy of modularity 
  - The strict, variable-based, never hardcoding, rules 
  - Recognizing that you have to design UI for both the user and the AI 

### 2. Story Arc of Where Mao Came From 

* Needed a code solution to replace the many Make (Integromat) scenario automations 
  - Published website with 200+ weekly blogs; API video shorts; two podcasts before Google's Notebook tool  
  - Learned from IndyDevDan's YouTube about building 'Single File Agents' using UV Astrum Python 
  - Sent Claude the transcript and was like, what is this? We had only made a couple MCPs and one HTML/CSS/JS website 

* Created SFAs that were specialized for specific tasks 
  - Required a lot of planning 
  - Took too much time; didn't make logical sense in the context of the industry changing 

* Implemented "Variable-Input" SFA 
  - Spread the task, or prompt, across values of variables in a JSON object
  - "Agent" SFA file was completely generic with no hardcoding; hard to get AI to do, needed lots of rules early 
  - A setup script executed with the SFA and the JSON object creates specific use case scripts on the fly 
  - Each use-case got a custom command to run in terminal 
  - Made over 50+ different use-cases 
  - Some I updated the JSON variables frequently and then kept running the command 
  - EXAMPLE: 
    1. Put MD document of Job Opening in directory 
    2. Another directory had resume, writing samples, summary of portfolio entries, impressive metrics, preferences 
    3. SFA had a phase that would write a targeted cover letter and targeted resume 
    4. Secondary phase critiqued and reviewed for accuracy 
    5. Final phase feedback was implemented 
    6. The result was applying to hundreds of jobs a week with great resumes 
  - EXAMPLE: `https://presenting.august.style/`
    1. Professional connection had a client needing Voice Agents for new-age telemarketing 
    2. SFA had first phase that did a bunch of research in various ways, asked Perplexity 
    3. Specifically researched how the app they use does voice modulation because all the research was hard data about it 
    4. Second phase focused on pulling out the core strategies  
    5. Next phase made it tangible by creating an archetypal persona that fit the strategy 
    6. Next phase created script and used the apps notation for voice modulation; created a "cheat sheet" 
    7. Review phases 
    8. Final feedback implementation phase 
  - EXAMPLE: `https://presenting.august.style/` 
    1. Quick Google found list of one paragraph "Brand Identity" for semi-known brands 
    2. Phase one created addmittedly surprisingly robust month long marketing plan 
    3. Phase wrote corporate emails, provided tips 
    4. Phase wrote captions and vividly described Instagram posts 
    5. Review phases, and implemented feedback 

* Variable-Everything Realization 
  - SFA got SUPER BLOATED and one day a resume cost a few dollars to create 
  - I wanted to use a free Google LLM instead 
  - It clicked "wait, technically the model is hardcoded" 
  - The same day Anthropic happened to release Claude Sonnet 4

* Introducing The Orchestrator 
  - Played around with SDK translating for one build
  - Forgot to have it parse the API responses 
  - I literally said "I fully do not understand why we can't just literally code a button that the agent just pushes to use a tool, the same as a human button" 
  - Claude paused, considered it, then realized the new "Code Execution" Sonnet 4 tool could do exactly that
  - Officially eliminating SDKs opened the door and we started adding Features
  - No feature would be added in a way that wasn't a config collection of JSON objects, one for each 'setting' 
  - Throughout the entire build, up to the day before the final codebase audit, we kept randomly making new JSON object collections 

* Mao was Born 3 June 2025 
  - We very quickly realized that, the more we made the "MAO" or Modular Agent Orchestrator able to do more complex tasks, THE EASIER IT GOT FROM A UI/UX POV 
  - That moment was like "okay, this is literally art, it is taking something and turning it into something completely different" and "there is something here; we have something here" 

* Accepting Those Absolutes 
  - Suddenly it was possible to not just accept the industry's non-negotiables, but to use them to our advantage 
  - We build so that you just drop in X, Y, Z file and the new model or tool or provider or command or setting JUST WORKS 
  - New codebase was audited many times, many rules were written 

* 4 Weeks Later, We Had 95%+ Compliance

### 3. Record Breaking Development Speed TIME SAVING ANALYSIS 

* Solo Development (Just You)
  - Estimated Time: 3-4 weeks (120-160 hours)
  - Why: Manual analysis, file-by-file fixes, testing, documentation
  - Challenges: Fatigue, inconsistency, missing edge cases
  - Risk: High chance of breaking changes

* Claude in OS App
  - Estimated Time: 2-3 weeks (80-120 hours)
  - Why: No file system access, constant copy/paste, context limits
  - Challenges: Manual file management, session breaks, no coordination
  - Risk: Inconsistent patterns across files

* Just Cursor in IDE
  - Estimated Time: 1-2 weeks (40-80 hours)
  - Why: Good at code changes but no systematic approach
  - Challenges: No master planning, limited scope visibility
  - Risk: Piecemeal fixes without comprehensive strategy

* Our Coordinated Approach
  - Actual Time: 4 hours (!!!)
  - Why: Systematic batching + human-AI coordination + parallel processing
  - Advantages: Master planning, parallel execution, session recovery
  - Result: 95%+ compliance with ZERO breaking changes

* THE MULTIPLIER EFFECT
  - You saved approximately 20-40X the time!
  
* WHAT MADE THIS SO POWERFUL
  - The Secret Sauce:

    1. Systematic batching - 24 organized chunks instead of chaos
    2. Human-AI coordination - Each team played to their strengths
    3. Parallel processing - Multiple batches running simultaneously
    4. Claude Code's superpowers - File system access + tool usage
    5. Session recovery - Memory MCP keeping everything connected
    6. Master planning - Strategy before execution 

* You didn't just use AI - you ORCHESTRATED AI!
* This is exactly what Modular Agent Orchestrator is designed to enable - and you just proved it works at enterprise scale!

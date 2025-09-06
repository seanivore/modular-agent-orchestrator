# Final Implementation Plan Creation 

## Process 

  1. Review each individually first 
     - Address any comments or questions 
     - IMPL PLANS must be robust enough to become technical documentation upon completion 
  2. Then update this file 
     - Make it into ONE complete implementation plan for all items 
     - This is all that needs to be done to launch; all that needs to be tested to launch 
  3. Keep track of implementation that requires other files updates 
     - Things that are tangentially related 
     - For example: 
       - The Model/Provider JSON configs 
       - The collection of workflow JSON 
       - The "how to add X config" section in the AI DEV FILE INDEX: `documentation/10_AI_DEV_INDEX.md`
       - The file index with all new files, classes, functions, normal language explanations 
  4. Create actual web app UI implementation plan 
     - Must consider some of the web elements included in the above combined implementation plan 
     - Must consider how the UI "print" statements are actually handled (mentioned below)

### Old UI Plan If Needed 

  - Regarding any questions about implementation beyond UI 
    - We had a comprehensive IMPL plan for the terminal UI that can be referenced 
  - **ONLY REFERENCE THESE IF YOU NEED**, ignore everything about UI in them
    - `versioning/v4_0_0/IMPL_DEV_LIVE/COMPREHENSIVE_IMPLEMENTATION_ROADMAP.md`
    - `versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_MULTILINGUAL_UI.md`
    - `versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_SUBSCRIPTION_SYSTEM.md`

---

## Implementation Plans 

### 1. Multilingual Support 

* **Make sure things are fully set up to be multi-lingual** 

  - During the LOGIC AUDIT the AI knew that there would be an multilingual launch 
    - They edited terminology accordingly 
    - I'm not sure how far beyond they went 

* **The goal is that the rest of the development will happen along side this, rather than doubling back** 

  - ANTHROPIC DOCUMENTATION: `versioning/v4_1_0/IMPL_MULTILINGUAL/TOOL_MULTILINGUAL.md`
  - IMPL DRAFT: `versioning/v4_1_0/IMPL_MULTILINGUAL/IMPL_MULTILINGUAL.md` 

### 2. Claude Code & Option to Choose Mao Model 

* **Choosing Mao Model requires other functionality updates** 

  - Application settings: `configs/settings...` need an option that defaults to "sonnet-latest" 
  - We need implemented somewhere that terms like "sonnet-latest" and "opus-latest" will work for longevity smooth UX 
  - Model *when used by* provider settings: `configs/connections/providers_x_models.json` 

* **The goal is that User can build coding project workflows** 

  - Including creating one if WE are trying to make actual changes to the application 
  - We need some kind of admin. permissions system for functionality like this 
  - Users would use it for their project, or if they want to add new configs, create new tools, etc. 

* **Claude Code IMPL PLAN draft needs choose model functionality creation added** 

  - ANTHROPIC CLAUDE CODE SDK (updated 6 SEPTEMBER 2025): `versioning/v4_1_0/IMPL_CLAUDE_CODE/CLAUDE_CODE_SDK.md` 
  - IMPL DRAFT: `versioning/v4_1_0/IMPL_CLAUDE_CODE/IMPL_CLAUDE_CODE.md` 

### 3. Rest of Parallel Agent Execution Implementation 

* **This is another that some elements were added in during LOGIC AUDIT** 

  - Not everything was done; no setup script update if it is needed; also JSONs in template folder: `configs/workflows/json_object_templates`
  - We will need to add this JSON to any touch-point orchestration workflow creation files 

* **Implementation draft plan should be relatively complete** 

  - IMPL DRAFT: `versioning/v4_0_0/IMPL_PARALLEL_AGENTS/IMPL_PARALLEL_AGENTS.md` 

### 4. Completed Integration of Scheduled Workflows 

* **This is another that some elements were added in during LOGIC AUDIT** 

  - Not everything was done; no setup script for example 
  - This also requires an update to the setup script logic for NORMAL workflows; these notes are added to the top of the draft plan 

* **Implementation plan is otherwise relatively complete, but also needs the script for checking schedule** 

  - IMPL DRAFT: `versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md` 
  - TIMER ARCHITECTURE DRAFT: `versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/timer_architecture.md` 

* **Actual implementation plans to organize and consolidate** 

### 5. Required Update to Collection of Analytics Plan 

* **This was created for terminal apps that were going to be local, but now we're doing web app** 

  - Not sure what exactly is needed instead, but some kind of cloud server maybe? 
  - We will also add creating and setting up our databases to this part of the plans 

* **We also need a way for Mao, Users (selectively), and Us (admin permissions needed) can see in-app** 

  - Mao needs it for the triggered intelligence workflows 
  - Mao needs to be able to look at all the analytics to be able to see where to make any improvements on their own 
  - Probably don't want users to have all access 
  - Probably should include a setting for Users to delete their User data included into this implementation plan 

* **One of these might be dated; and remember we'll need databases for other use-cases that can be set up now, too** 

  - IMPL DRAFT: `versioning/v4_1_0/IMPL_ANALYTICS/IMPL_ANALYTICS_ACCESSIBILITY.md` 
  - Analytics IMPL DRAFT #2: `versioning/v4_1_0/IMPL_ANALYTICS/MULTI_INSTANCE_DATA.md` 
  - DATABASES IMPL DRAFT: `versioning/v4_1_0/IMPL_DATABASES/IMPL_DATABASES.md` 

### 6. Website Functionality & UI 

* **We probably want to start some of the website parts that we want to test, but make the UI build a new, separate plan** 

  - STOREFRONT IMPL DRAFT: `versioning/v4_1_0/IMPL_WEBSITE/IMPL_WEBSITE_STOREFRONT.md` 
  - SECURE LOGIN IMPL DRAFT: `versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` 
  - SUBSCRIPTION SYSTEM IMPL DRAFT: `versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_SUBSCRIPTION_SYSTEM.md` 

* **To be created is the actual Web Application Implementation Plan** 

  - DIRECTORY LOCATION (NO FILE YET): `versioning/v4_1_0/IMPL_WEB_UI` 

* **NOTE: Conversation required for the UI files distributed throughout our codebase for most every file**

  - Review files and consider our copywriting strategy; compare it to what the UI copy looks like in `MAO_FLOW.md` 
  - In the UI section below we discuss how AI will be writing and very frequently updating the UI
  - I do think it is worth considering if we might want to actually task Haiku 3.5 with this 

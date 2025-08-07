# Getting Mao Ready for Global Launch 
*Implementing our way to global subscription finish line* 

## Remaining Implementation Plans 

Aside from a few items in the v4.1.0 plan documents, everything else for a multilingual launch with secure web login, user accounts for API keys, and subscription system is complete. 

### The Essentials 

While Claude Code did plan on adding the Claude Code implantation to these combined implementation plans, I think they were having new context window struggles because I don't see it. I handed over that and the databases implementation to them. 

Regardless, the rest of the guide and plans are complete to push through implementing the rest of the backend into the UI. 

In addition they created planning and built on our initial detailed docs for the secure login system, adding in subscription systems and user accounts for API keys. And most importantly, multilingual support. 

**INITIAL QUESTIONS** 

- Does the website stuff include localization for managing languages there as well? 
- What other plans do we need to make for a multilingual launch? 
- Not something I've ever done before! 

*Fun fact they created it to be done in three 16 hour sessions* 

```
./versioning/v4_0_0/V4_IMPL_TO_LAUNCH/
├── COMPREHENSIVE_IMPLEMENTATION_ROADMAP.md   ← Strategic overview
├── COMPLETION_PLAN.md                        ← You are here
├── IMPL_SUBSCRIPTION_SYSTEM
│   └── IMPL_SUBSCRIPTION_SYSTEM.md           ← Overseas launch system
├── IMPL_UI_COMPLETE
│   └── IMPL_UI_COMPLETE.md                   ← Every remaining component
└── IMPL_UI_DETAILED
    └── IMPL_UI_DETAILED.md                   ← Tools implementation
```

### The Sensible

If these were not included above, it would make sense to add them for launch. The analytics one connects all the local builds. Claude Code is core. And the databases are necessary both for the analytics and also for the storefront information and management. The new Anthropic tools are added in because they seem like they should be simple as they're from Anthropic, but also it is a good thing for optics. 

**INITIAL QUESTIONS** 

- Did we add any of these to the above documents? 
- Maybe we should? 
- Updating the database one for managing localization seems important too. 

```
./versioning/v4_1_0/
├── IMPL_ANALYTICS
│   ├── IMPL_ANALYTICS_ACCESSIBILITY.md
│   └── MULTI_INSTANCE_DATA.md
├── IMPL_ANTHROPIC_TOOLS
│   ├── TOOL_BASH.md
│   ├── TOOL_FINE_GRAINED_STREAMING.md
│   └── TOOL_PARALLEL_USE.md
├── IMPL_CLAUDE_CODE
│   ├── CLAUDE_CODE_SDK.md
│   └── IMPL_CLAUDE_CODE.md
└── IMPL_DATABASES
    └── IMPL_DATABASES.md
```

---

"Want to start with getting that Python CLI polished for your own dogfooding?" 

LOL what is 'dogfooding'?!? 

Okay, I just changed to a new branch in git and github so that I could leave all that TypeScript Terminal UI stuff there and delete it. 

I think next we should probably assess the IMPL docs that were all prepared to go from current state through to publishing and clean them up to do the same, but this time, 1 - make sure all the things we need in the IMPL docs are complete, 2 - create a new IMPL doc for getting it finished to be able to run the tool in the terminal for us to try it out (1 and 2 sort of the same lol), 3 - new/updated IMPL doc for creating the new web app UI. 

First I want to check if these were implemented if you could help me figure it out? 

versioning/v4_0_0/IMPL_PARALLEL_AGENTS/IMPL_PARALLEL_AGENTS.md
versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md

And then, let's go through these to create a new IMPL_DEV_LIVE.md for whatever we need to do to get it to a place where we can test the app on our own in the terminal. 

./versioning/v4_0_0/V4_IMPL_TO_LAUNCH/
├── COMPREHENSIVE_IMPLEMENTATION_ROADMAP.md   ← Strategic overview
├── COMPLETION_PLAN.md                        ← You are here
├── IMPL_SUBSCRIPTION_SYSTEM
│   └── IMPL_SUBSCRIPTION_SYSTEM.md           ← Overseas launch system
├── IMPL_UI_COMPLETE
│   └── IMPL_UI_COMPLETE.md                   ← Every remaining component
└── IMPL_UI_DETAILED
    └── IMPL_UI_DETAILED.md                   ← Tools implementation

I think we want to include these as well though, they should have been integrated into the above lists -- well, there also should have only been like one IMPL plan but CC was being crazy that day. 

./versioning/v4_1_0/
├── IMPL_ANALYTICS
│   ├── IMPL_ANALYTICS_ACCESSIBILITY.md
│   └── MULTI_INSTANCE_DATA.md
├── IMPL_ANTHROPIC_TOOLS
│   ├── TOOL_BASH.md
│   ├── TOOL_FINE_GRAINED_STREAMING.md
│   └── TOOL_PARALLEL_USE.md
├── IMPL_CLAUDE_CODE
│   ├── CLAUDE_CODE_SDK.md
│   └── IMPL_CLAUDE_CODE.md
└── IMPL_DATABASES
    └── IMPL_DATABASES.md

I think we'll need all of those items. If an IMPL document is already good-to-go, we can keep it a separate document (like IMPL_DATABASES.md for example, not that that one is done) and just list it at the top of our first new IMPL document as "must be done". The new doc I think we should put here. 

./versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_DEV_LIVE.md 

And then anything for the actual web app, we should put somewhere like this. 

./versioning/v4_1_0/IMPL_WEB_UI/IMPL_WEB_UI.md 

And I'll move the IMPL docs that are separate to their appropriate sub-directory. 

Oh and we have this one to look through and move to an appropriate home. 

./versioning/v4_0_0/IMPL_UI/
├── _NEW_USER_FLOW.md
├── _VISUAL_BRAND_IDENTITY.md
├── UI_PHASE_1_LOGIC.md
└── wireframe_img
    ├── 01-mao-terminal-wireframes.html
    ├── 02-mao-terminal-wireframes.html
    ├── after-typing-slash.png
    ├── before-typing-slash.png
    ├── config-enter-some-settings.png
    └── config-slash-command-panel.png

Wdyt? 
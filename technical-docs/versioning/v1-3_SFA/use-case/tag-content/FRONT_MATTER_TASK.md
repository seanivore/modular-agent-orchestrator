# Adding Front Matter To All Markdown Files

## Task Description

We need to implement this on all of our markdown files for a project directory that is going to be published as a website. Jekyll will be converting the markdown files to HTML. There is so much content on this website that we want to set up a search feature and possible some other features that help users find what they are looking for.

To achieve this we need to look at every markdown file and add the following front matter to the top of each file, above the first H1 heading. Use the title of the page for the title field. When reviewing the files, please come up with a meta seo description for the page. The possible categories, tags, and content types are below in three lists. Choose wisely and carefully. As in the example below, three is a good number. Unless the page is SERIOUSLY about more than three, try not to use more than three for each of the three categories. 

Do this for every markdown file listed in the directory tree below. There are a couple that have already been done for you. To do this, please start at the top of the directory tree and work your way down. Select the next file to work on and cross it off the list. Add the front matter as described above. Save the markdown file without changing the name or location. Then get started on the next file. 

### Front Matter Structural Example 

```yaml
---
title: "Document Title"
categories: ["scripts", "guides", "strategies"]
tags: ["bland-ai", "voice-modulation", "example-scripts"]
content_types: ["implementation", "research", "technical"]
description: "A meta seo description of the webpage"
---
```

## Challenges 

I didn't check all of them but technical-specification.md is over 10k tokens. I have no idea how, but for some reason the API did 5 of these, had trouble with that one, and ended up racking up over 894k tokens. We learned that the text_editor tools in API either are not as capable as when you use the filesystem edit_file tool by reading the document first, or even just chunks of lines at a time first, and then planning your targeted use of the edit_file tool accordingly. 

### Economical Tool Usage 

We have multiple options. 

1. First I would recommend using the `read_multiple_files` tool to read as many in a batch as you feel comfortable taking on. 
2. Don't forget the key for making targeted `edit_file` changes is to read the file first so you know exactly what part you can replace with the new inserted text. 
3. Let me know if you want I can upload the them all to Project Knowledge Base; then you could provide me front matter blocks in one document, attributing to which file I should add it to. 

### Checking Tokens 

If you ever want to check the tokens in a file, you can use the following command:

```bash
token absolute/path/to/file.md 
token absolute/path/to/directory/
token /"text in quotes"/ 
``` 

## Categories, Tags, and Content Types to Use 

### Categories
- Scripts
- Guides
- Strategies
- Technical
- Research
- Implementation

### Content Types
- Example Scripts
- Implementation Guides
- Strategy Documents
- Technical References
- Research Findings
- Case Studies

### Tags
- bland-ai
- voice-modulation
- example-scripts
- strategy
- implementation
- technical
- research
- case-study

## Markdown Website Pages 

Only two of them are designed exclusively in HTML/CSS/JS and they are crossed off. The agent supposedly handled five of them, but the work looked sub-par considering who carefully I structured the URL slug and sections. 

FWIW the ending URL when published will be: 

- presentable.august.style/about-our-agents.md
- presentable.august.style/about-our-agents/technical-specifications.md

Just to better understand the SEO and that what you see after the Project Directory folder are optimized for SEO. 

```bash 
├── /Users/seanivore/Development/voice-mkt-sfa/about-our-agents.md
│   ├── /Users/seanivore/Development/voice-mkt-sfa/about-our-agents/technical-specifications.md
│   ├── /Users/seanivore/Development/voice-mkt-sfa/about-our-agents/what-is-sfa-single-file-agent.md
│   └── /Users/seanivore/Development/voice-mkt-sfa/about-our-agents/workflow-feedback-job-resume-case-study.md
├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study.md
│   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/brand-identity-briefings.md
│   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/agent-configuration-prompt-input.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/glossier-content-plan.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/agent-configuration-prompt-input.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/glossier-content-plan.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/hydro-flask-content-plan.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/jungalow-content-plan.md
│   │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/content-plan/production-flow-content-plan.md
│   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/email-blast.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/email-blast/ai-prompt-configuration-agent.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/email-blast/glossier-email-campaign.md
│   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/email-blast/hydro-flask-email-campaign.md
│   │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/email-blast/production-flow-email-blast.md
│   └── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/instagram-post.md
│       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/instagram-post/glossier-instagram-posts.md
│       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/instagram-post/hydro-flask-instagram-posts.md
│       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/instagram-post/instagram-post-agentic-configuration.md
│       └── /Users/seanivore/Development/voice-mkt-sfa/ai-agentic-brand-content-case-study/instagram-post/production-flow-instagram-posts.md
└── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing.md
    ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/agentic-research-planning-case-study.md
    ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/bland-ai-guides.md
    ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/bland-ai-guides/api-documentation.md
    │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/bland-ai-guides/app-ui-guide.md
    ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/analysis-optimizing-voice-ai-mkt.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/analysis-voice-mkt-home-services.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/bland-ai-pro-tips.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/bland-ai-voice-modulation.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/strategy-assertive-urgent.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/strategy-combinations.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/strategy-curiosity-gap.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/strategy-empathy-objection.md
    │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/deep-research/strategy-strongest-combos.md
    ├── ~~Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/implement-bland-modulation-research.html~~
    ├── Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map/influence-lead-type.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map/outcome-result-strategy.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map/strategy-name.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map/tactic-types.md
    │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/index-section-site-map/vocal-characteristics.md
    ├── Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/voice-marketing-matrix.md
    │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/persona-strategy.md
    │   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/persona-strategy/annotated-vo-scripts.md
    │   │   ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/persona-strategy/identifying-archetypes.md
    │   │   └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/persona-strategy/tailored-tactical-frameworks.md
    │   └── Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/writing-guide.md
    │       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/writing-guide/emotion-driven-copywriting.md
    │       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/writing-guide/modulation-sound-patterns.md
    │       ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/writing-guide/notation-cheat-sheet.md
    │       └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/research-implementation/writing-guide/script-voice-indicators.md
    ├── ~~Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/sales-development-ai-secrets.html~~
    └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy.md
        ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy/assertive-urgent-emotional.md
        ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy/combine-optimize-tactics.md
        ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy/creating-curiosity-gap.md
        ├── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy/empathy-objection-handling.md
        └── /Users/seanivore/Development/voice-mkt-sfa/ai-voice-marketing/top-conversion-strategy/target-audience-groups.md
```
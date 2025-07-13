# Critical Mao Developmental Rules 

## **Rule #1** 
  - Variable-input philosophy is IMMUTABLE 
  - NEVER add hardcoded categories, templates, enums, or predetermined options
  - But we're not against adding new sets of variables!

## **Rule #2** 
  - 6-File Tool Architecture is IMMUTABLE. 
  - NEVER merge, combine, or reorganize the 6-file tool pattern 

## **Rule #3** 
  - Human Button Interface is A MUST UNDERSTAND CONCEPT 
  - NEVER convert back to SDK-based approaches or provider-specific implementations

## **Rule #4** 
  - Print statement separation is MANDATORY; only allowed in UI layer files 
  - Core logic must remain print-free; exceptions are 'demos' and 'button' generator files 

## **Rule #5** 
  - File naming standards are PROTECTED; keep them general, not more specific than needed 
  - E.g., why put 'mao' in a file name when all the files in the codebase are 'mao'
  - NO timestamps in file names; this is unnecessary UX

## **Rule #6** 
  - NO automatic backward compatibility; NO legacy aliases, compatibility layers, or "keeping the old name" patterns
  - Product is brand new, no legacy; in the future when it is needed it will be a discussion

## **Rule #7** 
  - HUMAN-FIRST DESIGN of SETUP SCRIPT and JSON CONFIG; they should be able to create and execute without AI assistance 
  - Less use by human users should not result in a more complex design, that is contrary to our mission 

## **Rule #8** 
  - Phases (tasks) start at 1, NEVER 0; NO "Phase 0" or "00_" prefixes in directory structure 
  - Improves UX, eliminates confusion, clear, intuitive; this is a rule of thumb 

## **Rule #9** 
  - NO HARDCODED SUCCESS CRITERIA; we don't pre-define metrics like "covers 5+ competitors" or "includes timeline"
  - Claude is QA, sequential thinking, reviewing deliverables 

## **Rule #10** 
  - Our SETUP SCRIPT means COMMAND REGISTRY is UNNECESSARY; unix filesystem handles command discovery and execution 
  - Setup scripts create executable commands in `/Users/seanivore/bin`; proven pattern 
  - SETUP SCRIPT DOES NOT PUT HYPHENS IN COMMAND LINE, only spaces 

## **Rule #11** 
  - SINGLE RESPONSIBILITY FOR STATE MANAGEMENT; Memory MCP handles ALL workflow state persistence 
  - No duplicate state saving mechanisms or parallel tracking systems; one source of truth for workflow context and progression 
  - Eliminates synchronization issues and redundant operations; clean integration with single, authoritative state management

## **Rule #12** 
  - It is 'Mao' not 'MAO'; this encourages proper pronunciation 
  - Don't use m-dashes, use semicolons; if it is a header, it doesn't need to be bold 
  - We don't use emojis in UI; not a huge fan of them in docs but eh 
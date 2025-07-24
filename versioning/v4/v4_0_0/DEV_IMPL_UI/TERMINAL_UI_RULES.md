# Mao Terminal Interface Design Rules
**Cognitive Flow Protocol for Terminal UI**

## **Core Philosophy**
**Visual graphic design with constraints**: mono text + semantic colors + white space ONLY. 
Design is what makes people actually USE our functional application.

---

## **Layout & Spacing Rules**

### **Character Grid Foundation**
1. **Design to the grid** - Terminal columns = character cells (typically 8-10px wide, 16-20px tall)
2. **Grid-based thinking** - Use character cell units (20px grid = character cell dimensions)
3. **Column alignment** - All layouts respect terminal grid constraints (80x24, 60x80, etc.)
4. **Monospace constraints** - Every character occupies exactly one grid cell

### **Paragraph Grouping**
5. **Group related content together** - first 4 lines stay at top, large gap, then input field
6. **Before/after paragraph spacing** - think document spacing, not cramped terminal
7. **Much taller height overall** - let content breathe, we're not fighting for real estate
8. **Double spacing between message blocks** - generous vertical rhythm

### **Horizontal Alignment System**
9. **4ch left alignment** - ALL text content aligns at 4 character spaces from left edge
10. **Tree branches align with content** - `├──` and text content share same left edge
11. **No-indicator lines = RARE emphasis** - even rarer than pink text, used for POWER
12. **Consistent indicator spacing** - `●` + 4ch gap before all text content

---

## **Typography Constraints**

### **Font & Size Limitations**
13. **One font, one size ONLY** - never change font size due to terminal uncertainty
14. **Monospace grid system** - each character = one grid cell (8-10px wide, 16-20px tall)
15. **Character cell atomic units** - design in character counts, not arbitrary pixels
16. **Grid-first design** - layouts that fit 80x24 or 60x80 work everywhere
17. **No visual chrome** - only semantic colors, character choice, and white space

---

## **Color System & Hierarchy**

### **Opacity & Subtlety**
18. **Light blue 50% opacity** - trustworthy actions should be subtle, not competing
19. **White 50% opacity** - less prominent for system/automated content
20. **Secondary yellow** - brown mustard with light opacity (like Claude Code)

### **Pink Bold Usage Rules (MOST CRITICAL)**
21. **Pink emphasizes WHAT something happens TO** - not the verb/action
    - ❌ "**Creating** project structure"  
    - ✅ "Creating **project structure**"
22. **One pink statement per viewport** - for 60-row terminals, only one visible pink
23. **Never consecutive pink lines** - increases cognitive load too much
24. **Pink = cognitive interrupt for objects/targets** - draws attention to WHAT needs focus

---

## **Interaction & State Patterns**

### **Completion Behavior**
25. **Checkmark icon replacement**: `▲ ✓ Portfolio complete!` → `✓ Portfolio complete!`
26. **Collapse completed workflows** - when all sub-items complete, show single confirmation
27. **Two-frame completion states** - show process reaching completion, then collapsed

### **Contextual Options Display**
28. **No command lists unless /slash-command used** - don't show `/preview /data /focus` lists
29. **Main screen options = toggles/choices** - "Deploy now? (y/n)" style
30. **"Popup modules"** have pre-accommodated space - no screen shifting when content appears

### **Workflow Tree Visualization**
31. **Tree characters align with content** - maintain 4ch alignment rule
32. **Shape persistence through states** - triangle stays triangle even when complete
33. **Progressive disclosure** - show hierarchy and relationships through tree structure

---

## **Content Strategy**

### **Help & Guidance**
34. **Single contextual help message** - not lists of options
35. **Modular help system** - different states pull different contextual messages
36. **Contextual affordances** - not menus/buttons, but situation-aware guidance

### **Message Attribution & Flow**
37. **Clear turn-taking** - visual conversation protocol for human-AI dialogue
38. **Attention management** - color hierarchy guides cognitive flow
39. **Context preservation** - consistent attribution and visual patterns

---

## **Technical Constraints**

### **Terminal Compatibility**
40. **Work with any terminal theme** - don't override user's background/default colors
41. **ANSI color fallbacks** - graceful degradation for limited color terminals
42. **Cross-platform consistency** - same experience across terminal environments
43. **Grid-based portability** - designs that work in 80x24 work everywhere

### **Performance & Responsiveness**
44. **Real-time updates** - content updates without screen jumping or shifting
45. **Smooth state transitions** - visual continuity during workflow changes
46. **Minimal cognitive load** - predictable patterns reduce mental overhead

---

## **Quality Standards**

### **Visual Excellence**
47. **Every space is intentional** - precise typography like Sean's original examples
48. **Cognitive architecture** - colors serve brain function, not aesthetics
49. **Professional polish** - terminal UI that rivals graphical applications
50. **Grid-perfect alignment** - respect character cell boundaries

### **User Experience**
51. **Intuitive attribution** - instantly clear who said what
52. **Priority clarity** - what needs attention vs what's informational
53. **Conversation flow** - natural reading and interaction patterns
54. **Wireframe methodology** - design in 20px character grid units for accuracy

---

**Remember**: This isn't just terminal styling - it's a **visual conversation protocol** for human-AI collaboration. These rules create cognitive architecture that makes complex workflows feel natural and effortless.

*Every rule serves the goal: making people actually USE our functional application.* 🎯

**Design Methodology**: Use 20px character grid for wireframes - each cell = one character space. Design to the grid, not arbitrary pixels. Layouts that fit the character grid work everywhere.
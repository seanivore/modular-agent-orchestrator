
## 2. Look and Feel, Mao App High Level Design 

### Single-Screen Chat-Centric Experience 

* **Everything in the app happens in one container, one screen**

  - LLM *AI manages app operations* in chat 
    - Chat is natural for LLMs 
    - Occasional toggle menu 
    - Mao answers select slash commands 
    - Message block types with their icons are defined in detail below 
    - Semantic highlighting also defined in detail below 

  - Users to have used headless apps in their chats for a while 
    - Creating AI image generations in *Discord* threads 
    - Talking to *Slack-bot* for admin 
    - Playing games or gathering info from *Telegram bots* 

* **Visual design gracefully keeps user attention on *just* contents of the chat** 

  - After login screen, user sees chat container is *minimalistic* and *matches everything*  
    - Think computer terminal *in terms of simplicity* of functionality and singular screen 
    - *NO RETRO NERDY VIBE*, instead, this is *high class* it is timeless and classic
    - Use of *character-based icons* indicating input fields and messages 

  - The UI, the entire app, is *one single container* 
    - The container has *clean, simple, narrow lines* and a *polished depth* 
    - The UI has *NO BUTTONS, NO MENU TEXT, NO ICONS* OR OTHER INDICATORS 
    - Intentional *ABSOLUTE NOTHING* creates 'silence is loud' moment that let's you know it is *clearly intentional* 
    - Edges and border's drop-shadow onto canvas has sharp, realistic look, and a dynamic, *REAL-TIME ANIMATION* 
    - Looks like frame casting shadow is extremely narrow; like centimeters deep and wide classic black picture frame 

  - The shadow has an ever-so-slight angle meant to *mimic shadow from the sun/moonlight* 
    - The direction and size of this angled shadow *changes with the movement of the sun or moon* in fluid, constant motion 
    - It is *extremely important* that the MOTION IS SO CONSTANT AND SUBTLE THAT IT IS *TOO SLOW TO SEE HAPPEN* 
    - Motion is only noticeable when you take a moment, pause, and you're like, *wow, this is wider now on this side!*

  - Dark mode shadows exist, maintaining the luxury depth without looking washed out 
    - Deeper blacks, subtle colored tints like very dark purple or deep blue 
    - This should feel like *expensive black velvet* with *rich depth* 
    - It should *NOT FEEL FLAT GRAY*

  - *Time of day* so is used to provide timing to the animation 
    - It is illustrated to *look and behave just like real life* 
    - Daylight has sharp, defined shadows and evening has softer, deeper, maybe slightly blue-tinted from moonlight shadows 
    - These colorations and design *guidelines have been researched and are provided in detail below* 

  - THINK: The way expensive hotels *adjust lighting imperceptibly throughout the day* 
  - FEEL: Luxury that makes people feel good without knowing why 

### Real-Time Shadow Movement Creates Unconscious Luxury from Careful Details 

* **Shadow has flow of *continuous* gradient motion** 

  - *Do not change shadows in discrete phases* 
  - Ensure the slowest motion possible 
    - Avoid users watching, seeing motion; simple magic  
    - Seeing it move is trite, corny, not worth our time 
    - Mimicking real life passage of time makes it our SUBTLE but DETAIL-ORIENTED focal point  

  - Continuous gradients have *signature moments* that it builds to 
    - The shadow evolves over time 
    - It has peak characteristics at specific times 

* **More peaks = smoother interpolation just like in animations** 

  - The more keyframes, the more natural in-between transitions become 
  - Two peaks might seem similar until compared directly side-by-side 

* **First development rounds will be done by swarm of generative AI agents**

  - Subagents that run in parallel to *build website UI all have same, very specific design spec* 
    - Allows us to see what and where small variations are  
    - Like hiring 20 creative agencies at once 

  - Same method used to *split test shadow 'peak' movement timing* 
    - A shadow with peaks every 3 hours 
    - Another every 2 hours 
    - Another with one every hour

  - They can all build on timings and the cinematic shadow design breakdowns 
    - Curious to see their artistic interpretations  
    - Let's have some subagents *research known best practice* to *create the desired shadow effect* 

  - This chart shows the 3 hour 'peak' points the shadow reaches before changing motion 
    - The actual motion of all shadows *NEVER STOPS* 
    - Must be fluid 

  - Is there any way to work an ability for subagents to see a visual before fully completing their design work? 

   | TIME   | SHADOW PEAK CHARACTERISTIC  | 
   | ------ | --------------------------- |
   | 06:00  | Dawn awakening              |
   | 09:00  | Morning warmth              |
   | 12:00  | Harsh midday precision      |
   | 15:00  | Afternoon softening         |
   | 18:00  | Golden hour magic           |
   | 21:00  | Twilight mystery            |
   | 00:00  | Deep night crispness        |
   | 03:00  | Pre-dawn stillness          |

### Reference of What Shadows Look Like Around-the-Clock 

* **Day time cinematic visual design outline** 

  - The day time *basics*  
    - Warm light creates cool shadows, but cool light creates warm; *be consistent* 
    - Remember that *light bounces around, subtly illuminating shadows*, *adding complexity to value and colors* 
    - Further away objects have lighter in value shadows, bluer in tone, and less definition 
    - *Maintain consistent light source and shadow characteristics* throughout for believable and harmonious feeling  
  - *Morning* 
    - Shadows are warm, soft, and long, often described as golden; gradually shortening as the sun ascends 
    - Colors tend to be cool, reflect ambient light off morning blue sky; illuminated areas carry more warmth 
    - Evokes a mood or sense of fresh beginnings; awakening, but also tranquility  
  - *Midday* 
    - Shadows have high contrast and are well defined; shortness and sharpness; at zenith they're directly under objects 
    - Light is harsh, direct creating strong highlights with intense vibrant colors in illuminated areas 
    - Intense and awake, clear feeling 
  - *Afternoon* 
    - Sun descends so shadows lengthen; light takes on cooler, diffused quality 
    - Light tints everything in warmer tones of purple and orange; shadows retain cooler blue hue 
    - Soft light id dramatic and has a contemplative feel or a serene mood compared to midday intensity 
  - *Evening at golden hour* 
    - First and last hours of daylight; warm, soft, almost magical 
    - Long, diffused shadows blending smoothly into surroundings which adds depth 
  - *Evening at twilight* 
    - Sun dipping below horizon; light is cooler, even more diffused as shadows continue to soften and blur 
    - Moody atmosphere that combines tranquility with mystery; eerie elongated shadows 

* **Night time cinematic visual design outline** 

  - The night time *basics* for shadow color, look, and feeling  
    - Night shadows use *close range of values*, AVOID PURE BLACK
    - Balance light and dark values; *create depth and dimension* even on smaller scale 
    - Darker shadows still possess color variations of cooler tones like blues and greens in moonlit areas
    - Convey moonlight strength via shadow edges; interplay of light and shadow frames focal points, adds depth, guides the eye 
  - *Early night* with moon rising
    - Long, dramatic shadows stretching far, but with slightly softer edges from less direct light source 
    - Feels mysterious and ethereal, often dramatic emphasizing day to night transition 
  - *Mid-night* with moon high in sky
    - Bright moon shines crisp, cooler light making shorter, more defined, sharper edged shadows 
    - Clearer feeling as things are more defined; still, sometimes isolating; highlighting interplay of light and dark more 
  - *Late night* with moon nearing the horizon 
    - Redder or warmer glow and elongated shadows again like early night but in opposite direction 
    - Sense of approaching dawn, closing, beginning soon, lingering magic still with just a bit of mystery hinting at fading night 

### UI Design Philosophy 

* **Minimalistic 'devil in the details' carefully executed**

  - *Micro details are very important*
    - Hermès doesn't add more features to bags, they make every stitch flawless 
    - Cinematographer-level shadow specs because shadow is 25% of our visual vocabulary; requires museum quality execution 
  - Shadow movement is not meant to be cute
    - It should barely be noticed to create luxury minimalism that separates us from boring
    - It is to make people say "I don't know why, but this feels expensive" 

* **Carefully constrained: FOUR ELEMENTS CONTROL OUR DESIGN** 

  1. *Shadow movement* is an ever-present, too-slow-to-see-move with human eye feature 
  2. Conceptual *semantic text highlighting* with few colors that lighten cognitive load 
  3. *Character choice* like bullet icons; typography, but only ONE FONT 
  4. *White space*, again lightening cognitive load; not a chat like a history receipt that records everything, it evolves, simplifies 

  - Limited constraint allows for each element to be executed with obsessive precision that is simple, sharp, effective 
    - We do not dazzle with features; the features are intuitive and quiet in that way 
    - Instead, we hypnotize with perfection of subtleties 

### About Our Tech Stack 

* **The entire website will be HTML, CSS, and JS** 

  - No framework needed, just simple web tech; maximum performance and simplicity 
  - Dynamic shadow system
    - JavaScript: `new Date()` gets current time
    - CSS: `box-shadow` properties can be dynamically updated 
    - Smooth transitions: CSS `transition: box-shadow 0.5s ease`
    - Geolocation: `navigator.geolocation` for real sun position (optional)

* **CSS Animation Note** 

  - Previous builds had a lot of trouble with lag when animation covered large portions of screen or had high number of animations 
    - We must engineer smart and avoid this 
    - Create shadows only in necessary area, along lines, shapes 

* **Basic structure:**

```javascript
function updateShadow() {
  const now = new Date();
  const hour = now.getHours();
  // Calculate shadow angle/intensity based on time
  // Update CSS custom properties
  document.documentElement.style.setProperty('--shadow-x', shadowX);
  document.documentElement.style.setProperty('--shadow-y', shadowY);
}
setInterval(updateShadow, 60000); // Update every minute
```

### Hybrid Caching Best Practices & Fingerprinting 

* **All models and/or providers config JSON objects have pricing** 

  - This information is used to dynamically calculate accurate usage costs regardless of what model the agent is 
  - This includes differences in counting tokens 

* **NECESSARY UPDATE: 'Estimated' costs must be ACTUAL COSTS using REAL MATH everywhere** 

  - Any areas we cannot use the real numbers and match, I need us to collect on a list
    - We cannot use fabricated information when we start marketing the product
    
  - Provider-Specific JSON Objects for Regular Updating 
    - There is a chart from Anthropic pasted below, we need this as a JSON config file that can be updated over time easily 
    - Find and create the same for any other models that do caching 

| Context Window Size  | Input      | Output        | 
| -------------------- | ---------- | ------------- |
| Prompts ≤ 200K       | $3 / MTok  | $15 / MTok    |
| Prompts > 200K       | $6 / MTok  | $22.50 / MTok |

|                    | Base          | 5m Cache      | 1h Cache     | Cache Hits    | Output        |
| Model              | Input Tokens  | Writes        | Writes       | & Refreshes   | Tokens        |
| ------------------ | ------------- | ------------- | ------------ | ------------- | ------------- | 
| Claude Opus 4.1    | $15 / MTok    | $18.75 / MTok | $30 / MTok   | $1.50 / MTok  | $75 / MTok    | 
| Claude Opus 4      | $15 / MTok    | $18.75 / MTok | $30 / MTok   | $1.50 / MTok  | $75 / MTok    |
| Claude Sonnet 4    | $3 / MTok     | $3.75 / MTok  | $6 / MTok    | $0.30 / MTok  | $15 / MTok    | 
| Claude Sonnet 3.7  | $3 / MTok     | $3.75 / MTok  | $6 / MTok    | $0.30 / MTok  | $15 / MTok    | 
| Claude Haiku 3.5   | $0.80 / MTok  | $1 / MTok     | $1.6 / MTok  | $0.08 / MTok  | $4 / MTok     |
| Claude Haiku 3     | $0.25 / MTok  | $0.30 / MTok  | $0.50 / MTok | $0.03 / MTok  | $1.25 / MTok  |

* **OTHER MODEL UPDATES: Context windows, etc.** 

  - Change Context Window for Sonnet 4 to 1 Million; needs update of Configuration File Templates index @ LINE 221
    - New Opus and other pricing for Cached Tokens; Sonnet 3.5 and Opus 3 depreciated 
    - Pricing multipliers are 5 min cache write are 1.25 times the base input, 1h are 2 times, and cache read are 0.1 time base 
    - Search online for any other models to update like GPT/OpenAI

# Keyword Master 


## Task Description 

Extract high-value semantic keywords and phrases from our documentation set. For each document:

1. Identify the most important concepts (beyond the obvious categories/tags)
2. Extract terminology that represents unique aspects of our approach
3. Identify phrases that users might search for when looking for this content
4. Consider both technical terms and natural language queries
5. Focus on what makes each document uniquely valuable

For each keyword/phrase, provide:
- The exact keyword/phrase
- Its significance/context
- The document(s) where it appears

Prioritize terms that would help users find exactly what they're looking for when combined with our categories, tags, and content types. Exclude generic terms already covered by our classification system.

Output the results as a structured JSON file that could be integrated with our search system.

## Review Phase 

"Think like a user searching for solutions. What specific words would someone type to find exactly this document and no others? Focus on unique value phrases (4-6 words) that capture core concepts. Extract 5-7 high-value terms per document, prioritizing distinctive technical terminology and problem-solving language over general concepts. Include both expert terminology and novice phrasing variants for each key concept."

This combines:
1. The search mindset (Google-style thinking)
2. Concrete guidance on quantity (5-7 terms per document)
3. Length guidance (4-6 word phrases capture more specificity)
4. The dual perspective (expert/novice terminology variants)

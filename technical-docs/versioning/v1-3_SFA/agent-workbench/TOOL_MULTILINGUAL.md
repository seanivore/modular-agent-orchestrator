Build with Claude
Multilingual support
Claude excels at tasks across multiple languages, maintaining strong cross-lingual performance relative to English.

​
Overview
Claude demonstrates robust multilingual capabilities, with particularly strong performance in zero-shot tasks across languages. The model maintains consistent relative performance across both widely-spoken and lower-resource languages, making it a reliable choice for multilingual applications.

Note that Claude is capable in many languages beyond those benchmarked below. We encourage testing with any languages relevant to your specific use cases.

​
Performance data
Below are the zero-shot chain-of-thought evaluation scores for Claude 3.7 Sonnet and Claude 3.5 models across different languages, shown as a percent relative to English performance (100%):

Language	Claude 3.7 Sonnet1	Claude 3.5 Sonnet (New)	Claude 3.5 Haiku
English (baseline, fixed to 100%)	100%	100%	100%
Spanish	97.6%	96.9%	94.6%
Portuguese (Brazil)	97.3%	96.0%	94.6%
Italian	97.2%	95.6%	95.0%
French	96.9%	96.2%	95.3%
Indonesian	96.3%	94.0%	91.2%
German	96.2%	94.0%	92.5%
Arabic	95.4%	92.5%	84.7%
Chinese (Simplified)	95.3%	92.8%	90.9%
Korean	95.2%	92.8%	89.1%
Japanese	95.0%	92.7%	90.8%
Hindi	94.2%	89.3%	80.1%
Bengali	92.4%	85.9%	72.9%
Swahili	89.2%	83.9%	64.7%
Yoruba	76.7%	64.9%	46.1%
1 With extended thinking and 16,000 budget_tokens.

These metrics are based on MMLU (Massive Multitask Language Understanding) English test sets that were translated into 14 additional languages by professional human translators, as documented in OpenAI’s simple-evals repository. The use of human translators for this evaluation ensures high-quality translations, particularly important for languages with fewer digital resources.

​
Best practices
When working with multilingual content:

Provide clear language context: While Claude can detect the target language automatically, explicitly stating the desired input/output language improves reliability. For enhanced fluency, you can prompt Claude to use “idiomatic speech as if it were a native speaker.”
Use native scripts: Submit text in its native script rather than transliteration for optimal results
Consider cultural context: Effective communication often requires cultural and regional awareness beyond pure translation
We also suggest following our general prompt engineering guidelines to better improve Claude’s performance.

​
Language support considerations
Claude processes input and generates output in most world languages that use standard Unicode characters
Performance varies by language, with particularly strong capabilities in widely-spoken languages
Even in languages with fewer digital resources, Claude maintains meaningful capabilities
Prompt Engineering Guide

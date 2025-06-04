Agents and tools
Google Sheets add-on
The Claude for Sheets extension integrates Claude into Google Sheets, allowing you to execute interactions with Claude directly in cells.

​
Why use Claude for Sheets?
Claude for Sheets enables prompt engineering at scale by enabling you to test prompts across evaluation suites in parallel. Additionally, it excels at office tasks like survey analysis and online data processing.

Visit our prompt engineering example sheet to see this in action.

​
Get started with Claude for Sheets
​
Install Claude for Sheets
Easily enable Claude for Sheets using the following steps:

1
Get your Anthropic API key

If you don’t yet have an API key, you can make API keys in the Anthropic Console.

2
Install the Claude for Sheets extension

Find the Claude for Sheets extension in the add-on marketplace, then click the blue Install btton and accept the permissions.


Permissions

3
Connect your API key

Enter your API key at Extensions > Claude for Sheets™ > Open sidebar > ☰ > Settings > API provider. You may need to wait or refresh for the Claude for Sheets menu to appear.

You will have to re-enter your API key every time you make a new Google Sheet

​
Enter your first prompt
There are two main functions you can use to call Claude using Claude for Sheets. For now, let’s use CLAUDE().

1
Simple prompt

In any cell, type =CLAUDE("Claude, in one sentence, what's good about the color blue?")

Claude should respond with an answer. You will know the prompt is processing because the cell will say Loading...

2
Adding parameters

Parameter arguments come after the initial prompt, like =CLAUDE(prompt, model, params...).
model is always second in the list.

Now type in any cell =CLAUDE("Hi, Claude!", "claude-3-haiku-20240307", "max_tokens", 3)

Any API parameter can be set this way. You can even pass in an API key to be used just for this specific cell, like this: "api_key", "sk-ant-api03-j1W..."

​
Advanced use
CLAUDEMESSAGES is a function that allows you to specifically use the Messages API. This enables you to send a series of User: and Assistant: messages to Claude.

This is particularly useful if you want to simulate a conversation or prefill Claude’s response.

Try writing this in a cell:


=CLAUDEMESSAGES("User: In one sentence, what is good about the color blue?
Assistant: The color blue is great because")
Newlines

Each subsequent conversation turn (User: or Assistant:) must be preceded by a single newline. To enter newlines in a cell, use the following key combinations:

Mac: Cmd + Enter
Windows: Alt + Enter

Example multiturn CLAUDEMESSAGES() call with system prompt

​
Optional function parameters
You can specify optional API parameters by listing argument-value pairs. You can set multiple parameters. Simply list them one after another, with each argument and value pair separated by commas.

The first two parameters must always be the prompt and the model. You cannot set an optional parameter without also setting the model.

The argument-value parameters you might care about most are:

Argument	Description
max_tokens	The total number of tokens the model outputs before it is forced to stop. For yes/no or multiple choice answers, you may want the value to be 1-3.
temperature	the amount of randomness injected into results. For multiple-choice or analytical tasks, you’ll want it close to 0. For idea generation, you’ll want it set to 1.
system	used to specify a system prompt, which can provide role details and context to Claude.
stop_sequences	JSON array of strings that will cause the model to stop generating text if encountered. Due to escaping rules in Google Sheets™, double quotes inside the string must be escaped by doubling them.
api_key	Used to specify a particular API key with which to call Claude.

Example: Setting parameters

​
Claude for Sheets usage examples
​
Prompt engineering interactive tutorial
Our in-depth prompt engineering interactive tutorial utilizes Claude for Sheets. Check it out to learn or brush up on prompt engineering techniques.

Just as with any instance of Claude for Sheets, you will need an API key to interact with the tutorial.
​
Prompt engineering workflow
Our Claude for Sheets prompting examples workbench is a Claude-powered spreadsheet that houses example prompts and prompt engineering structures.

​
Claude for Sheets workbook template
Make a copy of our Claude for Sheets workbook template to get started with your own Claude for Sheets work!

​
Troubleshooting

NAME? Error: Unknown function: 'claude'


#ERROR!, ⚠ DEFERRED ⚠ or ⚠ THROTTLED ⚠


Can't enter API key

​

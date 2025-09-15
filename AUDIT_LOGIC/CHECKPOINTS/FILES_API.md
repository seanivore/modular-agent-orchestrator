How do we have this set up now? Because it looks like the uploaded file needs to be at a path, which would potentially defeat our intention of using the Files API as a ways to save on tokens, no? Maybe you could review this and see if there is a way to do this like, would we want to put it in a temp. file? I'm also just a bit confused trying to wrap my head around this when thinking about the app being used by a User as a web app ... though I guess anything they'd want to use *would* be on their local computer. But there is a project state JSON that we'll be using for the memory context and I'm curious how that works. I'm guessing we can save it as .temp somehow first? 

This one isn't that in depth: 

`https://docs.anthropic.com/en/docs/build-with-claude/files`

But then the actual Messages API information is in depth, though when I tried to copy it, it said Markdown but came out as YAML. But I'm assuming what is on this page is more helpful. If you want I can gather the python message for each (unless we want cURL, I'm guessing no, but the whole "Code Execution too" thing confuses me a bit). 

CREATE FILE: `https://docs.anthropic.com/en/api/files-create` 
LIST FILES: `https://docs.anthropic.com/en/api/files-list` 
GET FILE METADATA: `https://docs.anthropic.com/en/api/files-metadata` 
DOWNLOAD A FILE: `https://docs.anthropic.com/en/api/files-content` 
DELETE A FILE: `https://docs.anthropic.com/en/api/files-delete` 
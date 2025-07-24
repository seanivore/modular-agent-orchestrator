# Secure Login Details 

## UserID Generation 

- The UserID is generated using a script 
- The script is a Python script that is run in the terminal 

`./Users/seanivore/Development/modular-agent-orchestrator/scripts/user_id_generator/user_id_generator.py`

Hey hey hey so I asked that you create for me two scripts a bit back. And back then I was thinking primarily about Usernames as login, but honestly the more I think of ways to create emotional gut checks from showing emotional intelligence. 

Example that I just asked Claude OS about doing --  "I'm super into this idea that instead of canned text -- like see in the bottom left of the second image, third image, fourth image -- that is Claude Code and whenever you message them and they are active running tools or writing files, it creates a contextually relevant word where it could just say "thinking" .... like the one says budgeting and that was after I asked them to take a break because we were eating up my API money.. the other says celebrating from after the audit -- and so often it says things like "flibbergitting" and super strange not-quite-words. That is UX emotional intelligence -- like I just LOL'ed and the actual gut check test that I made my employees have to pass to post content was if they made an audible noise like a gasp or LOL -- THAT is what converts people share share share donate etc. 

Anyway, I want to do this in a couple spots. That's doable right?"

Images attached. 

Well it makes me want more and more to use their real name. Not force them but encourage that. Cause I like how Claude OS always greets me on the homepage heading with something novel and "Sean" 

BUT then i realized, we created a script that created a unique ID for a word, that is always the same for that word, BUT WE DIDN'T REALIZE THAT PEOPLE MIGHT USE THE SAME USERNAME. I immediately thought of it when I considered names. 

So options being ... well I have a few options but I honestly sort of want to just demand it be email address that is valid. 

ALSO though like we need a login eventualy and GOD i love passkeys I logged into porkbun today to see if there were interesting "mao" or "maomao" email addresses (NO someone bought them all) for a line in the docs that say they should email us regarding data. Anyway this setup was rad because, even though it says to leave password blank if you use passkey, i had no memory of which i set up (and certainly didn't think "oh yeah of course porkbun has passkey lol) so i enter my normal password and hit enter (screenshots attached) and BOOM up comes my passkey anyway! no remembering anything necessary. its even smoother on mobile (and I cant take screenshots of it working lol) 

so what am i saying. ah well the trite option would be to block people from using their name or a username that someone else already has otherwise it will mess up half of our analytics that use the userID as an anon layer. BUT we need their email anyway. they'll have to pay a subscription fee which will give them access to online hosted configs of all the variety as well as guides for creating their own slash command for example. and well emails have to be unique! then i can get their name too. I mean claude code makes you jump to a website and log in that way which i guess is nicer than added api keys (OHHH which woudl be rad in that we could let them set up their api keys on our website in their account which owuld make things easier for them than trying to put it in an iphone or people not knowing how to do it with a terminal (which is why claude code does it that way)... 

so hmmi changed my mind halfway through this hahahah i was going to say we need to make it not allow dupes but fuck that we'll change the word "username" to "email", keep userID for the mental separation to encourage trust. 

cool and i jsut tried my email and it works fine. so what do we need to adapt then.... 


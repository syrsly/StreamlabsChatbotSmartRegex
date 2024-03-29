# StreamlabsChatbotSmartRegex
Make sure you get the latest version from https://github.com/syrsly/StreamlabsChatbotSmartRegex

Give your Streamlabs Chatbot some personality using regex and smart responses. Cooldowns supported. Costs not yet supported.


This script add-on for Streamlabs Chatbot/Ankhbot was created by Syrsly for his channel's bot at https://www.twitch.tv/syrsly and is based on work by Reecon: https://github.com/Reecon/SLCatchPhrases

Very loosely inspired by the code in the Streamlabs Chatbot "WordTrigger" script found at https://github.com/castorr/Chatbot-Scripts/tree/master/Tools/Word%20Trigger which allows a word to be anywhere in a phrase or sentence.

I update this script only in my free time. It is not my occupation. If you need support and it's time-sensitive, feel free to contact me on Twitch about it, and we can arrange a commission. Otherwise, post your issue(s) to the GitHub Issues section of this repository and I'll get to it when I feel motivated to do so, which could be in a hour, a day, or even a year.

### Example Expressions

Say "You're breathtaking!" or "ur amazing" and you'll get a nice response with this:
`youre /.*[yY]?[oO]?[uU]\'?[rR]?[eE]?\s+(\w+).*/ 4 everyone "No, *you're* $resp1!"`

Say "!joke" or "Tell me a joke" or anything with "joke" word and the bot will tell a joke from ICanHazDadJoke API:
`joke /.*joke.*/ 5 everyone "$joke"`

Note: Jokes can also be loaded from a jokes.conf file or via another API, but this will require minor code edits in the Parse function.

Say "!weather" or "What's the weather like" or anything with "weather" word and the bot will tell weather from the OpenWeatherMap API (requires setup, see "OpenWeatherMap API" code in Parse function):
`weather /.*weather.*/ 5 everyone "$weather"`

Note: Weather API returns JSON response. This example is included to show you how to use JSON in the Parse function.

Test your regex here: https://regexr.com/

Here's a short clip of myself (Syrsly) working on my own regex ideas for this script: https://www.twitch.tv/syrsly/clip/CulturedCrowdedSwallowGrammarKing

Like this bot script? I used to use it on my stream, but I've moved to greener pastures with PhantomBot. PhantomBot isn't as flexible or as easy to understand, but it can run headless on a VPS with 24/7 uptime, so I highly recommend it if you're willing to move to a VPS.

# Requirements:

Streamlabs Chatbot

That's about it, really. Maybe some coding knowledge but not a lot.

# Limitations:

Regex looks anywhere in a user's chat message, not just the beginning or end. Some effort was taken to begin supporting such features as beginning-with and ending-with searches, but that work was not yet fruitful before moving to PhantomBot. I may add onto the code for fun later, but please, if you need this kind of functionality, look elsewhere for now, or expand the code functionality yourself. It's simpler than you might think! (Please share any fixes you figure out in either the issues area or in a fork. Thanks.

The first regex found is the only one to trigger, per message. This is by design. I will not change this. Ever.
If a message has 2 regex patterns, it will stop responding after the first one (based entirely on where the regex is on the regex list file). If you want one phrase to trigger rather than another one, place it higher on the list.

Chat currency is not currently used in this script and I have no plans to support that feature. If it's really important to you, consider sponsoring the work. If you find bugs, feel free to report them in the issues section on GitHub and I can investigate the issues whenever it suits me. You can contact me via Twitter at twitter.com/syrslywastaken or send me an email at syrsly@syrsly.com if you need immediate support.

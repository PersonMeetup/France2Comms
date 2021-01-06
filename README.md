# France2Comms
*"Have you thought of making a channel here that auto posts to Twitter" -Hama*

France2Comms is a Discord/Twitter bot that allows automatic message posting to Twitter.

## Functionality
When a message is sent, the first action the bot will take is to check two things:
```
1) "Should I be checking messages right now?"
2) "Is this in the right channel?"
```
Should either of those prove false, the bot will ignore the message. The settings for those values will be pulled from the `config.ini` file that comes with the bot.
Past that, the bot will check if the user has opted into having their messages sent to the Twitter account. Should that prove true, the bot will send out the message bundle for another piece of code to handle.

## Commands:
`/mark [optional: channel]` Designates either the current or a selected channel for posting to Twitter [Admin/Dev only]
`/toggle [bool]` Sets message forwarding to Twitter on or off [Admin/Dev only]
`/optin` & `/optout` Signal participation in the bot's Twitter functionality

## Risks and Liabilities
I don't fully know what toes I could be stepping on right now, given the manual spam that the Twitter account has already dealt with. I'm playing as cautious as possible, as I don't want things to go completely wrong.

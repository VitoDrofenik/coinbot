# stockbot
### Discord bot

## Invite
You can invite the bot to your discord server by clicking the [link](https://bit.ly/39bxPcO).

## Setup
##### You only need this if you are going to host your own version of the bot
Before usage, a new Discord application has to be created, as shown in the [instructions](http://discordpy.readthedocs.io/en/latest/discord.html), where the private key is aquired. The key is used when running the application for authentication. It has to be placed into a folder next to the bot file, or directly in the client.run command.

## Usage
The bot has 5 commands:
* $price or $p<br/>usage: `$price <query> or $p <query>`<br/>sends an embed with the current price for the symbol.<br/>
* $indepth<br/>usage: `$indepth <query>`<br/>sends an embed with current price, open, dayHigh, dayLow, prevClose and marketCap for the symbol.<br/>
* $info<br/>usage: `$info <query>`<br/>sends an embed with some basic informations about the company with the symbol queried.<br/>
* $help<br/>usage: `$help`<br/>sends an embed with the help message.<br>
* $invite<br/>usage: `$invite`<br/>sends an invite link for itself to be added to other discord servers.
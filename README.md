# no-more-twitch-bots

Extremely simple script that will automatically ban all lurker Twitch bots that add up into your viewer list on Twitch 
but do absolutely nothing (except spamming).

Bot list to ban is extracted from [Twitch Insights API](https://twitchinsights.net/bots).

## Configuration

Clone the project, install requirements as usual:

```bash
git clone git@github.com:marcsances/no-more-twitch-bots.git
cd no-more-twitch-bots
python -m pip install requirements.txt
```

Register a chatbot app on [Twitch Developers](https://dev.twitch.tv/), get the client ID.

Get a bot token here [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/). Make sure to log in as a user with mod
privileges in your channel. No need to be yourself.

Go to ``main.py`` and edit the variables in uppercase:

| Variable        | Value                                                            |
|-----------------|------------------------------------------------------------------|
| USERNAME        | The username for which you generated a token                     |
| CHANNEL         | The channel where the bans should be applied                     |
| CLIENT_ID       | The chatbot app client ID generated on Twitch Devleopers         |
| TOKEN           | The bot token you created on the second link                     |
| WHITELIST       | List of bots that should not be banned (moobot, etc)             |
| DEBUG           | Set to true if you want to see what is going on through IRC      |
| THRESHOLD       | Minimum amount of channels where the bot is present to be banned |

That's it, once configured, run with:

```bash
python main.py
```

and enjoy

## Rolling back

You can rollback all the bans by changing line 42 from ``self.ban(entry[0])`` to ``self.unban(entry[0])``.

## FAQ

### OMG SO MANY USERS

Yeah all bots are taken into account. It would actually take half a year to ban every single bot (threshold=0), that's
why Threshold is a thing.

### Stuck on initializing

Try again, sometimes IRC just fails to initialize

### (Insert important bot name) here got banned

Add it to the whitelist so it's not banned anymore. Make sure that you add all your bots to the whitelist before 
proceeding.

Unban the bot in your channel and no worries.

### License?

Do whatever.
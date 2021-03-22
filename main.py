import logging
from multiprocessing import RLock
from threading import Thread
import sys
import time

import requests
from irc.bot import SingleServerIRCBot

USERNAME = 'A MOD OF YOUR CHANNEL'
CHANNEL = 'YOUR CHANNEL'
CLIENT_ID = 'GET ONE IN https://dev.twitch.tv/'
TOKEN = 'GET ONE IN https://twitchapps.com/tmi/'
DEBUG = False
WHITELIST = ['streamelemenmts', 'nightbot', 'moobot']


class TwitchBotBan(SingleServerIRCBot):
    def __init__(self):
        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + CHANNEL
        headers = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']
        self.lock = RLock()
        self.channel = CHANNEL

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + TOKEN)], USERNAME, USERNAME)

    def on_welcome(self, c, e):
        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print("Chatbot started, fetching mod users")
        r = requests.get('https://api.twitchinsights.net/v1/bots/all').json()
        for entry in r['bots']:
            self.ban(entry[0])
        print("Process complete")
        sys.exit(0)

    def ban(self, username):
        if username in WHITELIST:
            print("Refused to ban " + username)
            return
        with self.lock:
            self.connection.privmsg(self.channel, "/ban " + username)
        print("Banned " + username)
        time.sleep(0.5)

    def unban(self, username):
        self.connection.privmsg(self.channel, "/unban " + username)


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

print("Initializing")
Thread(target=TwitchBotBan().start).start()

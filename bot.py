import irc.bot
import os

username = "hassansyyid"
token = os.environ['BOT_OAUTH_TOKEN']
channel = "hassansyyid"


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel, tally, voters, question):
        self.token = token
        self.channel = '#' + channel
        self.tally = tally
        self.voters = voters
        self.question = question

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print
        'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, channel)

    def on_welcome(self, c, e):
        print
        'Joining ' + self.channel

        c.join(self.channel)

        c.privmsg(self.channel, "!!!!")
        c.privmsg(self.channel, self.question)
        c.privmsg(self.channel, "!!!!")

    def on_pubmsg(self, c, e):
        print(e)
        self.cast_vote(e.source, e.arguments[0].lower())
        return

    def cast_vote(self, user_id, selection):
        if selection in self.tally:
            if user_id not in self.voters:
                self.tally[selection] += 1
                self.voters[user_id] = selection
            else:
                # Remove old selection
                old_selection = self.voters[user_id]
                self.tally[old_selection] -= 1

                # New selection
                self.tally[selection] += 1
                self.voters[user_id] = selection

            print(self.tally)


def start_voting(opts, question):
    tally = {}

    # Add options
    for opt in opts:
        tally[opt] = 0

    print(tally)

    voters = {}

    bot = TwitchBot(username, token, channel, tally, voters, question)
    bot.start()

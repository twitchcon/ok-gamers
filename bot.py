import irc.bot
import os

username = "hassansyyid"
token = os.environ['BOT_OAUTH_TOKEN']
channel = "hassansyyid"
bot = None


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

    def announce_vote(self):
        c = self.connection

        c.privmsg(self.channel, "!!!!")
        c.privmsg(self.channel, "== VOTE ==")
        c.privmsg(self.channel, self.question)
        c.privmsg(self.channel, "!!!!")

    def on_welcome(self, c, e):
        print
        'Joining ' + self.channel

        c.join(self.channel)

        # Announce vote
        self.announce_vote()

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
    global bot

    # Create tally
    tally = {}

    # Add options
    for opt in opts:
        tally[opt] = 0

    print(tally)

    # Use running bot
    if bot is not None:
        bot.tally = tally
        bot.question = question
        bot.voters = {}
        bot.announce_vote()
    # Start the bot
    else:
        bot = TwitchBot(username, token, channel, tally, {}, question)
        bot.start()


def is_voting():
    global bot
    return bot is not None


def get_question():
    global bot
    return bot.question


def end_vote():
    global bot
    bot.disconnect()


def get_votes():
    global bot
    return {} if (bot is None) else bot.tally

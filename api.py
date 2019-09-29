# load env vars
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, make_response, jsonify

import bot

app = Flask(__name__)


@app.route('/votes')
def get_votes():
    if bot.is_voting():
        return make_response(jsonify(data={
            "title": bot.get_question(),
            "votes": bot.get_votes().values(),
            "labels": bot.get_votes().keys()
        }), 200)
    else:
        return make_response(jsonify(data={}), 200)


@app.route('/vote', methods=['POST'])
def start_vote():
    body = request.json
    print(body)
    bot.start_voting(body['opts'], body['phrase'])

# load env vars
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, make_response, jsonify

import bot

app = Flask(__name__)


@app.route('/votes')
def get_votes():
    if bot.is_voting():
        response = make_response(jsonify(data={
            "title": bot.get_question(),
            "votes": list(bot.get_votes().values()),
            "labels": list(bot.get_votes().keys())
        }), 200)
    else:
        response = make_response(jsonify(data={
            "title": "No ongoing poll!",
            "votes": [],
            "labels": []
        }), 200)

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/vote', methods=['POST'])
def start_vote():
    body = request.json
    print(body)
    bot.start_voting(body['opts'], body['phrase'])
    return make_response(jsonify(success=True), 200)

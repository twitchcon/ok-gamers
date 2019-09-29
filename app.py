# load env vars
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, make_response, jsonify

import azure.cognitiveservices.speech as speechsdk
import string
import time
import os

import bot

# Setup variables
KEYWORD = "ok gamers"  # lowercase please
DEBUG = True  # for testing purposes

FLUFF_PHRASES = ["should i", "should we", "do i", "do we"]  # fluff phrases to remove when considering vote intent

app = Flask(__name__)


def doSpeechRec():
    speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['AZURE_SERVICE_REGION']
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    def detectKeyword(evt):
        phrase = evt.result.text.lower()
        print(phrase)

        if KEYWORD in phrase:
            opts = parseKeywordPhrase(phrase)

            # Start vote
            bot.start_voting(opts, phrase)

    # Callback functions
    if DEBUG:
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: detectKeyword(evt))

    print("Say a few words\n\n")

    speech_recognizer.start_continuous_recognition()

    # TODO: Turn it off
    # speech_recognizer.stop_continuous_recognition()


def parseKeywordPhrase(phrase):
    """Return options to be voted on"""
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))  # Remove all punctuation.
    phrase = phrase.replace(KEYWORD, "")  # Remove the keyword.

    for _, fluff in enumerate(FLUFF_PHRASES):
        phrase = phrase.replace(fluff, "")

    phrase = phrase.lstrip(" ")  # Remove whitespace.
    opts = phrase.split(" or ")

    return opts


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


# == Start Speech Rec ==
doSpeechRec()

# load env vars
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, make_response, jsonify
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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

    foundKeyword = False

    def detectKeyword(evt):
        phrase = evt.result.text.lower()
        print(phrase)

        if KEYWORD in phrase:
            opts = parseKeywordPhrase(phrase)

            # Start vote
            bot.start_voting(opts, phrase)

            nonlocal foundKeyword
            foundKeyword = True

    # Callback functions
    if DEBUG:
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: detectKeyword(evt))

    print("Say a few words\n\n")

    speech_recognizer.start_continuous_recognition()

    while not foundKeyword:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()


def parseKeywordPhrase(phrase):
    """Return options to be voted on"""
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))  # Remove all punctuation.
    #phrase = phrase.replace(KEYWORD, "")  # Remove the keyword.

    #for _, fluff in enumerate(FLUFF_PHRASES):
    #    phrase = phrase.replace(fluff, "")

    phrase = phrase.lstrip(" ")  # Remove whitespace.

    #opts = phrase.split(" or ")

    text = nltk.word_tokenize(phrase)
    print(nltk.pos_tag(text))

    #words = phrase.split(" ")
    #tokenizer = MWETokenizer()
    #test = tokenizer.tokenize(words)
    #print(test)

    return text


@app.route('/votes')
def get_votes():
    return make_response(jsonify(votes=bot.get_votes()), 200)


# == Start Speech Rec ==

if __name__ == "__main__":
    if DEBUG:
        parseKeywordPhrase("ok gamers should we go left or right")
        #parseKeywordPhrase("In a little or a little bit or a lot in spite of")
    else:
        doSpeechRec()

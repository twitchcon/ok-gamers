# load env vars
from dotenv import load_dotenv

load_dotenv()

import azure.cognitiveservices.speech as speechsdk
import os
import requests
import string
import time

# Setup variables
KEYWORD = "ok gamers"  # lowercase please
DEBUG = True  # for testing purposes

FLUFF_PHRASES = ["should i", "should we", "do i", "do we"]  # fluff phrases to remove when considering vote intent


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
            requests.post('http://127.0.0.1:5000/vote', json={"opts": opts, "phrase": phrase})

    # Callback functions
    if DEBUG:
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: detectKeyword(evt))

    print("Say a few words\n\n")

    speech_recognizer.start_continuous_recognition()

    # Keep listening
    while True:
        time.sleep(0.5)

    # Turn it off
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


# == Start Speech Rec ==
doSpeechRec()

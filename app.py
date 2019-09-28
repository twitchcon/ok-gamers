import azure.cognitiveservices.speech as speechsdk
import string, time

# Setup variables
KEYWORD = "ok gamers" # lowercase please
PATH_TO_CONFIG = "config.txt" # txt file please
DEBUG = False # for testing purposes

FLUFF_PHRASES = ["should i", "should we", "do i", "do we"] # fluff phrases to remove when considering vote intent

def getTokens():
    f = open(PATH_TO_CONFIG, "r")
    lines = f.readlines()
    tokens = []
    for line in lines:
        line = line.rstrip("\n")
        tokens.append(line)

    if DEBUG:
        print("Got tokens:\n{}".format(tokens))

    return tokens

def doSpeechRec(tokens):
    speech_key, service_region = tokens[0], tokens[1]
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    foundKeyword = False

    def detectKeyword(evt):
        phrase = evt.result.text.lower()
        print(phrase)

        if KEYWORD in phrase:
            opts = parseKeywordPhrase(phrase)
            # TODO: Create vote in chat

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
    phrase = phrase.translate(str.maketrans("", "", string.punctuation)) # Remove all punctuation.
    phrase = phrase.replace(KEYWORD, "") # Remove the keyword.

    for _, fluff in enumerate(FLUFF_PHRASES):
        phrase = phrase.replace(fluff, "")

    phrase = phrase.lstrip(" ") # Remove whitespace.
    opts = phrase.split(" or ")

    return opts


if __name__ == "__main__":
    if DEBUG:
        parseKeywordPhrase("ok gamers do we go left or go right.")
    else:
        tokens = getTokens()
        doSpeechRec(tokens)

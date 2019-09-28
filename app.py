import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").

f = open("config.txt", "r")
lines = f.readlines()
tokens = []
for line in lines:
    line = line.rstrip("\n")
    tokens.append(line)

print(tokens)



speech_key, service_region = tokens[0], tokens[1]
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def doSpeechRec():
# Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result.
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query.
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.


    foundKeyword = False

    def detectKeyword(evt):
        print(evt.result.text)
        if "ok gamers" in evt.result.text.lower():
            nonlocal foundKeyword
            foundKeyword = True


# Callback functions
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
#speech_recognizer.recognized.connect(lambda evt: print('\n{}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: detectKeyword(evt))

    print('Say a few words\n\n')

    speech_recognizer.start_continuous_recognition()

    while not foundKeyword:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    """
    result = speech_recognizer.recognize_once()

# Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    """

if __name__ == "__main__":
    doSpeechRec()

import speech_recognition as sr
from playsound import playsound
import os
import sys
import string
import re
import json
from chatbot import predict_class as predict_class
from chatbot import get_response as get_response
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech_v1
from supportedLanguages import lang

sys.tracebacklimit = 0
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\Zenpa\OneDrive\Documents\Class Assignments\CS173\Final Project\Linguality\credentials.json" #setting API JSON
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #prevents tensorflow warnings https://stackoverflow.com/questions/35911252/disable-tensorflow-debugging-information
intents = json.loads(open('intents.json').read())

#translate API
translate_client = translate.Client()

#tts API
tts_client = texttospeech_v1.TextToSpeechClient()
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    speaking_rate=.75
)

#voice input library and API
r = sr.Recognizer()

#function to generate voice output
def generate_reply(sentence, accent):
    synthesis_input = texttospeech_v1.SynthesisInput(text=sentence)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=accent,
        ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE
    )

    response1 = tts_client.synthesize_speech(
        input = synthesis_input,
        voice = voice,
        audio_config = audio_config
    )
    with open('reply.mp3', 'wb') as output1:
        output1.write(response1.audio_content)

    playsound('reply.mp3')
    os.remove('reply.mp3')


print('------------------------ LINGUALITY ------------------------')
spokenLanguage = ""
userTurn = True

while True:
    userTurn = not userTurn
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        if userTurn == True:
            print('Waiting for you to finish saying the response...')
            audio = r.listen(source)
            continue
        print('Waiting for their response...')
        audio = r.listen(source)

    try:
        text = r.recognize_google_cloud(audio)
        output = translate_client.translate(
            text,
            target_language="en"
        )

        output['translatedText'] = re.sub(r'[^A-Za-z ]+', '', output['translatedText'])

        print("They said ( in", lang[output['detectedSourceLanguage']], ") ->",  output['translatedText'])
        spokenLanguage = output['detectedSourceLanguage']

        ##CALCULATE RESPONSE AND ADD IT TO FULL VOICE OUTPUT
        ints = predict_class(output['translatedText'].lower())
        print(ints)
        res = get_response(ints, intents)
        print(res)
        fullVoiceOutput = "They said " + output['translatedText'] + "... You should reply with: "
        generate_reply(fullVoiceOutput, 'en')
        output = translate_client.translate(
            res,
            target_language=spokenLanguage
        )
        if output['translatedText'] != output['input']:
            print("You should reply with:", output['translatedText'])
            print("Which means:", output['input'])
        else:
            print("You should reply with:", output['translatedText'])
        generate_reply(output['translatedText'], spokenLanguage)
    except sr.UnknownValueError:
        print("Linguality did not understand what they said")
        if spokenLanguage == "": #NO PRIOR LANGUAGE KNOWN YET
            print("You should reply with: huh?")
            message = "I did not understand them. You should reply with..."
            generate_reply(message, 'en')
            generate_reply('huh', 'en')

        else: #GETS PRIOR LANGUAGE
            text = "what?"
            output = translate_client.translate(
            text,
            target_language=spokenLanguage
            )
            message = "I did not understand them. You should reply with: "
            print("You should reply with:", output['translatedText'])
            #change language
            generate_reply(message, 'en')
            generate_reply(output['translatedText'], spokenLanguage)
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))


import speech_recognition as sr
from playsound import playsound
import os
import sys
import string
import re
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech_v1
from supportedLanguages import lang

sys.tracebacklimit = 0
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\Zenpa\OneDrive\Documents\Class Assignments\CS173\Final Project\Linguality\credentials.json"

#translate API
translate_client = translate.Client()

#tts API
tts_client = texttospeech_v1.TextToSpeechClient()
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3
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

spokenLanguage = ""
userTurn = True

while True:
    userTurn = not userTurn
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        if userTurn == True:
            print('Waiting you to finish saying the response...')
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

        #print("Google Cloud thinks they said", output)

        print("They said ( in", lang[output['detectedSourceLanguage']], ") ->",  output['translatedText'])
        spokenLanguage = output['detectedSourceLanguage']

        fullVoiceOutput = "They said " + output['translatedText'] + "... You should reply with: " #INSERT RESPONSE HERE
        ##CALCULATE RESPONSE AND ADD IT TO FULL VOICE OUTPUT

        #tts API
        synthesis_input = texttospeech_v1.SynthesisInput(text=fullVoiceOutput)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code='en',
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
    except sr.UnknownValueError:
        print("Linguality did not understand what they said")
        if spokenLanguage == "":
            print("You should reply with: huh?")
            message = "I did not understand them. You should reply with..."
            generate_reply(message, 'en')
            generate_reply('huh', 'en')

        else:
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


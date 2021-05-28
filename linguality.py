import speech_recognition as sr
import os
import sys
import string
import re
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
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

with sr.Microphone() as source:
    print('Say something: ')
    audio = r.listen(source)

try:
    text = r.recognize_google_cloud(audio)
except sr.UnknownValueError:
    print("Linguality did not understand what you said")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))

output = translate_client.translate(
    text,
    target_language="en"
)

output['translatedText'] = re.sub(r'[^A-Za-z ]+', '', output['translatedText'])

print("Google Cloud thinks they said", output)

print("They said ( in", lang[output['detectedSourceLanguage']], ") ->",  output['translatedText'])

fullVoiceOutput = "They said " + output['translatedText'] + "... You should say: " #INSERT RESPONSE HERE
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

with open('audio file1.mp3', 'wb') as output1:
    output1.write(response1.audio_content)
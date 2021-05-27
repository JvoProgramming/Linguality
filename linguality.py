import speech_recognition as sr
from langdetect import detect

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say something: ')
    audio = r.listen(source)

text = r.recognize_google(audio)
language = detect(text)

#SUPPORTED LANGUAGES
if language == 'en':
    language += '-US'
elif language == 'es':
    language += '-ES'
elif language == 'ja':
    language += '-JP'
elif language += 'hi':
    language += '-IN'
elif language += 'it':
    language += '-IT'
elif language += 'vi':
    language += '-VN'

print(r.recognize_google(audio))
print(language)
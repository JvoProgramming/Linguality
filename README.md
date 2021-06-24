# Linguality

Linguality.py is a python script (built using NLP tools) that allows English speakers to have a conversation in a foreign language. It records a microphone input from your conversation partner (e.g. a non-English speaker) and translates it for you to understand what they said. Once the translation is finished, it generates a response from chatbot.py using the intents.json file. This suggested response is then generated back to the conversation partner's language and outputted to the user, so he/she can use the generated response to reply to their partner. This python script is built using the Speech Recognition (for the microphone inputs and speech-to-text), Google API's (which allow it to translate sentences in a variety of languages), and the PlaySound library (to output and export text-to-speech files).

Be sure to install all required modules before running!

Also, make sure to replace the .json directory in linguality.py with your own google API's .json file

If there is a problem with the client authorization, try running:
pip install oauth2client

Before running linguality.py, please run training.py

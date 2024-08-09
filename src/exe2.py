import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
import playsound
from gtts import gTTS
import subprocess

# language = 'en'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
# openai.api_key='  '
load_dotenv()
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
# engine = pyttsx3.init("dummy")
# voice = engine.getProperty('voices')[1]
# engine.setProperty('voice', voice.id)
# name = "YOUR NAME HERE"
# greetings = [f"whats up master {name}",
#              "yeah?",
#              "Well, hello there, Master of Puns and Jokes - how's it going today?",
#              f"Ahoy there, Captain {name}! How's the ship sailing?",
#              f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                # engine.say(np.random.choice(greetings))
                # engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)
            myobj = gTTS(text = response_text, lang='en')
            filename="test.wav"
            #myobj.save("test.wav")
            myobj.save(filename)
            playsound.playsound(filename)
            # os.system("aplay test.wav")
            # Speak the response
            print("speaking")
            # os.system("espeak ' "+response_text + "'")
            # engine.say(response_text)
            # engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        # except sr.RequestError as e:
        #     print(f"Could not request results; {e}")
        #     engine.say(f"Could not request results; {e}")
        #     engine.runAndWait()
        #     listen_for_wake_word(source)
        #     break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)

    #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
import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
#import pyttsx3
import numpy as np
import playsound
import pyaudio
from gtts import gTTS
import subprocess

# language = 'en'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
openai.api_key='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'
load_dotenv()
# model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
# r = sr.Recognizer()
# name = "Social Tech Lab"
# greetings = [f"Welcome to {name}",
#              "yeah",
#              "Well, hello there, how's it going today?",
#              f"Ahoy there, Captain {name}! How's the ship sailing?",
#              f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]

#loding Vosk model
model_path = "/home/socialtech/vosk-model-ja-0.22"  
model = Model(model_path) 

recognizer=KaldiRecognizer(model,16000)

#capturing audio using pyaudio
cap=pyaudio.PyAudio()
stream= cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True,frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)

    
   
    if recognizer.AcceptWaveform(data):
        promt=recognizer.Result()
        print(promt)
        # Send input to OpenAI API
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{promt}"}])
        response_text = response.choices[0].message.content
        print(response_text)
        myobj = gTTS(text = response_text, lang='ja')
        filename="test.wav"
            #myobj.save("test.wav")
        myobj.save(filename)
        playsound.playsound(filename)
            # os.system("aplay test.wav")
            # Speak the response
        print("speaking")
         


# Load the Vosk model for Japanese (or download it if not available)

# Listen for the wake word "hey pos"
# def listen_for_wake_word(source):
#     print("Listening for 'Hey'...")

   
#     while True:
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             if "hey" in text.lower():
#                 print("Wake word detected.")
#                 myobj1 = gTTS(text = np.random.choice(greetings), lang='en')
#                 g="testg.wav"
#                 myobj1.save(g)
#                 playsound.playsound(g)

#                 break
#         except sr.UnknownValueError:
#             pass
# # Listen for input and respond with OpenAI API
# def listen_and_respond(source):
#     print("Listening...")

#     while True:
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             print(f"You said: {text}")
#             if not text:
#                 continue

#             # Send input to OpenAI API
#             response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
#             response_text = response.choices[0].message.content
#             print(response_text)
#             myobj = gTTS(text = response_text, lang='en')
#             filename="test.wav"
#             #myobj.save("test.wav")
#             myobj.save(filename)
#             playsound.playsound(filename)
          
#             print("speaking")
           
#             if not audio:
#                 listen_for_wake_word(source)
#         except sr.UnknownValueError:
#             time.sleep(20)
#             print("Silence found, shutting up, listening...")
#             listen_for_wake_word(source)
#             break

       

# Use the default microphone as the audio source
# with sr.Microphone() as source:
#     listen_for_wake_word(source)

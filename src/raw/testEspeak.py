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


openai.api_key='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'
load_dotenv()

#loding Vosk model
model_path = "/home/socialtech/vosk-model-ja-0.22"  
model = Model(model_path) 

recognizer=KaldiRecognizer(model,16000)
r = sr.Recognizer()


def listen_for_wake_word(source):
    print("Listening for 'Hello'...")
   
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")                
                myobj1 = gTTS(text = np.random.choice(greetings), lang='en')
                g="testg.wav"
                myobj1.save(g)
                playsound.playsound(g)
                break
        except sr.UnknownValueError:
            pass
def listen_and_respond(source):
    print("starting in english")
    print("Listening...")

    while True:
        audio = r.listen(source)
        text = r.recognize_google(audio)
        if recognizer.AcceptWaveform(text):
            promt=recognizer.Result()
            print(promt)




with sr.Microphone() as source:
    listen_for_wake_word(source)


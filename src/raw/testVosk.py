import os
import wave
import json
from vosk import Model, KaldiRecognizer
import pyaudio

# # Load the Vosk model for Japanese (or download it if not available)
# model_path = "/home/socialtech/OllamaMedVoice/model/vosk-model-small-ja-0.22"  
# model = Model(model_path) 

# # Open the audio file
# wf = wave.open("test.wav", "rb")

# # Set up the recognizer
# rec = KaldiRecognizer(model, wf.getframerate())


# # Process the audio
# while True:
#     data = wf.readframes(4000)
#     if len(data) == 0:
#         break
#     if rec.AcceptWaveform(dat-a):
#         result = rec.Result()
#         print(json.loads(result)["text"])

# # Final recognition result
# final_result = rec.FinalResult()
# print(json.loads(final_result)["text"])


model_path = "/home/socialtech/OllamaMedVoice/model/vosk-model-small-ja-0.22"  
model = Model(model_path) 

recognizer=KaldiRecognizer(model,4000)

cap=pyaudio.PyAudio()
stream= cap.open(format=pyaudio.paInt16, channels=1,rate=4000,input=True,frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
         print(recognizer.Result())

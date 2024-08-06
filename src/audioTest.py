import os
import playsound
import speech_recognition as sr
from gtts import gTTS

# from io import BytesIO
# mp3_fp = BytesIO()
# tts = gTTS('hello', lang='en')
# tts.write_to_fp(mp3_fp)

def speak(text):
    tts= gTTS(text=text, lang='es', tld='co.in')
    filename='voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

speak("秋の日本は、まるで絵画のように美しい季節です。朝晩の冷え込みが増し、山々が色とりどりの紅葉に染まります。日本の秋ならではの楽しみです。")
# 紅葉の名所として知られる京都の嵐山や奈良の東大寺の周辺では、赤や黄色、オレンジの葉が鮮やかに輝き、観光客や地元の人々を魅了します。秋の空は澄み渡り、高く青く広がり、まるで無限のキャンバスのようです。田んぼでは収穫の時期を迎え、金色の稲穂が風に揺れています。収穫祭や秋祭りも各地で催され、伝統的な踊りや音楽、地元の特産品が楽しめます。秋の味覚といえば、栗や柿、梨、そして松茸などの旬の食材が豊富です。焚き火の香りが漂う中、焼き芋を頬張りながら秋の深まりを感じることができるのも、

import pyttsx3

engine = pyttsx3.init()

engine.setProperty("voice", "Japanese")

#rate = engine.getProperty("rate")
#print(f"rate: {rate}")
engine.setProperty("rate", 130)

while (1):
    txt = "ひらがなで文字をにゅうりょくしてください"

    #print(f"text is: [{txt}]")
    if txt == None or len(txt) == 0:
        exit()
    engine.say(txt)
    engine.runAndWait()

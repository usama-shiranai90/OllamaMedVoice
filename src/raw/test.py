import speech_recognition as sr

# Function to recognize speech
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for the wake word 'hey'...")
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio)
        return response.lower()
    except sr.RequestError:
        print("API unavailable")
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    return ""

def main():
    recognizer = sr.Recognizer()
    # Use the index of your microphone device
    mic_index = 1  # Change this index based on your arecord -l output
    microphone = sr.Microphone(device_index=mic_index)

    while True:
        detected_word = recognize_speech_from_mic(recognizer, microphone)
        if "hey" in detected_word:
            print("Wake word detected! Listening for your prompt...")
            prompt = recognize_speech_from_mic(recognizer, microphone)
            print("You said: {}".format(prompt))

if __name__ == "__main__":
    main()

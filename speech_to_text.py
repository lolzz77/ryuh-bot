import speech_recognition as sr

def speech_to_text():
    sr.Microphone.list_microphone_names()
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        print(text)

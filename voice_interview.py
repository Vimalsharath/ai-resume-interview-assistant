import speech_recognition as sr
import pyttsx3


def speak(text):

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)


    try:

        answer = recognizer.recognize_google(audio)

        return answer


    except:

        return "Unable to recognize"


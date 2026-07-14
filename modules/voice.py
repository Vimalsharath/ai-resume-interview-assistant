import speech_recognition as sr
import pyttsx3



def speak(text):

    engine = pyttsx3.init()

    engine.setProperty(
        "rate",
        150
    )

    engine.say(text)

    engine.runAndWait()



def listen():

    recognizer = sr.Recognizer()


    with sr.Microphone() as source:


        print("Adjusting microphone...")


        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )


        print("Listening...")


        try:

            audio = recognizer.listen(
                source,
                timeout=30,
                phrase_time_limit=120
            )


        except sr.WaitTimeoutError:

            return "No speech detected"



    try:


        answer = recognizer.recognize_google(
            audio
        )


        return answer



    except sr.UnknownValueError:

        return "Could not understand speech"



    except sr.RequestError:

        return "Speech service unavailable"
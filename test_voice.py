from modules.voice import listen, speak


speak("Hello, please introduce yourself")


answer = listen()


print("You said:")
print(answer)
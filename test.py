# import subprocess

# result = subprocess.run('say "Hello, world!"')


import pyttsx3

engine = pyttsx3.init()

engine.say('Hello, world!')
engine.runAndWait()
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import pyttsx3
import webbrowser
import datetime

# -------------------- VOICE ENGINE --------------------
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # change to voices[1] for female

# -------------------- SPEECH RECOGNIZER --------------------
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

# -------------------- SPEAK FUNCTION --------------------
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------- LISTEN FUNCTION --------------------
def listen():
    print("Listening...")
    duration = 5
    fs = 16000

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav.write(f.name, fs, recording)
        filename = f.name

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    os.remove(filename)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        speak("Internet issue.")
        return ""

# -------------------- COMMAND PROCESSING --------------------
def process_command(command):

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + time)

    elif "open calculator" in command:
        speak("Opening calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening notepad")
        os.system("notepad")

    elif "exit" in command or "quit" in command:
        speak("Goodbye")
        exit()

    else:
        speak("I don't know that yet")

# -------------------- MAIN PROGRAM --------------------
speak("Hello, I am Jarvis. How can I help you?")

while True:
    command = listen()
    if command:
        process_command(command)

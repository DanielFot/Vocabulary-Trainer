import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 100
r.dynamic_energy_threshold = True

with sr.Microphone() as source:
    print("🎧 Say one short word:")
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.listen(source, phrase_time_limit=2)
    print("Processing...")

print("You said:", r.recognize_google(audio))

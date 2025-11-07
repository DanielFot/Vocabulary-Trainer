import random
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator
from difflib import SequenceMatcher

# Optional sound feedback

# --- WORDS DATABASE ---
WORDS = {
    "easy": {
        "Haus": "house",
        "Hund": "dog",
        "Katze": "cat",
        "Baum": "tree",
        "Auto": "car"
    },
    "medium": {
        "Schule": "school",
        "Freund": "friend",
        "Buch": "book",
        "Fenster": "window",
        "Garten": "garden"
    },
    "hard": {
        "Gesellschaft": "society",
        "Wissenschaft": "science",
        "Erfahrung": "experience",
        "Möglichkeit": "possibility",
        "Entwicklung": "development"
    }
}

# --- Fun facts to make the game engaging ---
FUN_FACTS = [
    "🇩🇪 'Fernweh' means the desire to travel to distant places!",
    "Did you know? The German word 'Gift' actually means poison 😱",
    "The longest German word ever printed was 79 letters long!",
    "German and English share about 60% of their vocabulary roots.",
    "‘Danke’ means thank you — a good word to remember! 🙌"
]

# --- Game Class ---
class GermanWordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 German Pronunciation Challenge")
        self.root.geometry("700x500")
        self.root.configure(bg="#1a1a2e")

        self.translator = Translator()
        self.recognizer = sr.Recognizer()

        self.score = 0
        self.mistakes = 0
        self.difficulty = tk.StringVar(value="easy")

        # --- UI Elements ---
        self.title_label = tk.Label(root, text="🇩🇪 German → English Pronunciation Game 🇬🇧",
                                    font=("Helvetica", 18, "bold"), bg="#1a1a2e", fg="#f5f5f5")
        self.title_label.pack(pady=20)

        # Difficulty selection
        tk.Label(root, text="Choose your difficulty:", bg="#1a1a2e", fg="#cccccc", font=("Arial", 12)).pack()
        diff_frame = tk.Frame(root, bg="#1a1a2e")
        diff_frame.pack(pady=5)
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(diff_frame, text=level.capitalize(), variable=self.difficulty,
                           value=level, bg="#1a1a2e", fg="#f5f5f5",
                           selectcolor="#222", font=("Arial", 11)).pack(side="left", padx=10)

        # Word to translate
        self.word_label = tk.Label(root, text="Press Start to begin!",
                                   font=("Helvetica", 20, "bold"), bg="#1a1a2e", fg="#ffd369")
        self.word_label.pack(pady=40)

        # Lives indicator (❤️ hearts)
        self.lives_label = tk.Label(root, text="❤️❤️❤️", font=("Arial", 20), bg="#1a1a2e", fg="#ff4d4d")
        self.lives_label.pack()

        # Buttons
        self.start_button = tk.Button(root, text="Start Game 🎮", command=self.start_game,
                                      bg="#00adb5", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)

        self.speak_button = tk.Button(root, text="Speak Now 🎤", command=self.listen_to_player,
                                      bg="#393e46", fg="white", font=("Arial", 12, "bold"), state="disabled")
        self.speak_button.pack(pady=10)

        # Status + score
        self.status_label = tk.Label(root, text="", font=("Arial", 14),
                                     bg="#1a1a2e", fg="#f8b400")
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14),
                                    bg="#1a1a2e", fg="#eeeeee")
        self.score_label.pack(pady=5)

    # --- Game Logic ---
    def start_game(self):
        self.score = 0
        self.mistakes = 0
        self.update_lives()
        self.score_label.config(text="Score: 0")
        self.status_label.config(text="")
        self.next_word()
        self.speak_button.config(state="normal")

    def next_word(self):
        level = self.difficulty.get()
        self.current_german, self.correct_english = random.choice(list(WORDS[level].items()))
        self.word_label.config(text=f"Translate this word:\n🇩🇪 {self.current_german}")

    def listen_to_player(self):
        self.status_label.config(text="🎧 Listening... please speak!")
        self.root.update()

        try:
            with sr.Microphone() as source:
                self.recognizer.energy_threshold = 80
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=2)

            try:
                user_text = self.recognizer.recognize_google(audio)
                self.check_answer(user_text.lower())
            except sr.UnknownValueError:
                self.status_label.config(text="😕 Didn't understand you, try again.")
            except sr.RequestError:
                self.status_label.config(text="🌐 Connection problem with speech API.")
            except Exception as e:
                self.status_label.config(text=f"⚠️ Error: {e}")

        except Exception as e:
            self.status_label.config(text=f"🎙️ Microphone error: {e}")

    def check_answer(self, user_text):
        ratio = SequenceMatcher(None, user_text.lower(), self.correct_english.lower()).ratio()
        if ratio > 0.75:
            self.score += 10
            self.status_label.config(text=f"✅ Correct! '{self.correct_english}'\n{random.choice(FUN_FACTS)}")
        else:
            self.mistakes += 1
            self.status_label.config(text=f"❌ Wrong! You said '{user_text}'. Correct: '{self.correct_english}'")

        self.score_label.config(text=f"Score: {self.score}")
        self.update_lives()

        if self.mistakes >= 3:
            messagebox.showinfo("💀 Game Over", f"Game Over! Final Score: {self.score}")
            self.speak_button.config(state="disabled")
        else:
            self.root.after(2500, self.next_word)

    def update_lives(self):
        hearts = "❤️" * (3 - self.mistakes) + "🤍" * self.mistakes
        self.lives_label.config(text=hearts)

# --- MAIN ---
if __name__ == "__main__":
    root = tk.Tk()
    game = GermanWordGame(root)
    root.mainloop()
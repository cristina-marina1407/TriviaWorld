import tkinter as tk
from tkinter import messagebox
import json
import random
import os
from PIL import Image, ImageTk

TOTAL_LEVELS = 10
QUESTIONS_PER_LEVEL = 5
QUESTION_FILE = 'questions.json'
BACKGROUND_IMAGE = 'world.jpg'

def load_questions():
    if not os.path.exists(QUESTION_FILE):
        messagebox.showerror("Error", f"The file '{QUESTION_FILE}' was not found!")
        exit()

    with open(QUESTION_FILE, 'r', encoding='utf-8') as f:
        try:
            questions = json.load(f)
            if not isinstance(questions, list) or len(questions) == 0:
                raise ValueError
            return questions
        except:
            messagebox.showerror("Error", f"The file '{QUESTION_FILE}' is invalid or empty!")
            exit()

all_questions = load_questions()

def get_random_questions(num):
    return random.sample(all_questions, num)

class TriviaWorlds:
    def __init__(self, master):
        self.master = master
        master.title("TriviaWorlds")
        master.geometry("800x600")

        self.bg_image = Image.open(BACKGROUND_IMAGE)
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(master, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.current_level = 1
        self.correct_answers = 0
        self.level_status = [None for _ in range(TOTAL_LEVELS)]

        self.show_start_screen()

    def show_start_screen(self):
        self.clear_screen()
        self.set_background()

        label = tk.Label(self.master, text="Welcome to TriviaWorlds!", font=("Comic Sans MS", 32, "bold"), bg="#f0f8ff")
        label.place(relx=0.5, rely=0.2, anchor="center")

        start_button = tk.Button(self.master, text="Start Game", font=("Comic Sans MS", 18), bg="#4CAF50", fg="white",
                                 width=15, height=2, command=self.show_level_map)
        start_button.place(relx=0.5, rely=0.4, anchor="center")

    def show_level_map(self):
        self.clear_screen()
        self.set_background()

        label = tk.Label(self.master, text="Select a Level", font=("Comic Sans MS", 24, "bold"), bg="#f0f8ff")
        label.pack(pady=20)

        self.levels_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.levels_frame.pack()

        self.level_buttons = []

        for i in range(1, TOTAL_LEVELS + 1):
            btn = tk.Button(self.levels_frame, text=f"Level {i}", width=12, height=2,
                            font=("Comic Sans MS", 14, "bold"),
                            command=lambda i=i: self.start_level(i))
            btn.grid(row=(i - 1) // 5, column=(i - 1) % 5, padx=10, pady=10)
            self.level_buttons.append(btn)

        self.update_level_colors()

    def start_level(self, level):
        self.current_level = level
        self.correct_answers = 0

        self.current_questions = get_random_questions(QUESTIONS_PER_LEVEL)
        self.current_question_index = 0

        self.show_question()

    def show_question(self):
        self.clear_screen()
        self.set_background()

        if self.current_question_index >= QUESTIONS_PER_LEVEL:
            self.finish_level()
            return

        self.current_question = self.current_questions[self.current_question_index]

        label = tk.Label(self.master, text=self.current_question["question"], font=("Arial", 20, "bold"),
                         wraplength=700, bg="#f0f8ff")
        label.pack(pady=30)

        self.selected_answer = tk.StringVar()

        options = ['A', 'B', 'C', 'D']
        for opt in options:
            text = f"{opt}. {self.current_question[opt]}"
            btn = tk.Radiobutton(self.master, text=text, variable=self.selected_answer, value=opt, font=("Arial", 16),
                                 bg="#f0f8ff")
            btn.pack(anchor="w", padx=150)

        submit_btn = tk.Button(self.master, text="Submit Answer", font=("Comic Sans MS", 16, "bold"), bg="#2196F3",
                               fg="white", command=self.check_answer)
        submit_btn.pack(pady=30)

    def check_answer(self):
        selected = self.selected_answer.get()
        correct = self.current_question["answer"]

        if selected == "":
            messagebox.showwarning("Warning", "Please select an answer before continuing!")
            return

        if selected == correct:
            self.correct_answers += 1
            messagebox.showinfo("Correct!", "Good job! ✅")
        else:
            correct_text = f"{correct}. {self.current_question[correct]}"
            messagebox.showerror("Wrong!", f"Wrong answer! ❌ The correct one was: {correct_text}")

        self.current_question_index += 1
        self.show_question()

    def finish_level(self):
        self.clear_screen()
        self.set_background()

        if self.correct_answers == QUESTIONS_PER_LEVEL:
            message = "Level passed! 😊"
            self.level_status[self.current_level - 1] = "passed"
        else:
            message = f"Level failed! 😢 You answered {self.correct_answers}/{QUESTIONS_PER_LEVEL} correctly."
            self.level_status[self.current_level - 1] = "failed"

        label = tk.Label(self.master, text=message, font=("Comic Sans MS", 26), bg="#f0f8ff")
        label.pack(pady=40)

        back_btn = tk.Button(self.master, text="Back to Level Map", font=("Comic Sans MS", 16), bg="#4CAF50",
                             fg="white", command=self.show_level_map)
        back_btn.pack(pady=10)

        if all(status == 'passed' for status in self.level_status):
            self.show_victory_animation()

    def show_victory_animation(self):
        self.clear_screen()
        self.set_background()

        label = tk.Label(self.master, text="Congratulations! You completed TriviaWorlds! 🎉",
                         font=("Comic Sans MS", 28, "bold"), bg="#f0f8ff", fg="gold")
        label.pack(pady=50)

    def update_level_colors(self):
        for idx, status in enumerate(self.level_status):
            if status == "passed":
                self.level_buttons[idx].config(bg="lightgreen", fg="black")
            elif status == "failed":
                self.level_buttons[idx].config(bg="tomato", fg="white")
            else:
                self.level_buttons[idx].config(bg="lightgray", fg="black")

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def set_background(self):
        self.background_label = tk.Label(self.master, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaWorlds(root)
    root.mainloop()
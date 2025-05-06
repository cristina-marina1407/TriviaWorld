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
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 768
BG_FADE = 0.4

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
        master.attributes('-fullscreen', True)
        master.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
        master.resizable(True, True)

        self.original_bg = Image.open(BACKGROUND_IMAGE).convert('RGB')
        base = self.original_bg.resize((DEFAULT_WIDTH, DEFAULT_HEIGHT), Image.Resampling.LANCZOS)

        faded = Image.blend(base, Image.new('RGB', base.size, 'white'), BG_FADE)
        self.bg_photo = ImageTk.PhotoImage(faded)

        self.background_label = tk.Label(master, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        master.bind('<Configure>', self._on_resize)
        master.bind('<Escape>', lambda e: master.attributes('-fullscreen', False))

        self.current_level = 1
        self.correct_answers = 0
        self.level_status = [None] * TOTAL_LEVELS

        self.show_start_screen()

    def _on_resize(self, event):
        if event.widget == self.master:
            w, h = event.width, event.height

            base = self.original_bg.resize((w, h), Image.Resampling.LANCZOS)
            faded = Image.blend(base, Image.new('RGB', base.size, 'white'), BG_FADE)

            self.bg_photo = ImageTk.PhotoImage(faded)
            self.background_label.config(image=self.bg_photo)

    def show_start_screen(self):
        self.clear_screen()
        self.set_background()

        label = tk.Label(self.master,
                         text="Welcome to TriviaWorlds!",
                         font=("Comic Sans MS", 48, "bold"),
                         bg="#f0f8ff")
        label.place(relx=0.5, rely=0.2, anchor="center")

        start_button = tk.Button(self.master,
                                 text="Start Game",
                                 font=("Comic Sans MS", 24, "bold"),
                                 bg="#4CAF50", fg="white",
                                 width=20, height=3,
                                 command=self.show_level_map)
        start_button.place(relx=0.5, rely=0.4, anchor="center")

    def show_level_map(self):
        self.clear_screen()
        self.set_background()

        label = tk.Label(self.master,
                         text="Select a Level",
                         font=("Comic Sans MS", 36, "bold"),
                         bg="#f0f8ff")
        label.pack(pady=30)

        self.levels_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.levels_frame.pack(pady=20)

        self.level_buttons = []
        for i in range(1, TOTAL_LEVELS + 1):
            btn = tk.Button(self.levels_frame,
                            text=f"Level {i}",
                            font=("Comic Sans MS", 20, "bold"),
                            width=14, height=3,
                            command=lambda i=i: self.start_level(i))
            btn.grid(row=(i - 1) // 5,
                     column=(i - 1) % 5,
                     padx=15, pady=15)
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

        q = self.current_questions[self.current_question_index]
        lbl_q = tk.Label(self.master,
                         text=q["question"],
                         font=("Arial", 28, "bold"),
                         wraplength=self.master.winfo_width() - 200,
                         bg="#f0f8ff")
        lbl_q.pack(pady=40)

        self.selected_answer = tk.StringVar()
        for opt in ['A', 'B', 'C', 'D']:
            text = f"{opt}. {q[opt]}"
            btn = tk.Radiobutton(self.master,
                                 text=text,
                                 variable=self.selected_answer,
                                 value=opt,
                                 font=("Arial", 24),
                                 anchor="w",
                                 bg="#f0f8ff",
                                 padx=20,
                                 pady=10)
            btn.pack(fill='x', padx=200, pady=5)

        submit_btn = tk.Button(self.master,
                               text="Submit Answer",
                               font=("Comic Sans MS", 24, "bold"),
                               bg="#2196F3", fg="white",
                               width=20, height=2,
                               command=self.check_answer)
        submit_btn.pack(pady=40)

    def check_answer(self):
        sel = self.selected_answer.get()
        correct = self.current_questions[self.current_question_index]["answer"]
        if not sel:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        if sel == correct:
            self.correct_answers += 1
            messagebox.showinfo("Correct!", "Good job! ✅")
        else:
            text = self.current_questions[self.current_question_index][correct]
            messagebox.showerror("Wrong!", f"❌ Correct answer was: {correct}. {text}")
        self.current_question_index += 1
        self.show_question()

    def finish_level(self):
        self.clear_screen()
        self.set_background()
        passed = self.correct_answers == QUESTIONS_PER_LEVEL
        self.level_status[self.current_level - 1] = 'passed' if passed else 'failed'

        if passed:
            msg = f"Level passed! 😊 {self.correct_answers}/{QUESTIONS_PER_LEVEL}"
            lbl = tk.Label(self.master,
                           text=msg,
                           font=("Comic Sans MS", 48),
                           bg="#f0f8ff", fg="green")
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            map_btn = tk.Button(self.master,
                                text="Back to Level Map",
                                font=("Comic Sans MS", 24),
                                bg="#4CAF50", fg="white",
                                width=20, height=2,
                                command=self.show_level_map)
            map_btn.place(relx=0.5, rely=0.8, anchor="center")
            map_btn.lift()
        else:
            msg = f"Level failed! 😢 {self.correct_answers}/{QUESTIONS_PER_LEVEL}"
            lbl = tk.Label(self.master,
                           text=msg,
                           font=("Comic Sans MS", 48),
                           bg="#f0f8ff", fg="red")
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            map_btn = tk.Button(self.master,
                                text="Back to Level Map",
                                font=("Comic Sans MS", 24),
                                bg="#4CAF50", fg="white",
                                width=20, height=2,
                                command=self.show_level_map)
            map_btn.place(relx=0.5, rely=0.8, anchor="center")
            map_btn.lift()

        if all(s == 'passed' for s in self.level_status):
            self.show_victory_animation()

    def start_next_level(self):
        next_level = self.current_level + 1
        if next_level <= TOTAL_LEVELS:
            if hasattr(self, 'canvas'):
                self.canvas.destroy()
            self.start_level(next_level)
        else:
            self.show_victory_animation()

    def _create_confetti(self):
        import random
        self.confetti_items = []
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        for _ in range(100):
            x = random.randint(0, w)
            y = random.randint(-h, 0)
            size = random.randint(5, 15)
            color = random.choice(colors)
            oval = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')
            speed = random.uniform(2, 5)
            self.confetti_items.append({'id': oval, 'speed': speed})
        self._animate_confetti()

    def _animate_confetti(self):
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        for item in self.confetti_items:
            self.canvas.move(item['id'], 0, item['speed'])
            x0, y0, x1, y1 = self.canvas.coords(item['id'])
            if y0 > h:
                self.canvas.coords(item['id'], x0, -10, x1, -10 + (y1 - y0))
        self.master.after(50, self._animate_confetti)

    def show_victory_animation(self):
        self.clear_screen()
        self.set_background()

        lbl = tk.Label(self.master,
                       text="Congratulations! You completed TriviaWorlds! 🎉",
                       font=("Comic Sans MS", 36, "bold"),
                       bg="#f0f8ff", fg="gold")
        lbl.pack(pady=60)

        self.canvas = tk.Canvas(self.master, bg="#f0f8ff", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._create_confetti()

    def update_level_colors(self):
        for idx, status in enumerate(self.level_status):
            btn = self.level_buttons[idx]
            if status == 'passed': btn.config(bg='lightgreen')
            elif status == 'failed': btn.config(bg='tomato')
            else: btn.config(bg='lightgray')

    def clear_screen(self):
        for w in self.master.winfo_children():
            if w is not self.background_label:
                w.destroy()

    def set_background(self):
        if hasattr(self, 'bg_photo'):
            self.background_label.config(image=self.bg_photo)
            self.background_label.lower()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaWorlds(root)
    root.mainloop()
    root = tk.Tk()
    app = TriviaWorlds(root)
    root.mainloop()

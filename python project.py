# -----------------------------------------------------------
# Intelligent Tutoring System — python Edition
# Author: Kunal Badhan | Chandigarh University
# -----------------------------------------------------------
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, os, random, time
import matplotlib.pyplot as plt
import networkx as nx

DATA_FILE = "data.json"

# ---------- Splash Screen ----------
def show_splash(root):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("500x300+450+250")

    # create gradient
    canvas = tk.Canvas(splash, width=500, height=300)
    canvas.pack()
    for i in range(300):
        color = "#%02x%02x%02x" % (173, 216 - i//4, 230)
        canvas.create_line(0, i, 500, i, fill=color)

    canvas.create_text(250, 140, text="Intelligent Tutoring System",
                       font=("Helvetica", 18, "bold"), fill="navy")
    canvas.create_text(250, 180, text="AI Edition", font=("Helvetica", 14), fill="darkblue")
    root.withdraw()
    splash.update()
    root.after(2500, splash.destroy)
    root.after(2500, root.deiconify)

# ---------- Data Management ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        data = {
            "AI Tools": {"score": 0, "attempts": 0},
            "ADBMS": {"score": 0, "attempts": 0},
            "Python Programming": {"score": 0, "attempts": 0}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
        return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Sample Quiz Bank ----------
QUIZ_DATA = {
    "AI Tools": [
        {"type": "mcq", "question": "Which of these is an AI framework by Google?",
         "options": ["TensorFlow", "React", "Bootstrap", "Docker"], "answer": "TensorFlow"},
        {"type": "text", "question": "Name one popular AI programming language.", "answer": "python"},
        {"type": "mcq", "question": "What does NLP stand for?",
         "options": ["Natural Language Processing", "Neural Logic Program", "Network Learning Process", "None"],
         "answer": "Natural Language Processing"}
    ],
    "ADBMS": [
        {"type": "mcq", "question": "Which of these is an example of an ADBMS?",
         "options": ["Oracle 12c", "MS Word", "Google Chrome", "Photoshop"], "answer": "Oracle 12c"},
        {"type": "text", "question": "What does ADBMS stand for?", "answer": "advanced database management system"},
        {"type": "mcq", "question": "Which command retrieves data from a database?",
         "options": ["SELECT", "DELETE", "INSERT", "UPDATE"], "answer": "SELECT"}
    ],
    "Python Programming": [
        {"type": "mcq", "question": "Which keyword is used to define a function in Python?",
         "options": ["def", "function", "define", "fun"], "answer": "def"},
        {"type": "text", "question": "What symbol is used for comments in Python?", "answer": "#"},
        {"type": "mcq", "question": "Which library is used for numerical computation?",
         "options": ["NumPy", "Pandas", "Tkinter", "Flask"], "answer": "NumPy"}
    ]
}

# ---------- Main App ----------
class IntelligentTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Tutoring System — AI Edition")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.data = load_data()

        style = ttk.Style()
        style.theme_use("clam")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.study_tab = ttk.Frame(self.notebook)
        self.quiz_tab = ttk.Frame(self.notebook)
        self.performance_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.study_tab, text="📘 Study")
        self.notebook.add(self.quiz_tab, text="🧠 Quiz")
        self.notebook.add(self.performance_tab, text="📊 Performance")

        self.setup_study_tab()
        self.setup_quiz_tab()

    # ---------- Study Tab ----------
    def setup_study_tab(self):
        ttk.Label(self.study_tab, text="Select Subject and Add Study Material:",
                  font=("Segoe UI", 12, "bold")).pack(pady=10)
        self.subject_var = tk.StringVar(value="AI Tools")
        subjects = list(QUIZ_DATA.keys())
        ttk.Combobox(self.study_tab, textvariable=self.subject_var, values=subjects,
                     state="readonly").pack(pady=5)

        self.file_list = tk.Listbox(self.study_tab, height=8)
        self.file_list.pack(pady=10, fill="x", padx=50)

        ttk.Button(self.study_tab, text="Attach Study File", command=self.add_file).pack(pady=5)
        ttk.Button(self.study_tab, text="Open Selected File", command=self.open_file).pack(pady=5)

    def add_file(self):
        fpath = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx *.pptx")])
        if fpath:
            self.file_list.insert(tk.END, fpath)
            messagebox.showinfo("File Added", "File attached successfully for study!")

    def open_file(self):
        sel = self.file_list.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a file to open.")
            return
        path = self.file_list.get(sel)
        os.startfile(path)

    # ---------- Quiz Tab ----------
    def setup_quiz_tab(self):
        ttk.Label(self.quiz_tab, text="Choose a Subject to Begin Quiz:",
                  font=("Segoe UI", 12, "bold")).pack(pady=10)
        self.quiz_subject = tk.StringVar(value="AI Tools")
        subjects = list(QUIZ_DATA.keys())
        ttk.Combobox(self.quiz_tab, textvariable=self.quiz_subject, values=subjects,
                     state="readonly").pack(pady=5)
        ttk.Button(self.quiz_tab, text="Start Quiz", command=self.start_quiz).pack(pady=15)
        self.quiz_frame = ttk.Frame(self.quiz_tab)
        self.quiz_frame.pack(pady=20)

    def start_quiz(self):
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        subject = self.quiz_subject.get()
        qlist = random.sample(QUIZ_DATA[subject], len(QUIZ_DATA[subject]))
        self.current = 0
        self.correct = 0
        self.questions = qlist
        self.show_question()

    def show_question(self):
        for w in self.quiz_frame.winfo_children():
            w.destroy()
        if self.current >= len(self.questions):
            self.end_quiz()
            return
        q = self.questions[self.current]
        ttk.Label(self.quiz_frame, text=f"Q{self.current + 1}. {q['question']}",
                  font=("Segoe UI", 11)).pack(pady=10)
        self.answer_var = tk.StringVar()

        if q["type"] == "mcq":
            for opt in q["options"]:
                ttk.Radiobutton(self.quiz_frame, text=opt, variable=self.answer_var, value=opt).pack(anchor="w", padx=40)
        else:
            ttk.Entry(self.quiz_frame, textvariable=self.answer_var, width=40).pack(pady=5)

        ttk.Button(self.quiz_frame, text="Submit", command=self.check_answer).pack(pady=15)

    def check_answer(self):
        ans = self.answer_var.get().strip().lower()
        q = self.questions[self.current]
        correct_ans = q["answer"].lower()
        if ans == correct_ans:
            self.correct += 1
        self.current += 1
        self.show_question()

    def end_quiz(self):
        total = len(self.questions)
        score = int((self.correct / total) * 100)
        subject = self.quiz_subject.get()
        self.data[subject]["attempts"] += 1
        self.data[subject]["score"] = int((self.data[subject]["score"] + score) / 2)
        save_data(self.data)

        msg = "Excellent! You're ready for harder topics." if score > 80 else \
              "Good effort! Revise and retry for better results." if score > 50 else \
              "Needs improvement. Review study material and retry."
        messagebox.showinfo("Quiz Completed",
                            f"Your Score: {score}%\n\n{msg}")
    # ---------- Performance Tab ----------
    def setup_performance_tab(self):
        for widget in self.performance_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.performance_tab, text="Performance Overview",
                  font=("Segoe UI", 12, "bold")).pack(pady=10)

        ttk.Button(self.performance_tab, text="Show Bar Chart", command=self.show_bar_chart).pack(pady=5)
        ttk.Button(self.performance_tab, text="Show Pie Chart", command=self.show_pie_chart).pack(pady=5)
        ttk.Button(self.performance_tab, text="Show Knowledge Graph", command=self.show_knowledge_graph).pack(pady=5)
        ttk.Button(self.performance_tab, text="Show Recommendations", command=self.show_recommendations).pack(pady=5)

    def show_bar_chart(self):
        subjects = list(self.data.keys())
        scores = [self.data[s]["score"] for s in subjects]
        plt.figure(figsize=(6, 4))
        plt.bar(subjects, scores)
        plt.title("Performance by Subject")
        plt.ylabel("Average Score (%)")
        plt.xlabel("Subjects")
        plt.ylim(0, 100)
        plt.show()

    def show_pie_chart(self):
        subjects = list(self.data.keys())
        scores = [max(self.data[s]["score"], 1) for s in subjects]  # avoid zero division
        plt.figure(figsize=(5, 5))
        plt.pie(scores, labels=subjects, autopct="%1.1f%%", startangle=90)
        plt.title("Overall Knowledge Distribution")
        plt.show()

    def show_knowledge_graph(self):
        G = nx.Graph()
        for s, d in self.data.items():
            G.add_node(s, score=d["score"])

        G.add_edges_from([
            ("AI Tools", "ADBMS"),
            ("AI Tools", "Python Programming"),
            ("ADBMS", "Python Programming")
        ])

        colors = []
        for node in G.nodes(data=True):
            sc = node[1]["score"]
            if sc >= 80:
                colors.append("green")
            elif sc >= 50:
                colors.append("orange")
            else:
                colors.append("red")

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000,
                font_color="white", font_size=10, font_weight="bold")
        plt.title("Knowledge Graph — Student Mastery Levels")
        plt.show()

    def show_recommendations(self):
        msg = "Personalized Study Recommendations:\n\n"
        for s, d in self.data.items():
            score = d["score"]
            if score >= 80:
                rec = "Advance to complex topics or practical applications."
            elif score >= 50:
                rec = "Revise core concepts and practice medium-level exercises."
            else:
                rec = "Revisit basics and go through easier study material."
            msg += f"{s}: {rec}\n"
        messagebox.showinfo("Recommendations", msg)


# ---------- Main Program ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligentTutorApp(root)
    show_splash(root)
    app.setup_performance_tab()
    root.mainloop()

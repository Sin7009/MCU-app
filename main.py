import tkinter as tk
from tkinter import ttk
from src.gui.teacher_tab import TeacherFrame
from src.gui.plan_tab import PlanFrame
from src.database import init_db

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Расписание МГПУ - Администратор")
        self.geometry("800x600")

        # Initialize DB
        init_db()

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Teacher Tab
        self.teacher_tab = TeacherFrame(self.notebook)
        self.notebook.add(self.teacher_tab, text="Преподаватели")

        # Study Plan Tab
        self.plan_tab = PlanFrame(self.notebook)
        self.notebook.add(self.plan_tab, text="Учебный план")

if __name__ == "__main__":
    app = App()
    app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from src.database import add_teacher, get_all_teachers

class TeacherFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # --- Add Teacher Section ---
        lbl_frame = ttk.LabelFrame(self, text="Добавить преподавателя")
        lbl_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ttk.Label(lbl_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(lbl_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(lbl_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = ttk.Entry(lbl_frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(lbl_frame, text="Предпочтения:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_prefs = ttk.Entry(lbl_frame)
        self.entry_prefs.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_add = ttk.Button(lbl_frame, text="Добавить", command=self.on_add_teacher)
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # --- List Teachers Section ---
        list_frame = ttk.LabelFrame(self, text="Список преподавателей")
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Email", "Prefs"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="ФИО")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Prefs", text="Предпочтения")

        self.tree.column("ID", width=30)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=100)
        self.tree.column("Prefs", width=200)

        self.tree.pack(fill="both", expand=True)

        self.load_teachers()

    def on_add_teacher(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        prefs = self.entry_prefs.get()

        if not name:
            messagebox.showerror("Ошибка", "Введите имя преподавателя")
            return

        add_teacher(name, email, prefs)
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_prefs.delete(0, tk.END)

        self.load_teachers()
        messagebox.showinfo("Успех", "Преподаватель добавлен")

    def load_teachers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        teachers = get_all_teachers()
        for t in teachers:
            self.tree.insert("", "end", values=t)

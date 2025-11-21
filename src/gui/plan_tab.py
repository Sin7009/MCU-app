import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.logic.importer import import_study_plan_from_csv, create_sample_csv
from src.database import get_all_disciplines, get_all_teachers, assign_teacher_to_discipline, clear_disciplines

class PlanFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # --- Controls ---
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        btn_load = ttk.Button(control_frame, text="Загрузить план (CSV)", command=self.on_load_plan)
        btn_load.pack(side="left", padx=5)

        btn_sample = ttk.Button(control_frame, text="Создать пример CSV", command=self.on_create_sample)
        btn_sample.pack(side="left", padx=5)

        btn_clear = ttk.Button(control_frame, text="Очистить план", command=self.on_clear_plan)
        btn_clear.pack(side="left", padx=5)

        # --- Assignment Controls ---
        assign_frame = ttk.LabelFrame(self, text="Назначение преподавателя")
        assign_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        ttk.Label(assign_frame, text="Выберите дисциплину из списка выше, затем выберите преподавателя:").pack(anchor="w", padx=5, pady=5)

        self.teacher_var = tk.StringVar()
        self.teacher_combo = ttk.Combobox(assign_frame, textvariable=self.teacher_var, state="readonly")
        self.teacher_combo.pack(side="left", padx=5, pady=5)

        btn_assign = ttk.Button(assign_frame, text="Назначить", command=self.on_assign)
        btn_assign.pack(side="left", padx=5, pady=5)

        # --- Table ---
        self.tree = ttk.Treeview(self, columns=("ID", "Subject", "Hours", "Group", "Semester", "Teacher"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Subject", text="Дисциплина")
        self.tree.heading("Hours", text="Часы")
        self.tree.heading("Group", text="Группа")
        self.tree.heading("Semester", text="Семестр")
        self.tree.heading("Teacher", text="Преподаватель")

        self.tree.column("ID", width=30)
        self.tree.column("Subject", width=200)
        self.tree.column("Hours", width=50)
        self.tree.column("Group", width=80)
        self.tree.column("Semester", width=60)
        self.tree.column("Teacher", width=150)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Bindings and Load
        self.refresh_data()

    def refresh_data(self):
        # Refresh Table
        for item in self.tree.get_children():
            self.tree.delete(item)

        disciplines = get_all_disciplines()
        for d in disciplines:
            # d is (id, subject, hours, group, semester, teacher_name)
            # if teacher_name is None, put "Не назначен"
            values = list(d)
            if values[5] is None:
                values[5] = "Не назначен"
            self.tree.insert("", "end", values=values)

        # Refresh Teacher Combobox
        teachers = get_all_teachers()
        # Store teacher IDs
        self.teacher_map = {f"{t[1]} (ID: {t[0]})": t[0] for t in teachers}
        self.teacher_combo['values'] = list(self.teacher_map.keys())

    def on_load_plan(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filepath:
            try:
                import_study_plan_from_csv(filepath)
                self.refresh_data()
                messagebox.showinfo("Успех", "План загружен")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def on_create_sample(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filepath:
            try:
                create_sample_csv(filepath)
                messagebox.showinfo("Успех", f"Пример создан: {filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def on_clear_plan(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены? Это удалит все дисциплины."):
            clear_disciplines()
            self.refresh_data()

    def on_assign(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите дисциплину из списка")
            return

        teacher_str = self.teacher_var.get()
        if not teacher_str:
            messagebox.showwarning("Внимание", "Выберите преподавателя")
            return

        teacher_id = self.teacher_map.get(teacher_str)

        # Iterate over selected items (support multi-select assignment)
        for item in selected_item:
            discipline_values = self.tree.item(item, "values")
            discipline_id = discipline_values[0]

            assign_teacher_to_discipline(discipline_id, teacher_id)

        self.refresh_data()
        messagebox.showinfo("Успех", "Преподаватель назначен")

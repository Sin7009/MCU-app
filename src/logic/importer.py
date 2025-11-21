import csv
import os
from src.database import add_discipline, clear_disciplines

def import_study_plan_from_csv(filepath: str):
    """
    Reads a CSV file and populates the disciplines table.
    Expected CSV columns: Subject Name, Hours, Group Name, Semester
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)

        rows = list(reader)
        if not rows:
            return

        start_index = 0
        first_row = rows[0]

        # Heuristic: check if first row contains "subject" or "name" or "hours" (case-insensitive)
        # to determine if it is a header.
        is_header = False
        if len(first_row) > 0:
            first_cell = first_row[0].lower()
            if "subject" in first_cell or "name" in first_cell or "дисциплина" in first_cell:
                is_header = True

        if is_header:
            start_index = 1

        for i in range(start_index, len(rows)):
            row = rows[i]
            if len(row) < 4:
                continue

            subject = row[0].strip()
            try:
                hours = int(row[1].strip())
            except ValueError:
                hours = 0
            group = row[2].strip()
            try:
                semester = int(row[3].strip())
            except ValueError:
                semester = 1

            add_discipline(subject, hours, group, semester)

def create_sample_csv(filepath: str):
    """Creates a sample CSV file for testing."""
    data = [
        ["Subject Name", "Hours", "Group Name", "Semester"],
        ["Высшая математика", "72", "ИВТ-21", "1"],
        ["Программирование на Python", "108", "ИВТ-21", "1"],
        ["Философия", "36", "ИВТ-21", "2"],
        ["Базы данных", "72", "ПИ-20", "3"]
    ]
    with open(filepath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

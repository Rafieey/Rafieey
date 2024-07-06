"""
Fatemeh Rafiee /// rafie01

"""



import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

class ExamSystem:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.students, file, ensure_ascii=False, indent=4)

    def add_student(self, identifier, full_name, phone_number, father_name):
        if identifier not in self.students:
            self.students[identifier] = {
                'نام کامل': full_name,
                'شماره تلفن': phone_number,
                'نام پدر': father_name,
                'نمرات': {}
            }
            self.save_data()
            return True
        else:
            return False

    def add_score(self, identifier, exam_name, full_score, achieved_score):
        if identifier in self.students:
            percent = (achieved_score / full_score) * 100
            self.students[identifier]['نمرات'][exam_name] = {
                'نمره کل': full_score,
                'نمره کسب شده': achieved_score,
                'درصد': percent
            }
            self.save_data()
            return True
        else:
            return False

    def get_scores(self, identifier):
        return self.students.get(identifier, {}).get('نمرات', {})

    def get_total_percent(self, identifier):
        scores = self.get_scores(identifier).values()
        return sum(score['درصد'] for score in scores) / len(scores) if scores else 0

    def get_rankings(self):
        total_scores = {identifier: self.get_total_percent(identifier) * len(self.get_scores(identifier)) for identifier in self.students}
        sorted_students = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_students

    def get_exam_count(self, identifier):
        return len(self.get_scores(identifier))

    def get_total_exam_counts(self):
        exam_counts = {identifier: len(self.students[identifier]['نمرات']) for identifier in self.students}
        sorted_counts = sorted(exam_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_counts

    def search_student(self, identifier):
        if identifier in self.students:
            student_info = self.students[identifier]
            return f"نام کامل: {student_info['نام کامل']}\nشماره تلفن: {student_info['شماره تلفن']}\nنام پدر: {student_info['نام پدر']}"
        else:
            return "کد ملی یافت نشد."

class App:
    def __init__(self, root, exam_system):
        self.exam_system = exam_system
        self.root = root
        self.root.title("فاطمه رفیعی")

        # Frame for adding student
        self.frame_add_student = tk.LabelFrame(root, text="افزودن فرد")
        self.frame_add_student.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_id = tk.Label(self.frame_add_student, text="کد ملی:")
        self.label_id.grid(row=0, column=0, padx=5, pady=5)

        self.entry_id = tk.Entry(self.frame_add_student)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_full_name = tk.Label(self.frame_add_student, text="نام کامل:")
        self.label_full_name.grid(row=1, column=0, padx=5, pady=5)

        self.entry_full_name = tk.Entry(self.frame_add_student)
        self.entry_full_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_phone_number = tk.Label(self.frame_add_student, text="شماره تلفن:")
        self.label_phone_number.grid(row=2, column=0, padx=5, pady=5)

        self.entry_phone_number = tk.Entry(self.frame_add_student)
        self.entry_phone_number.grid(row=2, column=1, padx=5, pady=5)

        self.label_father_name = tk.Label(self.frame_add_student, text="نام پدر:")
        self.label_father_name.grid(row=3, column=0, padx=5, pady=5)

        self.entry_father_name = tk.Entry(self.frame_add_student)
        self.entry_father_name.grid(row=3, column=1, padx=5, pady=5)

        self.button_add_student = tk.Button(self.frame_add_student, text="افزودن فرد", command=self.add_student)
        self.button_add_student.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Frame for adding score
        self.frame_add_score = tk.LabelFrame(root, text="افزودن نمره")
        self.frame_add_score.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_exam = tk.Label(self.frame_add_score, text="نام آزمون:")
        self.label_exam.grid(row=0, column=0, padx=5, pady=5)

        self.entry_exam = tk.Entry(self.frame_add_score)
        self.entry_exam.grid(row=0, column=1, padx=5, pady=5)

        self.label_full_score = tk.Label(self.frame_add_score, text="نمره کل:")
        self.label_full_score.grid(row=1, column=0, padx=5, pady=5)

        self.entry_full_score = tk.Entry(self.frame_add_score)
        self.entry_full_score.grid(row=1, column=1, padx=5, pady=5)

        self.label_achieved_score = tk.Label(self.frame_add_score, text="نمره کسب شده:")
        self.label_achieved_score.grid(row=2, column=0, padx=5, pady=5)

        self.entry_achieved_score = tk.Entry(self.frame_add_score)
        self.entry_achieved_score.grid(row=2, column=1, padx=5, pady=5)

        self.button_add_score = tk.Button(self.frame_add_score, text="افزودن نمره", command=self.add_score)
        self.button_add_score.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for actions
        self.frame_actions = tk.LabelFrame(root, text="عملیات")
        self.frame_actions.pack(padx=10, pady=10, fill=tk.BOTH)

        self.button_show_rankings = tk.Button(self.frame_actions, text="نمایش رتبه‌بندی", command=self.show_rankings)
        self.button_show_rankings.pack(fill=tk.BOTH, padx=5, pady=5)

        self.button_show_exam_counts = tk.Button(self.frame_actions, text="نمایش تعداد آزمون‌ها", command=self.show_exam_counts)
        self.button_show_exam_counts.pack(fill=tk.BOTH, padx=5, pady=5)

        # Frame for searching student
        self.frame_search_student = tk.LabelFrame(root, text="جستجو بر اساس کد ملی")
        self.frame_search_student.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_search_id = tk.Label(self.frame_search_student, text="کد ملی:")
        self.label_search_id.grid(row=0, column=0, padx=5, pady=5)

        self.entry_search_id = tk.Entry(self.frame_search_student)
        self.entry_search_id.grid(row=0, column=1, padx=5, pady=5)

        self.button_search = tk.Button(self.frame_search_student, text="جستجو", command=self.search_student_info)
        self.button_search.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def add_student(self):
        identifier = self.entry_id.get()
        full_name = self.entry_full_name.get()
        phone_number = self.entry_phone_number.get()
        father_name = self.entry_father_name.get()
        
        if self.exam_system.add_student(identifier, full_name, phone_number, father_name):
            messagebox.showinfo("موفقیت", f"فردی {full_name} اضافه شد.")
        else:
            messagebox.showerror("خطا", f"فردی با کد ملی {identifier} از قبل وجود دارد.")

    def add_score(self):
        identifier = self.entry_id.get()
        exam_name = self.entry_exam.get()
        
        try:
            full_score = float(self.entry_full_score.get())
            achieved_score = float(self.entry_achieved_score.get())
            
            if self.exam_system.add_score(identifier, exam_name, full_score, achieved_score):
                messagebox.showinfo("موفقیت", f"نمره برای {identifier} در {exam_name} اضافه شد.")
            else:
                messagebox.showerror("خطا", f"کد ملی {identifier} یافت نشد.")
        except ValueError:
            messagebox.showerror("خطا", "نمره نامعتبر است. لطفاً اعداد معتبر وارد کنید.")

    def show_rankings(self):
        rankings = self.exam_system.get_rankings()
        rankings_text = "\n".join([f"{rank + 1}. {identifier}: {total_score:.2f} امتیاز" for rank, (identifier, total_score) in enumerate(rankings)])
        messagebox.showinfo("رتبه‌بندی", rankings_text)

    def show_exam_counts(self):
        total_exam_counts = self.exam_system.get_total_exam_counts()
        exam_counts_text = "\n".join([f"{identifier}: {count} آزمون" for identifier, count in total_exam_counts])
        messagebox.showinfo("تعداد آزمون‌ها", exam_counts_text)

    def search_student_info(self):
        identifier = self.entry_search_id.get()
        student_info = self.exam_system.search_student(identifier)
        messagebox.showinfo("جستجو بر اساس کد ملی", student_info)

if __name__ == '__main__':
    exam_system = ExamSystem()
    root = tk.Tk()
    app = App(root, exam_system)
    root.mainloop()

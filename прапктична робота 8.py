import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class StudentFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анкета студента")
        self.root.geometry("560x360")
        self.root.resizable(False, False)


        self.base_dir = os.path.dirname(os.path.abspath(__file__))


        info_frame = tk.LabelFrame(
            self.root, text="Особисті дані", padx=12, pady=10, font=("Arial", 10, "bold")
        )
        info_frame.place(x=15, y=15, width=270, height=270)

        student_data = [
            ("Прізвище, ім'я:", "Мовчан Арсеній"),
            ("Факультет:", "Інформаційних технологій"),
            ("Спеціальність:", "121 Інженерія ПЗ"),
            ("Курс / Група:", "3 курс, група ІК-51"),
            ("Тема проєкту:", "Посібник «Двійкова арифметика»"),
            ("Email:", "a.movchan@istu.edu.ua")
        ]

        for idx, (label_text, value_text) in enumerate(student_data):
            tk.Label(
                info_frame, text=label_text, font=("Arial", 9, "bold"), fg="#333"
            ).grid(row=idx * 2, column=0, sticky="w", pady=(2, 0))
            tk.Label(
                info_frame, text=value_text, font=("Arial", 9)
            ).grid(row=idx * 2 + 1, column=0, sticky="w", pady=(0, 4))


        self.photo_portrait = self._load_image("portrait")
        self.photo_artistic = self._load_image("artistic")


        if self.photo_portrait:
            self.lbl_portrait = tk.Label(self.root, image=self.photo_portrait, bd=2, relief="groove")
        else:
            self.lbl_portrait = tk.Label(
                self.root, text="ПОРТРЕТНЕ ФОТО\n(файл не знайдено)",
                bg="#217346", fg="white", font=("Arial", 11, "bold")
            )

        if self.photo_artistic:
            self.lbl_artistic = tk.Label(self.root, image=self.photo_artistic, bd=2, relief="groove")
        else:
            self.lbl_artistic = tk.Label(
                self.root, text="ХУДОЖНЄ ФОТО\n(файл не знайдено)",
                bg="#2b579a", fg="white", font=("Arial", 11, "bold")
            )




        btn_frame = tk.Frame(self.root)
        btn_frame.place(x=15, y=300, width=530, height=45)

        tk.Button(
            btn_frame, text="Показати портретне фото", width=23, bg="#e1f0ff",
            command=self.show_portrait
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame, text="Показати художнє фото", width=23, bg="#fff2cc",
            command=self.show_artistic
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame, text="Вихід", width=10,
            command=self.root.quit
        ).pack(side="right", padx=10)

    def _load_image(self, base_name):

        for ext in (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
            full_path = os.path.join(self.base_dir, base_name + ext)
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path).resize((210, 260))
                    return ImageTk.PhotoImage(img)
                except Exception as e:
                    messagebox.showerror("Помилка файлу", f"Не вдалося відкрити {full_path}:\n{e}")
                    return None
        return None

    def show_portrait(self):

        self.lbl_portrait.place(x=310, y=22, width=210, height=260)
        self.lbl_portrait.lift()

    def show_artistic(self):

        self.lbl_artistic.place(x=310, y=22, width=210, height=260)
        self.lbl_artistic.lift()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentFormApp(root)
    root.mainloop()
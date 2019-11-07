from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import os

class MainWindow(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.title("Face Recognition 3.14")
        self.geometry("1000x400")

        todo1 = tk.Label(self, text="Tugas Besar 2.0 Al-Jabar Geometri", bg="lightgrey", fg="black", pady=10)

        # self.tasks.append(todo1)

        # for task in self.tasks:
        #     task.pack(side=tk.TOP, fill=tk.X)

        # self.task_create = tk.Text(self, height=3, bg="white", fg="black")

        # self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        # self.task_create.focus_set()

        # self.bind("<Return>", self.add_task)

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        image1 = Image.open("9.jpg")
        image1 = image1.resize((270, 270), Image.ANTIALIAS)
        image1X = ImageTk.PhotoImage(image1)
        label1 = Label(self, image=image1X)
        label1.image = image1X
        label1.place(x=20, y=55)

        image2 = Image.open("4.png")
        image2 = image2.resize((270, 270), Image.ANTIALIAS)
        image2X = ImageTk.PhotoImage(image2)
        label2 = Label(self, image=image2X)
        label2.image = image2X
        label2.place(x=320, y=55)

    def Directory():
        filename = filedialog.askopenfilename(title='Choose Picture')
        return filename
	



    # def add_task(self, event=None):
    #     task_text = self.task_create.get(1.0,tk.END).strip()

    #     if len(task_text) > 0:
    #         new_task = tk.Label(self, text=task_text, pady=10)

    #         _, task_style_choice = divmod(len(self.tasks), 2)

    #         my_scheme_choice = self.colour_schemes[task_style_choice]

    #         new_task.configure(bg=my_scheme_choice["bg"])
    #         new_task.configure(fg=my_scheme_choice["fg"])

    #         new_task.pack(side=tk.TOP, fill=tk.X)

    #         self.tasks.append(new_task)

    #     self.task_create.delete(1.0, tk.END)
    def entry():
        E1 = Entry(self, text ="Input Top Match Number", bd =5)
        E1.pack(side = RIGHT)
        return E1.get()
    
if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()



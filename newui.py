from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import os
from newrunable import run
import numpy as np
objPic = ' '
window = Tk()
window.title("Face Recognition 3.14")
window.geometry("1000x400")
count = 0
L = np.array([])
option = True
entry = 0
def RunEuclidean():
    global entry
    global objPic
    global count
    count = 0
    ShowImageList(True,objPic,entry)
def RunCosine():
    global entry
    global objPic
    global count
    count = 0
    ShowImageList(False,objPic,entry)

def ShowImageListLanjutan():
    global L
    global count
    image2 = Image.open(L[count])
    image2 = image2.resize((270, 270), Image.ANTIALIAS)
    image2X = ImageTk.PhotoImage(image2)
    label2 = Label(window, image=image2X)
    label2.image = image2X
    label2.place(x=320, y=55)

def ShowImageList(option, address, top):
    global L
    L = np.copy(run(option, address, top))
    image2 = Image.open(L[0])
    image2 = image2.resize((270, 270), Image.ANTIALIAS)
    image2X = ImageTk.PhotoImage(image2)
    label2 = Label(window, image=image2X)
    label2.image = image2X
    label2.place(x=320, y=55)
    
def Next():
    global count
    count +=1
    ShowImageListLanjutan(count)

def Directory():
    filename = filedialog.askopenfilename(title='Choose Picture')
    return filename

def ImageProccess():
    global objPic
    objPic = Directory()
    image1 = Image.open(objPic)
    image1 = image1.resize((270, 270), Image.ANTIALIAS)
    image1X = ImageTk.PhotoImage(image1)
    label1 = Label(window, image=image1X)
    label1.image = image1X
    label1.place(x=20, y=55)


def getEntry():
    global entry
    entry =  eval(e1.get())

def Next():
    global count
    global L
    count+=1
    if count < len(L):
        ShowImageListLanjutan()


# Entri Top Number


tk.Label(window, text="Input Top Number").place(x = 800,  y = 130)
e1 = tk.Entry(window)
e1.place(x= 800, y = 150)

tk.Button(window, text='Show', command = getEntry).place(x= 700,  y= 150)

buttonFile = Button(window, text='Choose Image', command=ImageProccess).place(x=800, y=300)
buttonEuclidean = Button(window, text='Euclidean', command=RunEuclidean).place(x= 800,  y=200 )
buttonCos = Button(window, text='Cosine', command=RunCosine).place(x= 800,  y= 250)
buttonNext = Button(window, text = 'Next Result', command = Next).place(x = 600, y = 350)

# window.iconbitmap(r'/home/aufa/Desktop/Fix/panah.ico')
window.mainloop()

#!/usr/bin/python
import numpy as np
import cv2
import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import urllib
import sqlite3
import ttk
import tkMessageBox
from tkfilebrowser import askopendirnames
from tkFileDialog import askopenfilename, askdirectory

import os

url='http://192.168.1.116:8080/shot.jpg'
recognizedflag=0
#Set up GUI

root = tk.Tk()
root.geometry("1260x640+80+50")
root.resizable(width=False, height=False)

#Makes main window

root.wm_title("Floating Faces")
# root.config(background="#d9d9d9")

def quit_app():
    root.quit()

def setupDatabase():
    import VFR_GUI_DC


def insertDir (pathname, dirname, changed_dirname):
    conn = sqlite3.connect("dir.db")
    with conn:
        cur=conn.cursor()
        cur.execute("INSERT INTO Directorylist(pathname, dirname, changed_dirname) VALUES ('"+ pathname +"',' " + dirname + " ' ,' " + changed_dirname + " ' )")
        max_id = cur.lastrowid
        Id= max_id
    cmd = "SELECT * FROM Directorylist WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        #str(sname) = testname
        cmd = "UPDATE Directorylist SET pathname=' " + pathname + " ' WHERE ID=" + str(Id)
    else:
        #str(sname) = testname
        cmd = "INSERT INTO Directorylist(ID,pathname, dirname, changed_dirname) Values(" + str(Id) + ",' " + pathname + " ', ' " + dirname + " ', ' " + changed_dirname + " ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def getDir(dirname):
    con = sqlite3.connect("dir.db")
    cur= con.cursor()
    cur.execute("SELECT * FROM Directorylist WHERE dirname =?", (str(dirname),))
    rows = cur.fetchall()
    profile1 = ["0","1"]
    for row in rows:
        profile1 = row
    con.close()
    return profile1

def lockDir():
    global recognizedflag
    from VFR_GUI_recognizer import recognizedFace

    recognizedflag = recognizedFace()

    if recognizedflag==1:
        names = askopendirnames(initialdir=("/home/pragyan/Documents/Facial recognition main project/FFRec-GUI_edit/"),okbuttontext= ("Lock"),title=("Choose directory"),filetypes = (("HTML files", "*.html;*.htm")  ,("All files", "*.*") )
    )
        for name in names:
             print name
             hiddenname= os.path.split(name)
             os.rename(name, "../FFRec-GUI_edit/bin/."+hiddenname[1])
             insertDir(hiddenname[0], hiddenname[1],"asdfgh")
             pro= getDir(hiddenname[1])
             print(str(pro[1]))

    else:
        tkMessageBox.showwarning(
            "Unidentified face!",
            "A snapshot was taken!"
        )

def unlockDir():
    global recognizedflag
    from VFR_GUI_recognizer import recognizedFace

    recognizedflag = recognizedFace()
    if recognizedflag==1:
        names = askopendirnames(initialdir=("/home/pragyan/Documents/Facial recognition main project/FFRec-GUI_edit/"),okbuttontext= ("Unlock"),title=("Choose directory"),filetypes = (("HTML files", "*.html;*.htm")  ,("All files", "*.*") ))
        for name in names:
             print name
             hiddenname= os.path.split(name)
             hiddenname2= hiddenname[1].split(".")
             os.rename(name, hiddenname[0]+"/"+hiddenname2[1])
    else:
        tkMessageBox.showwarning(
            "Unidentified face!",
            "A snapshot was taken!"
        )

# Inserting background image
photos = PhotoImage(file="images/bg.png")
label= Label(root,image=photos)
label.grid(row=0,column=50, rowspan= 50,columnspan=100)
#Inserting logo image

# photo = PhotoImage(file="images/logo.gif")
# label= Label(root,image=photo)
# label.grid(row=2,column=50, padx=90,pady=50,rowspan= 30)

#FLOATING FACES text

# theLabel= tk.Label(root, text="FLOATING FACES",
#                    foreground="black",
#                    font="Helvetica 20 bold").grid(row=2, column=80, ipady=100, sticky=N)

# Button to call Dataset creator GUI


# foreground="ivory2"
# background="gray23"
theButton = tk.Button(text='Set it up',
                      command=setupDatabase,
                      activebackground='LightSteelBlue1',
                      foreground="ivory2",
                      background="light cyan",
                      font="Helvetica 14 bold ",
                      borderwidth=3)
theButton.grid(row=29, column=118, ipadx=15)
# Add image to set it up button
Image1=PhotoImage(file="images/sup.png")
theButton.config( image=Image1 )

# Opens directory listing

theButton = tk.Button(text='Lock app',
                      command=lockDir,
                      activebackground='LightSteelBlue1',
                      foreground="ivory2",
                      background="light cyan",
                      font="Helvetica 14 bold ",
                      borderwidth=4)
theButton.grid(row=29, column=128, ipadx=15)
# Add image to lock app button
Image2=PhotoImage(file="images/lockapps.png")
theButton.config( image=Image2 )

# Opens directory listing

theButton = tk.Button(text='Unlock app',
                      command=unlockDir,
                      activebackground='LightSteelBlue1',
                      foreground="ivory2",
                      background="light cyan",
                      font="Helvetica 14 bold",
                      borderwidth=4)
theButton.grid(row=29, column=138,ipadx=15)
# Add image to unlock app button
Image3=PhotoImage(file="images/ul.png")
theButton.config( image=Image3 )

# COPYRIGHT Label
#
# theLabel= tk.Label(root, text="(c) 2017 FLOATING FACES ALL RIGHTS RESERVED.",
#                    foreground="black",
#                    font="Helvetica 8 italic").grid(row=6, column=80)

# EXIT Button

theButton = tk.Button(text='Exit',
                      command=quit_app,
                      activebackground='LightSteelBlue1',
                      foreground="ivory2",
                      background="light cyan",
                      font="Helvetica 14 bold italic",
                      borderwidth=3)
theButton.grid(row=45, column=130, sticky=S, ipadx=36,columnspan=50)
# Add image to exit button
Image4=PhotoImage(file="images/exit.png")
theButton.config( image=Image4 )
#Starts GUI

root.mainloop()


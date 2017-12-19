import numpy as np
import cv2
import Tkinter as tk
from Tkinter import *
import Image, ImageTk
import urllib
import sqlite3
import ttk
import tkMessageBox

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('trainer/trainer.yml')

cascadePath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascadePath);

# #Set up GUI
# root = tk.Tk()
# root.geometry("1280x800")
# #Makes main window
# root.wm_title("Floating Faces")
# root.config(background="#00394d")
#
# #Graphics window
# imageFrame = tk.Frame(root, width=200, height=600)
# imageFrame.grid(row=0, column=0, padx=70, pady=100)
# # Button(root,text=tk.Frame = tk.LabelFrame"Submit").grid(row=3)
#
# #Capture video frames
# lmain = tk.Label(imageFrame)
# lmain.grid(row=0, column=0)
#

# Quits the TkInter app when called
def quit_app():
    root.quit()


# Opens a message box when called
def show_about(event=None):
    tkMessageBox.showwarning(
        "About",
        "This Awesome Program was Made in 2016"
    )

#
# # Create the menu object
# the_menu = Menu(root)
#
# # ----- FILE MENU -----
#
# # Create a pull down menu that can't be removed
# file_menu = Menu(the_menu, tearoff=0)
#
# # Add items to the menu that show when clicked
# # compound allows you to add an image
# file_menu.add_command(label="Open")
# file_menu.add_command(label="Save")
#
# # Add a horizontal bar to group similar commands
# file_menu.add_separator()
#
# # Call for the function to execute when clicked
# file_menu.add_command(label="Quit", command=quit_app)
#
# # Add the pull down menu to the menu bar
# the_menu.add_cascade(label="File", menu=file_menu)

# RECOGNIZER #

url='http://192.168.1.116:8080/shot.jpg'
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

def getProfile(Id):
    conn=sqlite3.connect("Faces1.0.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def recognizedFace():
    while True:
        global recognizedflag
        recognizedflag = 0

        imgResp=urllib.urlopen(url)

        #change into bytearray of unsigned integer type
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)

        #Decode numpy array to opencv2 image
        img=cv2.imdecode(imgNp,-1)

        # cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:

            Idu, conf = recognizer.predict(gray[y:y+h, x:x+w])
            cv2.putText(img,str(conf), (x, y + h + 120 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
            if (conf<100):
                recognizedflag=1
                break
                cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 2)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 225), 2)

            # cv2.imshow('frame', img)
            cv2.waitKey(1)
        return recognizedflag
#
# def recognizedFace():
#     print(recognizedflag)

#
# recognizedFace()

## VIDEO FEED ##
# def showFrame():
#
#     cv2image = recognizeFace()
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)
#     lmain.imgtk = imgtk
#     lmain.configure(image=imgtk)
#     lmain.after(10, showFrame)


#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(root, width=1000, height=200)
#sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

import numpy as np
import cv2
import sqlite3
import urllib

#Global variables
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 0, 0)
fontColor1 = (0, 0, 255)


url='http://192.168.0.108:8080/shot.jpg'
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
# path= 'dataSet'

def getProfile(Id):
    conn=sqlite3.connect("Faces1.0.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def recognizeFace():
    # while True:
    global fontFace
    global fontColor
    global fontColor
    global fontColor1
    fontColor1 = (0, 0, 255)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 0, 0)
    imgResp=urllib.urlopen(url)

    #change into bytearray of unsigned integer type
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)

    #Decode numpy array to opencv2 image
    img=cv2.imdecode(imgNp,-1)

    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:

        Idu, conf = recognizer.predict(gray[y:y+h, x:x+w])
        cv2.putText(cv2image,str(conf), (x, y + h + 120 ), fontFace, fontScale, fontColor1)
        if (conf<80):
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (225, 0, 0), 2)
            profile = getProfile(Idu)
            if(profile!=None):
                cv2.putText(cv2image, str(profile[1]), (x,y+h+30),fontFace, fontScale, fontColor)
                cv2.putText(cv2image, str(profile[3]), (x, y + h + 60), fontFace, fontScale, fontColor)
                cv2.putText(cv2image, str(profile[4]), (x, y + h + 90), fontFace, fontScale, fontColor)
                cv2.putText(cv2image, str(profile[5]), (x, y + h + 120), fontFace, fontScale, fontColor)
        else:
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 0, 225), 2)
            # cv2.putText(img,"Not Found", (x, y + h + 30 ), fontFace, fontScale, fontColor1)
        cv2.imshow('frame', cv2image)
        if ord('q') == cv2.waitKey(1):
          break
cv2.destroyAllWindows()
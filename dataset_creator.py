import numpy as np
import cv2
import sqlite3
import os
from PIL import Image
import urllib

sampleNum = 0
Id=0
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0, 0, 255)

url='http://192.168.1.180:8080/shot.jpg'
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#im = cv2.imread('images/testpragyan.jpg', cv2.IMREAD_COLOR)

def getImagesAndLabels(path):
    # Get all file path
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    # Initialize empty face sample
    faceSamples = []

    # Initialize empty id
    ids = []

    # Loop all the file path
    for imagePath in imagePaths:

        # Get the image and convert it to grayscale
        PIL_img = Image.open(imagePath).convert('L')

        # PIL image to numpy array
        img_numpy = np.array(PIL_img, 'uint8')

        # Get the image id
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # Get the face from the training images
        faces = detector.detectMultiScale(img_numpy)

        # Loop for each face, append to their respective ID
        for (x, y, w, h) in faces:
            # Add the image to face samples
            faceSamples.append(img_numpy[y:y + h, x:x + w])

            # Add the ID to IDs
            ids.append(id)

    # Pass the face array and IDs array
    return faceSamples, ids

def insertOrUpdate(Name):
    conn = sqlite3.connect("Faces1.0.db")
    with conn:
        cur=conn.cursor()
        cur.execute("INSERT INTO People(Name) VALUES ('"+ Name +"');")
        max_id = cur.lastrowid
        Id= max_id
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        #str(sname) = testname
        cmd = "UPDATE people SET Name=' " + "testname" + " ' WHERE ID=" + str(Id)
    else:
        #str(sname) = testname
        cmd = "INSERT INTO people(ID,Name) Values(" + str(Id) + ",' " + "testname" + " ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    return max_id

# sname=raw_input('Enter your name:')

# name =  "_".join(sname.lower().split(" "))
# Make directory
# Facespath="Faces database/" + name
# os.makedirs(Facespath)
Id = insertOrUpdate("testname")
def datasetCreate():
    global sampleNum
    sampleNum=0
    while(True):
        imgResp = urllib.urlopen(url)
        # change into bytearray of unsigned integer type
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        # Decode numpy array to opencv2 image
        img = cv2.imdecode(imgNp, -1)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            sampleNum= sampleNum + 1
            cv2.imwrite("Faces database/face-" + "testname" + "." + str(Id) + "."+ str(sampleNum)+".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(cv2image, (x - 50, y - 50), (x + w + 50, y + h + 50), (0, 225, 0), 2)
            # break if the sample number is more than 5
        if sampleNum > 5:

            break

    # Trainer
    # # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Get the faces and IDs
    faces, ids = getImagesAndLabels('Faces database/')

    # Train the model using the faces and IDs
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer.yml
    # with open('trainer.yml', "a") as recognizer:
    recognizer.write('trainer/trainer.yml')
    return 0

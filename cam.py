import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import os
import sys
import json

def new_user():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30

    raw_capture = PiRGBArray(camera, size=(640, 480))

    face_cascade = cv2.CascadeClassifier("haarcascade_face.xml")

    name = input("What's his/her Name? ")
    dirName = "./images/" + name
    print(dirName)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Profile created")
    else:
        print("Profile already exists!")
        sys.exit()
        
    song = input("What's your song?")
    pathSong = "./audio/" + song + ".mp3"
    print(pathSong)

    with open("user_profiles.json", "r") as user_profiles:
        #read the dict, add to the dict, overwrite the old dict
        user_dict = json.load(user_profiles)
        user_dict[name] = pathSong
    json.dump(user_dict, open("user_profiles.json", "w"))
    print(user_dict)
    user_profiles.close()

    count = 0
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        if count >= 30:
            break
        frame = frame.array
        # flips the camera
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
        for (x, y, w, h) in faces:
            roiGray = gray[y:y+h, x:x+w]
            fileName = dirName + "/" + name + str(count) + ".jpg"
            cv2.imwrite(fileName, roiGray)
            cv2.imshow("face", roiGray)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            count += 1

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        raw_capture.truncate(0)

        if key == 27:
            break
        
    cv2.destroyAllWindows()

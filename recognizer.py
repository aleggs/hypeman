import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep

import pygame
import json
import time

def run():
    relay_pin = [26]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.output(relay_pin, 0)

    with open('labels', 'rb') as f:
        dict = pickle.load(f)
        f.close()

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    raw_capture = PiRGBArray(camera, size=(640, 480))


    face_cascade = cv2.CascadeClassifier("haarcascade_face.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    font = cv2.FONT_HERSHEY_SIMPLEX


    init_time = 0
    playback_started = False
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        frame = frame.array
        # flips the camera
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roi_gray)
            highest_conf = 0
            for name, value in dict.items():
                if value == id_:
                    print(name + " conf: " + str(conf))
                    highest_conf = name

            if conf >= 70 and conf < 105:
                GPIO.output(relay_pin, 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, highest_conf + str(conf), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

                # music section
                with open("user_profiles.json", "r") as user_profiles:
                    user_dict = json.load(user_profiles)
                    try:
 
                        if (not playback_started):
                            song = user_dict[highest_conf]                    
                            pygame.mixer.init()
                            pygame.mixer.music.load(song)
                            pygame.mixer.music.play()
                            
                            init_time = time.time()
                            playback_started = True
                        if (playback_started):
                            curr_time = time.time()
                            if curr_time - init_time > 10:
                                playback_started = False
                                pygame.mixer.music.fadeout(5000)
                        #while pygame.mixer.music.get_busy() == True:
                            # pygame.time.Clock().tick(100000)
                            # break;
                        
                        # pygame.mixer.music.fadeout(20000)
                        
                    except KeyError:
                        print("Song not found! Please set up your user profile.")
                    

            else:
                GPIO.output(relay_pin, 0)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        raw_capture.truncate(0)

        if key == 27:
            break

    cv2.destroyAllWindows()

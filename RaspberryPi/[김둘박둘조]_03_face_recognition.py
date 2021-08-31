import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time

#from multiprocessing import Process
from threading import Thread

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

#----------buzzer ------------------------

buzzer = 11
#wrong = [7,7,5,5,6,7,7,5,5,6]
#
#scale = [261,294,329,349,392,440,493,523]

GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.LOW)

p=GPIO.PWM(buzzer,100)

rightCheck = 0
wrongCheck = 0

#--------------------------------------

#-------------------led--------------

red1 = 13
yellow = 15
green = 29
blue = 31
red2 = 33

#-------led setup----------

GPIO.setup(red1, GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(yellow, GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(green, GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(blue, GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(red2, GPIO.OUT,initial=GPIO.LOW)

rightLed=0
wrongLed=0

#-------------------------------------

recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('/home/pi/fdCam/trainer/trainer.yml')
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> loze: id=1,  

names = ['no','sojeong','hyejeong','zimin']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

#------------buzzer function-----------

def rightBuz():
    print("rightCheck")
    global p
    global rightCheck
    
    right = [400,440,400,360,329,294,261,530]
    
    rightCheck=rightCheck+1
    print(rightCheck)

    if(rightCheck == 10):
        try:
            p.start(70)
            p.ChangeDutyCycle(40)
            for j in range(1):
                for i in range(len(right)):
                    p.ChangeFrequency(right[i])
                    time.sleep(0.2)
                    if i == 6:
                        time.sleep(0.5)
        finally:
            p.stop()
            rightCheck=0

def wrongBuz():
    global p
    global wrongCheck
    
    wrong = [440,400,440,400,294,261,294,261]

    wrongCheck=wrongCheck+1
            
    if (wrongCheck ==10):
        try:
            p.start(70)
            p.ChangeDutyCycle(30)
            for j in range(1):
                for i in range(len(wrong)):
                    p.ChangeFrequency(wrong[i])
                    time.sleep(0.3)
                    if i==3:
                        time.sleep(0.3)
        finally:
            p.stop()
            wrongCheck=0

def rightled():
    print("rightLED")
    global rightLed
    rightLed=rightLed+1
    print(rightLed)
    if rightLed == 10:
        for i in range(10):

            GPIO.output(yellow,GPIO.LOW)
            time.sleep(0.001)
            GPIO.output(green,GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(red1,GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(blue,GPIO.LOW)
            time.sleep(0.001)
            GPIO.output(red2,GPIO.HIGH)
            
            time.sleep(0.3)
            
            GPIO.output(red1,GPIO.LOW)
            time.sleep(0.001)
            GPIO.output(yellow,GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(green,GPIO.LOW)
            time.sleep(0.001)
            GPIO.output(blue,GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(red2,GPIO.LOW)
            
            time.sleep(0.3)
            
        else:
            GPIO.output(red1,GPIO.LOW)
            GPIO.output(yellow,GPIO.LOW)
            GPIO.output(green,GPIO.LOW)
            GPIO.output(blue,GPIO.LOW)
            GPIO.output(red2,GPIO.LOW)
        rightLed=0
        
def wrongled():
    print("wrong")
    global wrongLed
    wrongLed=wrongLed+1
    print(wrongLed)
    if wrongLed==10:
        GPIO.output(red1,GPIO.HIGH)
        GPIO.output(yellow,GPIO.LOW)
        GPIO.output(green,GPIO.LOW)
        GPIO.output(blue,GPIO.LOW)
        GPIO.output(red2,GPIO.HIGH)
        wrongLed=0
        
def rightMain():
    t1 = Thread(target = rightled)
    t2 = Thread(target = rightBuz)
    
    t1.start()
    print("t1start")
    t2.start()
    print("t2start")

def wrongMain():
    t1 = Thread(target = wrongled)
    t2 = Thread(target = wrongBuz)
    
    t1.start()
    print("t1start")
    t2.start()
    print("t2start")
#----------the number of people--------
knownUser=False
#unknownUser=0
#----------------------------------------
while True:
    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
                        
            knownUser = True
            rightMain()
            
        else :
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            
            #Process(target=wrongled).start()
            if knownUser==False:
                wrongMain()
            
      
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff
    # Press 'ESC' for exiting video
    if k == 27:
        p.stop()
        break
    knownUser=False
        
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
GPIO.cleanup()
#! /usr/bin/python
# import the necessary packages
import cv2
from imutils.video import VideoStream
import time
import pickle
import face_recognition
import imutils
import RPi.GPIO as GPIO
from mail import send_mail

threshold_time=10 #avoiding spam, will send message in minimum 10 seconds, and will update led in 10 seconds
threshold_frame=5 # for example %20

#sometimes system can make false detection, so i added "correctness rate" for make mor stabilized.
correction_u=0 #correctness of unknown person
correction_p=0 #correctness of known person

red_led=23
green_led=24

GPIO.setmode(GPIO.BCM) #gpio names
GPIO.setwarnings(False)

GPIO.setup(red_led,GPIO.OUT) #setmode
GPIO.setup(green_led,GPIO.OUT)

GPIO.output(green_led,GPIO.LOW)
GPIO.output(red_led,GPIO.LOW)

def take_photo():
    img_name = "photo.jpg"
    print('Taking a photo')
    cv2.imwrite(img_name, frame1)

#trained model
encoded_model = "trained_model.pickle"

#face detector xml file
cascade = "haarcascade_frontalface_default.xml"

# load models
print("Loading files...")
data = pickle.loads(open(encoded_model, "rb").read())
detector = cv2.CascadeClassifier(cascade)

print("Starting...")
vs = VideoStream(0).start() #start cam
time.sleep(2.0)

timer1= time.time() #for avoiding spam (counter)
timer2=threshold_time
timing=True #if it is true it means we can send mail.

while True:

    frame = vs.read()
    frame1=frame.copy()
    frame = imutils.resize(frame, width=500)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #gray for face detection
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #rgb for face recog

    # detect faces
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

    #boxe of face
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    #face data
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    if timer2-timer1>threshold_time: 
            timing=True
            GPIO.output(green_led,GPIO.LOW)
            GPIO.output(red_led,GPIO.LOW)  

    if not timing: 
        correction_u=0
        correction_p=0


    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["face_data_encode"],encoding)
        
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes 
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # which person's face is this ? 
            name = max(counts, key=counts.get)
                
        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
    
        banner=top-10 #dont write name too close to box
    
        if name!="Unknown":
            correction_p=correction_p+1  #max value is 5 (think like: if it is 1 -- it means %20, if it is 2 -- it means %40)
            #print("p:"+str(correction_p)) 

            cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2) #draw green box
        
            cv2.putText(frame, name, (left, banner), cv2.FONT_HERSHEY_SIMPLEX,.8, (0, 255, 0), 2) #draw green label

            if timing and correction_p==threshold_frame:
                
                take_photo()
                send_mail(name)

                GPIO.output(green_led,GPIO.HIGH)
                print("Green LED turning ON\n-----------") 
        
                correction_p=0
                timing=False
                timer1=timer2

        if name=="Unknown":
            correction_u=correction_u+1     
            #print("u:"+str(correction_u))

            cv2.rectangle(frame, (left, top), (right, bottom),(0, 0, 255), 2) #draw red box
        
            cv2.putText(frame, name, (left, banner), cv2.FONT_HERSHEY_SIMPLEX,.8, (0, 0, 255), 2)#draw red label

            if  timing and correction_u==threshold_frame:
                
                take_photo()
                send_mail(name)

                GPIO.output(red_led,GPIO.HIGH)
                print("Red LED turning ON\n-----------") 

                correction_u=0
                timing=False
                timer1=timer2
   
    # display frame
    cv2.imshow("Face Recognition", frame)

    timer2=time.time()

    key = cv2.waitKey(1) & 0xFF

    # if q pressed
    if key == ord("q"):
        GPIO.output(green_led,GPIO.LOW)
        GPIO.output(red_led,GPIO.LOW)  
        break

#clean
cv2.destroyAllWindows()
vs.stop()
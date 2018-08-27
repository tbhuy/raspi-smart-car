from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.conf import settings
import pi_motor2 as motor
import os
import cv2
# Create your views here.
def index(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render({},request))

def stream():

    cap=cv2.VideoCapture(0)
    print(settings.STATIC_ROOT)
    cascPath = os.path.join(settings.STATIC_ROOT,"haarcascade_frontalface_default.xml")
    faceCascade = cv2.CascadeClassifier("/home/pi/haarcascade_frontalface_default.xml")
    while True:
        ret,frame=cap.read()
        if not ret:
            print("Error")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

    # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)       
    
        cv2.imwrite('demo.jpg',frame)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+open('demo.jpg','rb').read())
              
def video_feed(resquest):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace;boundary=frame')

def run(request, direction):
    motor.run(direction)
    return HttpResponse("Running "+ direction)

def turn(request, direction):
    motor.turn(direction)
    return HttpResponse("Turned " + direction)

def stop(request):
    motor.stop()
    return HttpResponse("Stopped")

def speedAdjust(request, step):
    motor.speedAdjust(step)
    return HttpResponse("Speed adjusted")
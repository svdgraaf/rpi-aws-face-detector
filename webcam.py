import cv2
import threading
import sys
from datetime import datetime, timedelta
from PIL import Image
import io
import copy
import boto3

is_detecting = False

def detect_faces(image):
    global is_detecting
    client = boto3.client('rekognition', region_name='eu-west-1')
    resp = client.search_faces_by_image(
        Image={
            'Bytes': image
        },
        CollectionId='Sentia'
    )
    print resp
    if len(resp['FaceMatches']) > 0:
        for face in resp['FaceMatches']:
            print "%s: %s" % (face['Face']['ExternalImageId'], face['Face']['Confidence'])
            say_hi(face['Face']['ExternalImageId'])
    else:
        print "No faces DETECTED from collection"
    is_detecting = False

def say_hi(name):
    client = boto3.client('polly', region_name='eu-west-1')
    response = client.synthesize_speech(
        OutputFormat='mp3',
        SpeechMarkTypes=[
            'sentence'
        ],
        Text='Goodmorning %s' % name,
        TextType='text',
        VoiceId='Joanna'
    )
    print response

faceCascade = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

now = datetime.utcnow()
face_detected = False
detected_face = None

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    try:
        x,y,w,h = faces[0]
        # print x,y,w,h
        if x > 0 or y > 0:
            # detected_face = gray.copy()[y:(y+h), x:(x+h)]
            face_detected = True
        else:
            face_detected = False
    except:
        face_detected = False
        pass

    print 'is_detecting:', is_detecting
    if face_detected and not is_detecting:
        is_detecting = True
        img = Image.fromarray(frame)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG')
        t = threading.Thread(target=detect_faces, args=[imgByteArr.getvalue()])
        t.start()

    # Display the resulting frame
    cv2.imshow('Video', frame)
    cv2.moveWindow('Video', 0, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # print 'Took %s' % (datetime.utcnow() - now)
    now = datetime.utcnow()

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import pywhatkit
import face_recognition
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
'''
#now = datetime.now()
    #if now.hour==8 and now.minute==10:

# connection of database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="FlaskDb"
)

# Get the informations from db
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM students")

 # Create some lists for incoming informations from db
myresult = mycursor.fetchall()
known_face_encodings = []
known_face_names = []
# Use incoming informations that from db with for loop


for info in myresult:
    print(info[3])
    print(info[1])

# This is a app of running face recognition on live video from your webcam.
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.


# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this specific app.


# Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
    img = face_recognition.load_image_file(info[3])
    encoding = face_recognition.face_encodings(img)[0]


# Create arrays of known face encodings and their names
    known_face_encodings.append(encoding)
    known_face_names.append(info[1])
 
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
coming_names=[]
process_this_frame = True
count=0
while True:
    for info in myresult:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Taninamadi"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]


            # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                isthere=name in face_names
                if isthere==False:
                    if name!="Taninamadi":
                        face_names.append(name)

           # print(face_names) ------------------------------------------------------------------------------
        process_this_frame = not process_this_frame

    # Display the results
        for (top, right, bottom, left), name in zip(face_locations,face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

        # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

        # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    # Display the resulting image
        cv2.imshow('Video', frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
   #if time is equal to 09:15, break and quit!
    now = datetime.now()
    if now.hour==9 and now.minute==15:
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

print(face_names)
'''
#------------------------------------------------------------------------------------------------------------------------------------------------------

#def sendmsg():
pywhatkit.sendwhatmsg("+49"+"1774979723","Derslerimiz 15 dakika önce başlamıştır ve yüz tanıma sistemine göre çocuğunuz okula girmemiştir, bilginize...", 12, 8, 15, True, 2)
count=count+1

#-------------------------------------------------------------------------------------------------------------------------------------------------------
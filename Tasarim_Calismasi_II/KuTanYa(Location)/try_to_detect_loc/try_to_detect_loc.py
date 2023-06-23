# Libarries

import cv2
import numpy as np
import mysql.connector
import time
 

# Connection of database:
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="FlaskDb"
)

# Getting the informations from db:
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM objects")

 # Creating some lists for incoming informations from db:
myresult = mycursor.fetchall()
# Use incoming informations that from db with for loop:
for x in myresult:
    print(x[2])
    print(x[1])

######################################################################################################################
#---------------------------------------------------------------------------------------------------------------------
######################################################################################################################

def ref_photo_loc(photo):
    global ref_circles
    # Upload the image and flip it:
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # Open the image:
    kernel = np.ones((3,3), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    # Use the Hough transform method to detect circles:
    ref_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=48.51, minRadius=0, maxRadius=0)

    # Determine the positions of the circles:
    if ref_circles is not None:
        ref_circles = np.round(ref_circles[0, :]).astype("int")
        for (x, y, r) in ref_circles:
            print("Daire Merkezi: ({}, {})".format(x, y))
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
    return ref_circles

#--------------------------------------------------------------------------------------


def live_cam_loc(gray):
    global circles
    # Open the image:
    kernel = np.ones((3,3), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    # Use the Hough transform method to detect circles:
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=48.51, minRadius=0, maxRadius=0)

    # Determine the positions of the circles:
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            print("Daire Merkezi: ({}, {})".format(x, y))
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

    # Show the image:
    cv2.imshow('frame', frame)
    return circles




########################################################################################################################
#-----------------------------------------------------------------------------------------------------------------------
########################################################################################################################

# Find the positions of the circles in the reference photograph:
ref_photo_loc(x[2])

# Define arrays to hold the positions of the circles:
ref_circles_positions = []
detected_circles_positions = []
# Obtain the positions of the reference circles:
for circle in ref_circles:
    print(circle)
    x = int(circle[0])
    y = int(circle[1])
    ref_circles_positions.append((x, y))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 793)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 494)



while True:

    # Capture an image from the camera:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    live_cam_loc(gray)

    print("Daire Merkezi: ({}, {})".format(x, y))
    # Retrieve the positions of the detected circles:
    if circles is not None:
        for circle in circles:
            x = int(circle[0])
            y = int(circle[1])
            detected_circles_positions.append((x, y))

    # Perform the comparison:
    matched_circles = []
    for ref_circle_pos in ref_circles_positions:
        for detected_circle_pos in detected_circles_positions:
            dist = np.sqrt((ref_circle_pos[0] - detected_circle_pos[0])**2 + (ref_circle_pos[1] - detected_circle_pos[1])**2)
            if dist < 80:  # We can accept a certain margin of error:
                matched_circles.append(detected_circle_pos)
                break

    if len(matched_circles) == len(ref_circles_positions):
        text = "Daireler uyumlu (Dogru)"
        time.sleep(2)
        detected_circles_positions = []
    else:
        text = "Daireler uyumsuz (Yanlis)"

    # Print the results to the screen:
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    
    # To exit, press the 'q' key:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera connection:
cap.release()
# Close all windows:
cv2.destroyAllWindows()

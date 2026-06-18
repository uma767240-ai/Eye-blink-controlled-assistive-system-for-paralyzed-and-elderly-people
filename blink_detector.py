import cv2
import serial
import time

# 1. Setup Serial communication
# Make sure the port matches your Raspberry Pi (usually '/dev/ttyACM0' or '/dev/ttyUSB0')
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2) # Give connection time to stabilize
except:
    print("Could not connect to Arduino. Check port settings.")

# 2. Load pre-trained cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

print("Starting blink detection...")

while True:
    ret, img = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        
        # Logic: If no eyes are detected for a frame, send blink signal
        if len(eyes) == 0:
            print("Blink detected!")
            try:
                ser.write(b'1') # Sending '1' to Arduino
            except:
                pass
            time.sleep(0.5) # Prevent multiple triggers for one blink

    # Press 'q' to quit the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

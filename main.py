import cv2
from cv2 import VideoCapture
from cv2 import waitKey
import mediapipe as mp
import time

mp_hands = mp.solutions.hands #Detects hands
mp_draw = mp.solutions.drawing_utils #Use for drawing things

#Open camera
cap = cv2.VideoCapture(0)

#Get frame width and height
cap.set(3, 2560) #3 is the index of width
cap.set(4, 1600) #4 is the index of height

def main():
    print("Press 'q' to stop")
    while True:
        attempt = 0
        success, img = cap.read()

        #Allow the program to load the camera and capture the images for 5 tries, each time intervals is 0.2s
        while not success and attempt < 5:
            time.sleep(0.2)
            success, img = cap.read()
            attempt += 1
        if not success:
            print("failed to read frame")
            break

        img = cv2.flip(img, 1)

        cv2.imshow('Image', img)

        #Wait 1ms, in that time, if user presses 'q', break the function
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

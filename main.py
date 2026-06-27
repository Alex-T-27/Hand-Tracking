import cv2
import mediapipe as mp
import time

mp_face = mp.solutions.face_detection #Detects face
mp_hands = mp.solutions.hands #Detects hands
mp_draw = mp.solutions.drawing_utils #Use for drawing things

#Open camera
cap = cv2.VideoCapture(0)

#Get frame width and height
cap.set(3, 2560) #3 is the index of width
cap.set(4, 1600) #4 is the index of height

def main():
    print("Press 'q' to stop")
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,

        #The higher the more accurate, the less it can detect the hand
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5,
        ) as hands:
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
            height, width, _ = img.shape
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Switch format from BGR to RGB because OpenCV uses BGR as standard
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        img, 
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,

                    )

                    finger_tips = {
                        "Thumb": hand_landmarks.landmark[4],
                        "Index": hand_landmarks.landmark[8],
                        "Middle": hand_landmarks.landmark[12],
                        "Ring": hand_landmarks.landmark[16],
                        "Pinky": hand_landmarks.landmark[20],
                    }

                    for name, landmark in finger_tips.items():
                        #Convert normalized coordinates into pixel coordinates
                        x = int(landmark.x * width) 
                        y = int(landmark.y * height)

                        cv2.putText(
                            img,
                            name,
                            (x, y - 15),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5,
                            color=(255, 255, 255),
                            thickness=1,
                        )
                        
                        cv2.circle(
                            img,
                            (x, y),
                            5,
                            (0, 255, 0),
                            -1,

                        )

            cv2.imshow('Image', img)

            #Wait 1ms, in that time, if user presses 'q', break the function
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

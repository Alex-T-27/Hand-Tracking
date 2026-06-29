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
        ) as hands, \
        mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5,
        ) as face_detection:
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
            height, width, _ = img.shape #Scale the height and width with the size of the image
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Switch format from BGR to RGB because OpenCV uses BGR as standard
            hands_results = hands.process(rgb_frame)
            face_results= face_detection.process(rgb_frame)
            
            if face_results.detections:
                for detection in face_results.detections:
                    print("FACE DETECTED") 
                    
                    bbox = detection.location_data.relative_bounding_box 

                    box_x, box_y = int(bbox.xmin * width), int(bbox.ymin * height)

                    cv2.putText(
                        img,
                        "Alex the chud",
                        (box_x, box_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0,255,0),
                        2,

                    )
                    mp_draw.draw_detection(
                        img,
                        detection,
                    )

                    keypoints = detection.location_data.relative_keypoints
                    
                    face_parts = {
                        "Right_eye": keypoints[0],
                        "Left_eye": keypoints[1],
                        "Nose": keypoints[2],
                        "Mouth": keypoints[3],
                        "Right_ear": keypoints[4],
                        "Left_ear": keypoints[5],
                    }
                        
                    for parts, detection in face_parts.items():
                        face_x, face_y = int(detection.x * width), int(detection.y * height) 

                        print(f"{parts} is at \n{detection}")

                        cv2.circle(
                            img,
                            (face_x, face_y),
                            3,
                            (0, 255, 0),
                            -1,
                        )
            print("--------------------------------------------------------------------------------------------------------------------------------")

            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    print("HAND DETECTED")
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
                        hands_x = int(landmark.x * width) 
                        hands_y = int(landmark.y * height)

                        print(f"{name} is at \n{landmark}")
                         
                        cv2.putText(
                            img,
                            name,
                            (hands_x, hands_y - 15),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5,
                            color=(255, 255, 255),
                            thickness=1,
                        )
                        
                        cv2.circle(
                            img,
                            (hands_x, hands_y),
                            5,
                            (0, 255, 0),
                            -1,

                        )
                print("--------------------------------------------------------------------------------------------------------------------------------")

            cv2.imshow('Image', img)
            
            #Wait 1ms, in that time, if user presses 'q', break the function
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

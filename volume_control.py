import cv2
import mediapipe as mp
import numpy as np
import math
from pycaw.pycaw import AudioUtilities

# 1. CONNECTING TO WINDOWS AUDIO

devices = AudioUtilities.GetSpeakers()

# New Pycaw method
volume = devices.EndpointVolume

# 2. SETTING UP MEDIAPIPE HAND DETECTION

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 3. OPENING WEBCAM


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()


# 4. MAIN PROGRAM LOOP

while True:

    success, img = cap.read()

    if not success:
        print("ERROR: Could not read webcam.")
        break

    img = cv2.flip(img, 1)

    
    height, width, _ = img.shape

    
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    
    results = hands.process(rgb_img)


    # 5. IF A HAND IS DETECTED

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


        
            # 6. GETTING THUMB AND INDEX FINGER
            
            thumb = hand_landmarks.landmark[4]

            index = hand_landmarks.landmark[8]


            # Converting MediaPipe coordinates to pixels
            thumb_x = int(thumb.x * width)
            thumb_y = int(thumb.y * height)

            index_x = int(index.x * width)
            index_y = int(index.y * height)


          
            # 7. DRAWING POINTS
        

            cv2.circle(
                img,
                (thumb_x, thumb_y),
                10,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.circle(
                img,
                (index_x, index_y),
                10,
                (255, 0, 255),
                cv2.FILLED
            )


            # Drawing line between thumb and index
            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 0, 255),
                3
            )


          
            # 8. CALCULATING DISTANCE
       

            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )


            # 9. CONVERTING DISTANCE TO VOLUME
            


            volume_percent = np.interp(
                distance,
                [30, 250],
                [0, 100]
            )

            volume_percent = float(volume_percent)


            # Converting percentage to 0.0 - 1.0
            volume_level = volume_percent / 100.0


            # Setting Windows volume
            volume.SetMasterVolumeLevelScalar(
                volume_level,
                None
            )


            
            # 10. VOLUME BAR
      

            bar_y = int(
                np.interp(
                    volume_percent,
                    [0, 100],
                    [400, 100]
                )
            )


            # Outer volume bar
            cv2.rectangle(
                img,
                (50, 100),
                (90, 400),
                (255, 255, 255),
                3
            )


            # Filled volume bar
            cv2.rectangle(
                img,
                (50, bar_y),
                (90, 400),
                (255, 255, 255),
                cv2.FILLED
            )


        
            # 11. DISPLAYING VOLUME PERCENTAGE
        

            cv2.putText(
                img,
                f"Volume: {int(volume_percent)}%",
                (30, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )


          
            # 12. DISPLAYING DISTANCE
          
            cv2.putText(
                img,
                f"Distance: {int(distance)}",
                (30, 490),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )


 
    # 13. DISPLAYING CAMERA WINDOW
      cv2.imshow(
        "Hand Gesture Volume Control",
        img
    )

   

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



# 15. CLEANING UP

cap.release()
cv2.destroyAllWindows()
hands.close()

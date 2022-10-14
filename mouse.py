import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from typing import List
import autopy
from config_file import *


cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)
cap.set(10, 150)


w_screen, h_screen = autopy.screen.size()


detector = HandDetector(detectionCon=0.8, maxHands=1)


def function_click(previous_mode: str, clicking_mode: str, finger_1: List[int], finger_2: List[int],
                   distance_min: int) -> str:
    distance_array = detector.findDistance(finger_1, finger_2, img)
    distance, info = distance_array[0], distance_array[1]
    if distance < distance_min and previous_mode != clicking_mode:
        cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0), cv2.FILLED)
       
        if clicking_mode == "left_clicking":
            autopy.mouse.click(autopy.mouse.Button.LEFT)
        elif clicking_mode == "right_clicking":
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
        elif clicking_mode == "middle_clicking":
            autopy.mouse.click(autopy.mouse.Button.MIDDLE)
        previous_mode = clicking_mode
    elif distance >= distance_min:
        previous_mode = 'None'

    return previous_mode


if __name__ == '__main__':
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)

        if hands:
            lmList = hands[0]['lmList']
            xb, yb, wb, hb = hands[0]['bbox']
           
            x1, y1 = lmList[8]

            
            fingers_up = detector.fingersUp(hands[0])

            
            cv2.rectangle(img, (framR, framR), (w_cam - framR, h_cam - framR), (255, 0, 255), 2)

            
            if fingers_up == [0, 1, 0, 0, 0]:
                
                x3 = np.interp(x1, (framR, w_cam - framR), (0, w_screen))
                y3 = np.interp(y1, (framR, h_cam - framR), (0, h_screen))
                
                current_location_x = previous_location_x + (x3 - previous_location_x) / smoothening
                current_location_y = previous_location_y + (y3 - previous_location_y) / smoothening

                
                autopy.mouse.move(current_location_x, current_location_y)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                previous_location_x, previous_location_y = current_location_x, current_location_y

            
            elif fingers_up == [0, 1, 1, 0, 0]:
                previous_mode = function_click(previous_mode, 'left_clicking', lmList[8], lmList[12], 40)

            elif fingers_up == [0, 1, 1, 1, 0]:
                previous_mode = function_click(previous_mode, 'middle_clicking', lmList[8], lmList[16], 70)

            elif fingers_up == [1, 1, 0, 0, 0]:
                previous_mode = function_click(previous_mode, 'right_clicking', lmList[4], lmList[6], 100)

            
           

        cv2.imshow("Image", img)
        cv2.waitKey(1)

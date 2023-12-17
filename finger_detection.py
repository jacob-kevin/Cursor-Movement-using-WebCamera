import cv2
import mediapipe as mp
import pyautogui
import pywinauto
import time
from math import hypot

pyautogui.PAUSE = 0.001

def main():
    lmlist = []
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    screenWidth,screenHeight=pyautogui.size()

    while True:
        success, image = cap.read()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)
        lmlist = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])

                fingers = []
                # Check which fingers are raised
                for finger in range(1, 6):  # Finger indices 1 to 4 (thumb to pinky)
                    tip_id = finger * 4  # Each finger has 4 landmarks, and the tip landmark is at position 4
                    if lmlist[tip_id][2] < lmlist[tip_id - 2][2]:  # Compare y-coordinates of tip and base landmarks
                        fingers.append(1)  # Finger is raised
                    else:
                        fingers.append(0)  # Finger is not raised

                mode_selector(fingers,1.020-lm.x, lm.y,screenWidth,screenHeight,lmlist,image)

                # print("Raised Fingers:", fingers)
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
                cv2.imshow("Output", image)
                cv2.waitKey(1)

def mode_selector(finger,cx,cy,screenWidth,screenHeight,lmlist,image):
    xaxis=int(((cx) * screenWidth))
    yaxis=int(((cy) * screenWidth))
    current_x, current_y = pyautogui.position()
    print(xaxis,yaxis)



    if finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
        smooth_x, smooth_y = smooth_cursor_move(xaxis, yaxis, current_x, current_y)
        pyautogui.moveTo(smooth_x, smooth_y)
        time.sleep(0.1)
        if len(lmlist) > 20:
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]
            length = hypot(x2 - x1, y2 - y1)
            print("Pinch:",length)
            if length+10 < 49:
                pywinauto.mouse.press(button='left', coords=(xaxis, yaxis))
                status="Hold engaged"
                print(status)
            time.sleep(0.1)




    if  finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0 :
        pyautogui.click()




    if  finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0 :
        if len(lmlist) > 20 :
            x1,y1=lmlist[8][1],lmlist[8][2]
            x2,y2=lmlist[12][1],lmlist[12][2]
            length=hypot(x2-x1,y2-y1)
            print("Scroll:",length)
            if length > 49 :
                pyautogui.click(clicks=2)

            else :
                direction=int(540-cy/0.001)
                print(direction)
                pyautogui.scroll(direction,cx,cy)
                print("V.Scroll")

def smooth_cursor_move(target_x, target_y, current_x, current_y, smoothing_factor=0.5):
    smooth_x = int(current_x + smoothing_factor * (target_x - current_x))
    smooth_y = int(current_y + smoothing_factor * (target_y - current_y))
    return smooth_x, smooth_y
if __name__ == "__main__":
    main()

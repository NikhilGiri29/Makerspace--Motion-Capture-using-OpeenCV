############################################################################
# This File is the Keyboard input simulator which takes input depending on #
# the direction the user's hands is pointing. If running for the first     #
# time I suggest running with "SnakeGame.py" file. Though remember to keep #
# the snake game tab selected so that thee keyboard inputs are read there. #
# Enjoy!!!!                                                                #
############################################################################

#### Imports ####
import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
from pynput.keyboard import Key, Controller

keyboard = Controller()  # Simulating Keyboard Inputs

detector = htm.handsDetector()

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
flag = ''


thres = 150  # --> change it if any problem (Decrease if smoll hands, Increase if big hands)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
   
    temp = flag
    flag = detector.direction_hand(img, thres, 12, 0, flag)
    #### if hand is pointing down and the last input was not down ####
    if flag == 'd' and temp != flag:
        keyboard.press(Key.down)
        keyboard.release(Key.down)

    #### if hand is pointing up and the last input was not up ####
    elif flag == 'u' and temp != flag:
        keyboard.press(Key.up)
        keyboard.release(Key.up)

    #### if hand is pointing right and the last input was not right (IMAGE IS FLIPPED!!!!) ####
    elif flag == 'l' and temp != flag:
        keyboard.press(Key.right)
        keyboard.release(Key.right)

    #### if hand is pointing left and the last input was not left (IMAGE IS FLIPPED!!!!) ####
    elif flag == 'r' and temp != flag:
        keyboard.press(Key.left)
        keyboard.release(Key.left)

    #### fps calculations (Greater the better) ####
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

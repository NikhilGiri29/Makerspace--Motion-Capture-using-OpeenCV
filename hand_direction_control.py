
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
    '''
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        x = (lmList[12][1] - lmList[0][1])
        y = (lmList[12][2] - lmList[0][2])
        print(x, y)

        if y > thres and flag != 'd':
            print("==================down===========================")
            flag = 'd'

        elif y < -thres and flag != 'u':
            print("=================up===============================")
            flag = 'u'

        elif x > thres and flag != 'l':
            print("===============left===========================")
            flag = 'l'

        elif x < -thres and flag != 'r':
            print("===============right===========================")
            flag = 'r'
    '''

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

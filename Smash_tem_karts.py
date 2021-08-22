
#### Imports ####
import cv2
import time
import HandTrackingModule as htm
from pynput.keyboard import Key, Controller

keyboard = Controller()  # Simulating the keyboard presses

detector = htm.handsDetector()


cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    # Since there is no sense in car just standing it will either go back or move forward
    flag = detector.num_fingers(img, "r", 8)
    if flag:
        #print("Yippie ....les gooo boiiii")
        ## --> Right Index is open
        print("U")
        keyboard.press(Key.up)
        keyboard.release(Key.down)
    else:
        print("D")
        ## --> Right Index is close
        keyboard.press(Key.down)
        keyboard.release(Key.up)

    flag1 = detector.num_fingers(img, "l", 8)
    flag2 = detector.num_fingers(img, "l", 12)
    flag3 = detector.num_fingers(img, "l", 20)

    if flag1 and not flag2:
        print("R")
        ## --> Left Index is open and Left middle is closed
        keyboard.press(Key.right)
    else:
        keyboard.release(Key.right)

    if flag2:
        print("L")
        ## --> Left Middle is open
        keyboard.press(Key.left)
    else:
        keyboard.release(Key.left)

    if flag3:
        print("Space")
        ## --> Left little finger is open
        keyboard.press(Key.space)
    else:
        keyboard.release(Key.space)

    #### fps calculations (Greater the better) ####
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    img = cv2.flip(img, 1)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

#### Releasing any keyboard button pressed as the game may end abruptly by the user #####
keyboard.release(Key.down)
keyboard.release(Key.up)
keyboard.release(Key.left)
keyboard.release(Key.right)
keyboard.release(Key.space)

cap.release()
cv2.destroyAllWindows()

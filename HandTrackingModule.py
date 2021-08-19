###########################################################################
# This File is the base Hand detection module and needs to be imported in #
# all image processing py scripts and there we will create a instance of  #
# handsDetector class and use its functions                               #
###########################################################################

#### Imports ####
import cv2
import mediapipe as mp
import time

#### Main class we will use in other py files ####
class handsDetector():

    #### The innit function with standard mediapipe variables ####
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    #### Finds Hands and draws lines on them ####
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    #### Find the hand with given hand no and highlits it using blue circles ####
    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, z = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

        return lmList

    #### The function to detect the direction the hand is pointing to ####
    def direction_hand(self, img, thres, ind_1, ind_2, flag):
        img = self.findHands(img)
        lmList = self.findPosition(img)
        if len(lmList) != 0:
            x = (lmList[ind_1][1] - lmList[ind_2][1])
            y = (lmList[ind_1][2] - lmList[ind_2][2])
            # print(x, y)

            if y > thres:
                return 'd'

            elif y < -thres:
                return 'u'

            elif x > thres:
                return 'l'

            elif x < -thres:
                return 'r'

        return flag

    #### The function to detect and return the hand no for left and right hand ####
    def left_or_right(self, img):
        img = self.findHands(img, draw=False)
        lmList = self.findPosition(img, draw=False)
        if len(lmList) != 0:
            num_hands = len(self.results.multi_handedness)
            if num_hands != 2:
                # print(num_hands)
                # print("I got removed Here")
                return False, 2, 2
            for id, classification in enumerate(self.results.multi_handedness):
                # print("I got here !!!!!!!!!!")
                if classification.classification[id].label == "Left":
                    l = classification.classification[id].index
                    return True, l, 1 - l
                elif classification.classification[id].label == "Right":
                    r = classification.classification[id].index
                    return True, 1 - r, r
                else:
                    print("What the hell just happened....heh?")
                    return False, 2, 2
        return False, 2, 2
        
    #### The function to detect whether a finger is open or closed ####
    # tip_num => 8, 12, 16, 20
    def num_fingers(self, img, hand_flag, tip_num):

        flag, left, right = self.left_or_right(img)
        if flag:
            if hand_flag == "l":
                hand_index = left
            elif hand_flag == "r":
                hand_index = right
            else:
                print("Please check the hand_flag Parameter")
                return False
            lmList = self.findPosition(img, draw=False, handNo=hand_index)

            if lmList[tip_num][2] < lmList[tip_num - 2][2]:
                return True

        return False


def main():
    #### A test program can be ran in another py file with suitable imports ####
    '''
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handsDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
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
    '''


if __name__ == "__main__":
    main()

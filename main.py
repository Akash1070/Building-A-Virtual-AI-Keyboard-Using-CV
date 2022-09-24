

import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

ClickedText = ""
keyboard = Controller()
def drawALL(img,buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    return img


class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos = pos
        self.text = text
        self.size = size




# myButton = Button([100,100],'Q')
# myButton1 = Button([200,100],'W')
# myButton2 = Button([300,100],'E')
# myButton3 = Button([400,100],'R')
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img= detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    drawALL(img, buttonList)

    if lmlist:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            if x<lmlist[8][0]<x+w and y<lmlist[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                l,_,_=detector.findDistance(8,12,img)
                # print(l)
                if l < 50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                    ClickedText += button.text
                    sleep(0.2)
    cv2.rectangle(img, (55,345), (700,450), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, ClickedText, (60,425), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)







    # cv2.rectangle(img,(100,100),(200,200),(0,0,0),cv2.FILLED)
    # cv2.putText(img,'Q',(120,180),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),5)
    # myButton = Button([100,100],'Q')

    # img = myButton1.draw(img)
    # img = myButton2.draw(img)
    # img = myButton3.draw(img)
    cv2.imshow('camera',img)
    cv2.waitKey(1)





import os
import random
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)

id_list = [0, 17, 78, 292]

folder_eatable = 'Objects/eatable'
list_eatable = os.listdir(folder_eatable)
eatables = []
for obj in list_eatable:
    eatables.append(cv2.imread(f'{folder_eatable}/{obj}', cv2.IMREAD_UNCHANGED))

folder_non_eatable = 'Objects/noneatable'
list_non_eatable = os.listdir(folder_non_eatable)
non_eatables = []
for obj in list_non_eatable:
    non_eatables.append(cv2.imread(f'{folder_non_eatable}/{obj}', cv2.IMREAD_UNCHANGED))

current_object = eatables[0]

pos = [300, 0]
speed = 5
count = 0
global is_eatable
is_eatable = True
game_over = False


def reset_object():
    global is_eatable
    pos[0] = random.randint(100, 1180)
    pos[1] = 0
    rand_no = random.randint(0, 2)  # change the ratio of eatables/ non-eatables
    if rand_no == 0:
        current_object = non_eatables[random.randint(0, 3)]
        is_eatable = False
    else:
        current_object = eatables[random.randint(0, 3)]
        is_eatable = True

    return current_object


while True:
    success, img = cap.read()

    if game_over is False:
        img, faces = detector.findFaceMesh(img, draw=False)

        img = cvzone.overlayPNG(img, current_object, pos)
        pos[1] += speed

        if pos[1] > 520:
            current_object = reset_object()

        if faces:
            face = faces[0]
            # for idNo, points in enumerate(face):
            #     cv2.putText(img, str(idNo), points, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)
            up = face[id_list[0]]
            down = face[id_list[1]]

            for index in id_list:
                cv2.circle(img, face[index], 5, (255, 255, 0), 5)
            cv2.line(img, face[id_list[0]], face[id_list[1]], (0, 255, 0), 2)
            cv2.line(img, face[id_list[2]], face[id_list[3]], (0, 255, 0), 2)
            horizontal, _ = detector.findDistance(face[id_list[0]], face[id_list[1]])
            vertical, _ = detector.findDistance(face[id_list[2]], face[id_list[3]])

            cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
            cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)
            distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
            # print(distMouthObject)

            ratio = int((horizontal / vertical) * 100)
            # print(ratio)
            if ratio > 60:
                mouth = "open"
            else:
                mouth = "closed"
            cv2.putText(img, mouth, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 127, 255), 1)

            if distMouthObject < 100 and ratio > 60:
                if is_eatable:
                    currentObject = reset_object()
                    count += 1
                else:
                    game_over = True
        cv2.putText(img, str(count), (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 5)
    else:
        cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        reset_object()
        game_over = False
        count = 0
        currentObject = eatables[0]
        is_eatable = True

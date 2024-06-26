import cv2
import numpy as np
# pip install opencv-python

hsv = 0
lower_blue1 = 0
upper_blue1 = 0

lower_blue2 = 0
upper_blue2 = 0

lower_blue3 = 0
upper_blue3 = 0


def nothing(x): # 트랙바 생성시 필요함
    pass

def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold

    # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환 (x, y 값으로 저장)
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img_color[y, x])
        #print(x,y)
        color = img_color[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]
        
        threshold = cv2.getTrackbarPos('threshold', 'img_result')

        

        # HSV 색공간에서 마우스 클릭으로 얻은 픽셀값과 유사한 픽셀값의 범위를 정함
        if hsv[0] < 10:
            print("case1")
            lower_blue1 = np.array([hsv[0]-10+180, threshold, threshold]) # 색상만 조절
            upper_blue1 = np.array([180, 255, 255])

            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])

            lower_blue3 = np.array([hsv[0], threshold, threshold])
            upper_blue3 = np.array([hsv[0]+10, 255, 255])
            #     print(i-10+180, 180, 0, i)
            #     print(i, i+10)

        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])

            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0]+10-180, 255, 255])

            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, 180, 0, i+10-180)
            #     print(i-10, i)
        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([hsv[0]+10, 255, 255])

            lower_blue2 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])

            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, i+10)
            #     print(i-10, i)

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)


cv2.namedWindow('img_color')
cv2.setMouseCallback('img_color', mouse_callback)

cv2.namedWindow('img_result')
cv2.createTrackbar('threshold', 'img_result', 0, 255, nothing)
cv2.setTrackbarPos('threshold', 'img_result', 30) # 초기값 30



cap = cv2.VideoCapture(0)



while(True):
    #img_color = cv.imread('hsv.png')
    ret, img_color = cap.read()
    height, width = img_color.shape[:2]
    img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)

    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

    img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3
    
    kernel = np.ones((11,11), np.uint8) 
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel) # 점으로 보이는 노이즈를 제거
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel) # 검은 구멍 메움

    img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask)
    
    numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(img_mask)
    # 쉽게 라벨링 할 수 있음
    
    for idx, centroid in enumerate(centroids):
        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue
        
        if np.any(np.isnan(centroid)):
            continue
        
        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])
        
        if area > 50:
            cv2.circle(img_color, (centerX, centerY), 10, (0, 0, 255), 10)
            cv2.rectangle(img_color, (x, y), (x+width, y+height), (0,0,255))
    #print(numOfLabels,stats)
        

    cv2.imshow('img_color', img_color)
    cv2.imshow('img_mask', img_mask)
    cv2.imshow('img_result', img_result)


    if cv2.waitKey(1) & 0xFF == 27:
        break


cv2.destroyAllWindows()
import cv2
import numpy as np

class Line:
    def __init__(self,image,frame):
        self.hsv = image
        self.frame = frame
        self.lower_blue = np.array([39, 11, 0])
        self.upper_blue = np.array([99, 128, 255])
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        self.mask = cv2.inRange(self.hsv, self.lower_blue, self.upper_blue)
        self.kernel = np.ones((5,5),np.uint8)
        self.dilation = cv2.dilate(self.mask,self.kernel,iterations = 2)
        self.kernel = np.ones((15,15),np.uint8)
        self.opening = cv2.morphologyEx(self.dilation, cv2.MORPH_OPEN, self.kernel)
        self.mask = cv2.morphologyEx(self.opening, cv2.MORPH_CLOSE, self.kernel) 
        self.res = cv2.bitwise_and(self.frame,self.frame, mask= self.mask)
        
    def contour(self):
        self.contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(self.contours) > 0:
            cnt = max(self.contours, key = cv2.contourArea)
            try:
                M = cv2.moments(cnt) 
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                self.x,self.y,self.w,self.h = cv2.boundingRect(cnt)
                #self.frame = cv2.rectangle(self.frame,(self.x,self.y),(self.x+self.w,self.y+self.h),(0,255,0),2)
                #print("x : {0} Y : {1}".format(w,h))
            except:
                print('eror')

        cv2.circle(self.frame,(self.x+self.w/2,self.y+self.h/2), 12, (0,0,255), -1)
        
        return self.frame
    
    def CentreOfCircle(self):
        return self.x+self.w/2 ,self.y+self.h/2

cap = cv2.VideoCapture(0)
w=[0,0,0,0,0,0]
h=[0,0,0,0,0,0]
while(1):
    framel=[[],[],[]]
    hsvl=[[],[],[]]
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for i in range(0,3):
        for j in range(0,2):
            framel[i].append(frame[i*160:(i+1)*160 , j*320:(j+1)*320].copy())  
            hsvl[i].append(hsv[i*160:(i+1)*160 , j*320:(j+1)*320].copy())
    #print(len(framel),len(hsvl))

    LINE0 = Line(hsvl[0][0],framel[0][0])
    frame0= LINE0.contour()

    LINE1 = Line(hsvl[0][1],framel[0][1])
    frame1 = LINE1.contour()

    LINE2 = Line(hsvl[1][0],framel[1][0])
    frame2 = LINE2.contour()
    
    LINE3 = Line(hsvl[1][1],framel[1][1])
    frame3 = LINE3.contour()

    LINE4 = Line(hsvl[2][0],framel[2][0])
    frame4 = LINE4.contour()

    LINE5 = Line(hsvl[2][1],framel[2][1])
    frame5 = LINE5.contour()
    w[0] , h[0] = LINE0.CentreOfCircle()
    w[1] , h[1] = LINE1.CentreOfCircle()
    w[2] , h[2] = LINE2.CentreOfCircle()
    w[3] , h[3] = LINE3.CentreOfCircle()
    w[4] , h[4] = LINE4.CentreOfCircle()
    w[5] , h[5] = LINE5.CentreOfCircle()

    cv2.circle(frame,(320,80), 12, (0,0,255), -1)
    cv2.circle(frame,(320,240), 12, (0,0,255), -1)
    cv2.circle(frame,(320,400), 12, (0,0,255), -1)
    #print("Weight 0 : " ,320 - w[0])
    cv2.imshow('frame',frame)
    cnt = 0
    for i in range(0,3):
        for j in range(0,2):
            cv2.imshow('frame'+str(cnt),framel[i][j])
            cnt += 1
    
    #print("w: {0} H : {1}".format(w,h))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

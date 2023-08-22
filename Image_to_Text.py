import cv2
import pytesseract
import os

class Image_to_Text_AI:
    
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        self.mouseX = 0
        self.mouseY = 0
        self.img = None
        self.cropped_img = None
        self.num_mouse_clicks=0
        self.rectangle_start_point = 0
        self.rectangle_end_point = 0
        self.showCamera()
        self.manuallyCropImage()
        
    def showCamera(self):

        while(True):
            ret, frame = self.cam.read()
            frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            
            # 32 is spacebar
            if c == 32:
                cv2.imwrite("Homework.png", frame)
                self.img = cv2.imread('Homework.png')
                break

        self.cam.release()
        cv2.destroyWindow("Input")


    def imageToText(self):
        img = self.cropped_img
        text = pytesseract.image_to_string(img,config = '--oem 3 --psm 6')
        os.remove("Homework.png")
        return text


    def drawCircle(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.img,(x,y),3,(255,0,0),-1)

            if self.num_mouse_clicks == 0:
                self.rectangle_start_point = (x,y)
                
            elif self.num_mouse_clicks == 1:
                self.rectangle_end_point = (x,y)

            else:
                # sets img equal to clean clone to 'delete' all drawings
                self.img = cv2.imread('Homework.png')
                cv2.circle(self.img,(x,y),3,(255,0,0),-1)
                self.num_mouse_clicks = 0
                self.rectangle_start_point = (x,y)

            self.num_mouse_clicks+=1

    def manuallyCropImage(self):
        
        while(True):
    
            cv2.imshow('Click on two opposite corners surrounding text and press enter to crop', self.img)
            cv2.setMouseCallback("Click on two opposite corners surrounding text and press enter to crop",self.drawCircle)
            c =  cv2.waitKey(1)
            if self.num_mouse_clicks == 2:
                cv2.rectangle(self.img,self.rectangle_start_point,self.rectangle_end_point,(0,0,255),2)
                
                #13 is enter key
                if c == 13:
                    x1 = self.rectangle_start_point[0]
                    y1 = self.rectangle_start_point[1]
                    x2 = self.rectangle_end_point[0]
                    y2 = self.rectangle_end_point[1]
                    self.cropped_img = self.img[y1:y2, x1:x2]
                    break
            # 32 is spacebar
            if c==27:
                break
        cv2.destroyWindow('Click on two opposite corners surrounding text and press enter to crop')


if __name__ == '__main__':

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    al = Image_to_Text_AI()


    # shows waitkey keys
    """img = cv2.imread('Homework.png') # load a dummy image
    while(1):
        cv2.imshow('img',img)
        k = cv2.waitKey(0)
        if k==27:    # Esc key to stop
            break
        elif k==-1:  # normally -1 returned,so don't print it
            continue
        else:
            print(k) # else print its value"""

    


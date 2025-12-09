import cv2 as cv 
import numpy as np
import threading 
from time import sleep
from Packages.video import VideoCapture
from Packages.vision import vision 
from Packages.hsvfilter import hsvFilter
# Detection of contours over live feed of image
class Contours(vision):
    def __init__(self, capture=None, filter=None, type='BGR')
        
        #if self.filter is None:
            #self.filter = hsvFilter(155, 0, 255, 100, 255, 200)
        #else:
            #assert filter is hsvFilter, "Type error"
            #self.filter = filte    
        self.stopped = False 
        self.thread = None
        
        self.contours = None
        
    def start(self):
        if self.thread and self.thread.is_alive():
            print("Contours thread already running")
            return self
        self.stopped = False
        self.thread = threading.Thread(target=self.findContours, daemon=True)
        self.thread.start()
        print("Contours thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
            
    def is_alive(self):
        return self.thread.is_alive() if self.thread else False

    def findContours(self):
        
        while not self.stopped:
            
            # Applies HSV filter to image
            #filtered_img = self.apply_hsv_filter(filter=self.filter, image=self.capture.frame)
            # Turn into grayscale
            
            if self.type == 'BGR':
                gray = cv.cvtColor(self.capture.frame, cv.COLOR_BGR2GRAY)
            if self.type == 'LAB':
                temporary = cv.cvtColor(self.capture.frame, cv.COLOR_Lab2BGR)
                gray = cv.cvtColor(temporary, cv.COLOR_BGR2GRAY)
            # Main function
            ret, thresh = cv.threshold(gray, 65, 255, cv.THRESH_BINARY)
            if (ret):
                kernel = np.ones((7,7), np.uint8)
                thresh = cv.dilate(thresh, kernel)
                contours,_ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    print("Contours detected successfully. ")
                    self.contours = contours
                else:
                    print("Error: No contours detected")
                    return self
            else:
                print("Unable to detect contours ")
                return self
            
    def drawBound(self):
        if len(self.contours) > 0 and self.contours is not None:
            x, y, w, h = cv.boundingRect(self.contours[0])
            canvas = self.capture.frame.copy()
            cv.rectangle(canvas, (x, y), (x+w, y+h), (0, 255, 0), 3)
            print("Drawn sucessfully")
            return canvas # type = np.array (image file) 
        else:
            print("No contours drawn")
            return self.capture.frame 
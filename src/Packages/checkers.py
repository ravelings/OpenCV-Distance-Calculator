import cv2 as cv
import threading
import numpy as np
from time import sleep 

class Checkers:
    
    obj = []  
    def __init__(self, board_dimensions, new_criteria=None):
        
        self.board_dimensions = (board_dimensions[0] - 1, board_dimensions[1] - 1)
        if new_criteria is not None:
            self.criteria = new_criteria
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) 
        self.capture = None
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((self.board_dimensions[0] * self.board_dimensions[1],3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.board_dimensions[0],0:self.board_dimensions[1]].T.reshape(-1,2)
        
        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.
        # Corners
        self.corners = None
        self.ret = None
        # Threading
        self.stopped = False
        self.thread = None
        self.exchange = None
        
        pass
    
    def start(self):
        if self.thread and self.thread.is_alive():
            print("Vision thread already running")
            return self
        
        self.stopped = False
        self.thread = threading.Thread(target=self.detectCheckers, daemon=True)
        self.thread.start()
        print("Checkers thread started.")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
    
    def setCapture(self, capture):
        self.capture = capture
        
        return self
    
    def verifyCorners(self):
        if self.corners is None or self.ret is None:
            return False
        else:
            return True
    
    def detectCheckers(self):
        
        while not self.stopped:
            sleep(0.1)
            print("Detecting checkers... ")
            if self.capture is None:
                print("Capture not found.")
                continue
            
            # Convert frame to gray scale
            grayImage = cv.cvtColor(self.capture.frame, cv.COLOR_BGR2GRAY)
            
            ret, corners = cv.findChessboardCorners(grayImage, self.board_dimensions)
            if ret == True:
                # Corner refinement
                corners2 = cv.cornerSubPix(grayImage, corners, (11,11), (-1,-1), self.criteria)
                # Assign corners and ret
                self.corners = corners2 
                self.ret = ret
                print("Corner detected.")
                continue

            print("No Corners Detected.")
            continue
        
    def drawCheckers(self):
        if not self.verifyCorners():
            #print("No corners to DRAW. ")
            return  self
        
        frameCopy = self.capture.frame
        
        cv.drawChessboardCorners(frameCopy, (self.board_dimensions), self.corners, self.ret)
        print("Drawn successfully ")
        return frameCopy
        
    def appendCorners(self):
        if not self.verifyCorners():
            print("No corners to APPEND. ")
            return self

        self.objpoints.append(self.objp)
        self.imgpoints.append(self.corners)
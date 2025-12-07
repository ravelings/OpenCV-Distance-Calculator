import cv2 as cv 
import threading

class VideoCapture:
    
    camera = None
    
    def __init__(self, camera=0):
        
        self.stream = cv.VideoCapture(camera)
        # grabbed = if work
        # frame = the frame
        self.grabbed, self.frame = self.stream.read()
        
        self.stopped = False
        self.thread = None
        self.exchange = None
        
        pass
    
    def start(self):
        if self.thread and self.thread.is_alive():
            print("Vision thread already running")
            return self
        self.stopped = False
        self.thread = threading.Thread(target=self.get, daemon=True)
        self.thread.start()
        print("Vision thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
    
    def get(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()
        """ if self.grabbed:
            print("Frame grabbed")"""
import cv2 as cv
import numpy as np
import threading
from time import sleep
from Packages.hsvfilter import hsvFilter

class vision:
    filtered_needle = None
    filter = None
    # Window for Trackbar
    window = "Trackbar"
    # HSV Values
    ## Hue
    hMax = 0
    hMin = 0
    ## Saturation
    sMax = 0
    sMin = 0
    ## Value
    vMax = 0
    vMin = 0
    ## Threshold
    threshold = 0.08
    def __init__(self, needle=None, HSV_FILTER=None):
        self.filter = HSV_FILTER
        
        if needle is not None:
            self.filtered_needle = self.apply_hsv_filter(needle)
            self.resized_needle = self.filtered_needle
        
        self.stopped = False
        self.thread = None
        self.exchange = None
        pass
    
    def set_exchange(self, exchange):
        self.exchange = exchange
        print("Exchanged")
    
    def start(self):
        if self.thread and self.thread.is_alive():
            print("Vision thread already running")
            return self
        self.stopped = False
        self.thread = threading.Thread(target=self.match, daemon=True)
        self.thread.start()
        print("Vision thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
    
    def is_alive(self):
        return self.thread.is_alive() if self.thread else False
    
    def init_gui(self):
        # Create window
        cv.namedWindow(self.window)
        # Dummy function
        def nothing(position):
            pass
        # Trackbar
        ## Hue
        cv.createTrackbar('hMax', self.window, 0, 179, nothing)
        cv.createTrackbar('hMin', self.window, 0, 179, nothing)
        ## Saturation
        cv.createTrackbar('sMax', self.window, 0, 255, nothing)
        cv.createTrackbar('sMin', self.window, 0, 255, nothing)
        ## Value
        cv.createTrackbar('vMax', self.window, 0, 255, nothing)
        cv.createTrackbar('vMin', self.window, 0, 255, nothing)
        
        # Default value
        cv.setTrackbarPos('hMax', self.window, 179)
        cv.setTrackbarPos('sMax', self.window, 255)
        cv.setTrackbarPos('vMax', self.window, 255)
        
    def get_filter_from_trackbar(self) -> hsvFilter:
        
        filter = hsvFilter()
        
        ## Hue
        filter.hMax = cv.getTrackbarPos('hMax',self.window)
        filter.hMin = cv.getTrackbarPos('hMin',self.window)
        ## Saturation
        filter.sMax = cv.getTrackbarPos('sMax',self.window)
        filter.sMin = cv.getTrackbarPos('sMin',self.window)
        ## Value
        filter.vMax = cv.getTrackbarPos('sMax',self.window)
        filter.vMin = cv.getTrackbarPos('sMin',self.window)
        
        print("hsv filter hMax: ", filter.hMin)
        
        return filter

    def apply_hsv_filter(self, filter=None, image=None) -> np.array:

        if image is None:
            converted_img = cv.cvtColor(self.exchange.frame, cv.COLOR_BGR2HSV) 
        else:
            # assert image is type(np.array), "Image must be type np.array"
            converted_img = cv.cvtColor(image, cv.COLOR_BGR2HSV) 
        # creates reference
        
# This block of code is performing color filtering based on the HSV (Hue, Saturation, Value) values
# specified by the trackbars. Here's a breakdown of what each step does:
        if filter is None:
            self.filter = self.get_filter_from_trackbar()
                # Debug
                #print("vMax: ", self.filter.vMax)
                #print("vMin: ", self.filter.vMin)
            # Set minimum and maximum HSV values to display
            lower = np.array([self.filter.hMin, self.filter.sMin, self.filter.vMin])
            upper = np.array([self.filter.hMax, self.filter.sMax, self.filter.vMax])
        else:
            lower = np.array([filter.hMin, filter.sMin, filter.vMin])
            upper = np.array([filter.hMax, filter.sMax, filter.vMax])
        print("Lower: ", lower)
        print("Upper: ", upper)   
        # Apply threshold
        mask = cv.inRange(converted_img, lower, upper)
        result = cv.bitwise_and(converted_img, converted_img, mask=mask)
        
        image = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        
        return image
    
    def _needle_for_frame(self, frame_shape):
        if self.filtered_needle is None:
            return None
        
        frame_h, frame_w = frame_shape[:2]
        needle_h, needle_w = self.filtered_needle.shape[:2]
        
        if needle_h <= frame_h and needle_w <= frame_w:
            self.resized_needle = self.filtered_needle
            return self.resized_needle
        
        scale = min(frame_h / needle_h, frame_w / needle_w)
        new_w = max(1, int(needle_w * scale))
        new_h = max(1, int(needle_h * scale))
        
        if (self.resized_needle is not None and
            self.resized_needle.shape[0] == new_h and
            self.resized_needle.shape[1] == new_w):
            return self.resized_needle
        
        self.resized_needle = cv.resize(self.filtered_needle, (new_w, new_h), interpolation=cv.INTER_AREA)
        print(f"Needle resized to {new_w}x{new_h} to fit frame")
        return self.resized_needle
    
    def match(self):
        
        print("Match called")
        
        while not self.stopped:
            if self.exchange is None or self.exchange.frame is None:
                sleep(0.01)
                continue
            
            ## Filter images
            filtered_haystack = self.apply_hsv_filter(self.exchange.frame)
            template = self._needle_for_frame(filtered_haystack.shape)
            if template is None:
                print("No template available")
                sleep(0.1)
                continue
            
            ## Apply match template
            result = cv.matchTemplate(filtered_haystack, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
            print("Max Value: ", max_val)
            
            if max_val <= self.threshold:
                sleep(0.01)
                continue
            else:
                top_left = max_loc
                bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
                
                cv.rectangle(self.exchange.frame, top_left, bottom_right, 255, 5)
                
                print("Rectangle drawn at: (", top_left[0], " ", top_left[1], ")")
                sleep(0.01)

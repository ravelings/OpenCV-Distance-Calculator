import cv2 as cv 

# Internal Packages
from Packages.video import VideoCapture
from Packages.vision import vision

capture = VideoCapture(0).start() # start video capture 
visual = vision().start() # start vision object
visual.set_exchange(capture) # capture starts exchanging frames

visual.init_gui() # initialize trackbars

def main() -> None:
    while (True):
        image = visual.apply_hsv_filter_trackbar()
        
        cv.imshow('window', image)
        
        key = cv.waitKey(1)
        if key == ord('q'):
            visual.stop()
            capture.stop()
            cv.destroyAllWindows()
            break
    print("Main processed terminated.")
    
main()

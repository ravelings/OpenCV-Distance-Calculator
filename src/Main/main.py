import cv2 as cv 
import threading
from vision import vision
from hsvfilter import hsvFilter
from video import VideoCapture

needle = cv.imread('/Users/emmelinechow/Documents/Coding/Python/4. OpenCV Object Recognition/purple_cloth2.jpeg', cv.IMREAD_UNCHANGED)

# Set filter to show only purple (hopefully)
filter = hsvFilter(179, 70, 255, 110, 255, 0)
# Initialize trackbar
# vision_cloth.init_gui()
matchCloth = vision(needle, filter)

exchange = VideoCapture(0).start()
matchCloth.set_exchange(exchange)
matchCloth.start()


while (True):
    
    # Apply filter to image
    # output = vision_cloth.apply_hsv_filter(purple_cloth)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exchange.stop()
        matchCloth.stop()
        break
    
    frame = matchCloth.exchange.frame
    
    cv.imshow('window', frame)
    

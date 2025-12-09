import cv2 as cv 
import os
from Packages.video import VideoCapture
from Packages.checkers import Checkers
Chess_Board_Dimensions = (8, 8)

n = 0  # image counter

# checks images dir is exist or not
image_path = "/Users/emmelinechow/Documents/Coding/Python/4. OpenCV Object Recognition/images"

Dir_Check = os.path.isdir(image_path)

if not Dir_Check:  # if directory does not exist, a new one is created
    os.makedirs(image_path)
    print(f'"{image_path}" Directory is created')
else:
    print(f'"{image_path}" Directory already exists.')

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

capture =  VideoCapture(0).start() # Begins capturing
board = Checkers(Chess_Board_Dimensions, criteria).setCapture(capture)
board.start() # Begins detecting checkers from capture
while (True):
    
    drawn = board.drawCheckers()
    
    cv.imshow('window', board.capture.frame)
    
    if cv.waitKey(1) == ord('q'):
        board.stop()
        capture.stop()
        cv.destroyAllWindows()
        break
    
print("Program ended")
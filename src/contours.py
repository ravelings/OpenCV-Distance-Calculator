import cv2 as cv 
import numpy as np 

from Packages.vision import vision
from Packages.hsvfilter import hsvFilter

def findContours(img):
    ret, thresh = cv.threshold(img, 65, 255, cv.THRESH_BINARY)
    if (ret):
        kernel = np.ones((7,7), np.uint8)
        thresh = cv.dilate(thresh, kernel)
        contours,_ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            print("Contours detected successfully. ")
            return contours
        else:
            print("Error: No contours detected")
            return None
    else:
        print("Unable to detect contours ")
        return None
    
def drawBound(image, contours):
    assert len(contours) > 0 , "Contours empty"
    x, y, w, h = cv.boundingRect(contours[0])
    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
def main() -> None:
    filter = hsvFilter(155, 10, 255, 100, 255, 180)

    image = cv.imread("orange_box.jpeg", cv.IMREAD_UNCHANGED)
    visual = vision()
    #visual.init_gui()
    #filtered_img = visual.apply_hsv_filter_trackbar(filter= filter, image= image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    contours = findContours(gray)
    
    drawBound(image, contours)
    
    while (True):
        # filtered_img = visual.apply_hsv_filter_trackbar(image=image)
        cv.imshow('window', image)
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        
    print("Program ended. ")


main()
    



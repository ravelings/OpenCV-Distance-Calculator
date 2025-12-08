import cv2 as cv 
import numpy as np
from Packages.labfilter import LabFilter

class LabImage:
    def __init__(self, image):

        self.window = 'trackbar' 

        self.image = cv.cvtColor(image, cv.COLOR_BGR2LAB)
        self.imageFiltered = self.image.copy()

    def init_gui(self):
        cv.namedWindow(self.window, cv.WINDOW_NORMAL)

        # Dummy function
        def nothing(position):
            pass
        # Trackbar (Scaled)
        ## L [0, 100]
        cv.createTrackbar('L Max', self.window, 0, 255, nothing)
        cv.createTrackbar('L Min', self.window, 0, 255, nothing)
        ## a* [-127, 127]
        cv.createTrackbar('a* Max', self.window, 0, 128, nothing)
        cv.createTrackbar('a* Min', self.window, 0, 128, nothing)
        ## b* [-127, 127]
        cv.createTrackbar('b* Max', self.window, 0, 128, nothing)
        cv.createTrackbar('b* Min', self.window, 0, 128, nothing)
        
        # Default value
        cv.setTrackbarPos('L Max', self.window, 255)
        cv.setTrackbarPos('a* Max', self.window, 0)
        cv.setTrackbarPos('b* Max', self.window, 0)

        return self 
    
    def get_trackbar_pos(self):

        labFilter = LabFilter()
        # L
        labFilter.LMax = cv.getTrackbarPos('L Max', self.window)
        labFilter.LMin = cv.getTrackbarPos('L Min', self.window)
        # a*
        labFilter.aMax = cv.getTrackbarPos('a* Max', self.window)
        labFilter.aMin = cv.getTrackbarPos('a* Min', self.window)
        # b*
        labFilter.bMax = cv.getTrackbarPos('b* Max', self.window)
        labFilter.bMin = cv.getTrackbarPos('b* Min', self.window)

        return labFilter 
    
    def applyFiltered(self):
        
        filter = self.get_trackbar_pos()

        lower = np.array([self.filter.LMin, self.filter.aMin, self.filter.bMin])
        upper = np.array([self.filter.LMax, self.filter.aMax, self.filter.bMax])

        mask = cv.inRange(self.imageFiltered, lower, upper)
        result = cv.bitwise_and(self.imageFiltered, self.imageFiltered, mask=mask)

    def getImage(self):
        return cv.cvtColor(self.filteredImage, cv.COLOR_Lab2BGR)
        

class hsvFilter:
    
    def __init__(self, hMax=None, hMin=None, sMax=None, sMin=None, vMax=None, vMin=None):
        ## Hue
        self.hMax = hMax
        self.hMin = hMin
        ## Saturation
        self.sMax = sMax
        self.sMin = sMin
        ## Value
        self.vMax = vMax
        self.vMin = vMin
    
    
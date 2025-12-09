
# Contains constantly updated image file (frame)
class ImageCapture:
    def __init__(self, image):
        self.frame = image
        self.orig_frame = image.copy()
        self.ret = True # image is true
        
        
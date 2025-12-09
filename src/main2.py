import cv2 as cv 
from Packages.LABtest import LabImage
from Packages.contours import Contours
from Packages.imagecapture import ImageCapture

def main() -> None:
    image = cv.imread('orange_box.jpeg', cv.IMREAD_UNCHANGED)

    lab = LabImage(image=image)
    lab.init_gui()
    image = ImageCapture(lab.imageFiltered)
    contours = Contours(image, type='LAB')
    contours.start()  

    cv.namedWindow('contours', cv.WINDOW_NORMAL)
    cv.namedWindow('Filtered Image', cv.WINDOW_NORMAL)
    while (True):
        lab.applyFiltered()
        display = contours.drawBound()
        cv.imshow('contours', display)
        cv.imshow('Filtered Image', cv.cvtColor(image.frame, cv.COLOR_Lab2BGR))
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break

    print("Program ended.")

main()

print("BOop")
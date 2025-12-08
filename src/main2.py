import cv2 as cv 
from Packages.LABtest import LabImage



def main() -> None:
    image = cv.imread('orange_box.jpeg', cv.IMREAD_UNCHANGED)

    lab = LabImage(image=image)
    lab.init_gui()

    while (True):
        lab.applyFiltered()
        display = lab.getImage()
        
        cv.imshow('Image', display)
        key = cv.waitKey(1)

        if key == ord('q'):
            cv.destroyAllWindows()

    print("Program ended.")

main()
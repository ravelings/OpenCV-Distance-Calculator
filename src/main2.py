import cv2 as cv 
from Packages.LABtest import LabImage



def main() -> None:
    image = cv.imread('orange_box.jpeg', cv.IMREAD_UNCHANGED)

    lab = LabImage(image=image)
    lab.init_gui()

    cv.namedWindow('image', cv.WINDOW_NORMAL)

    while (True):
        lab.applyFiltered()
        display = lab.getImage()
        cv.imshow('image', display)
        key = cv.waitKey(1)

        if key == ord('q'):
            cv.destroyAllWindows()

    print("Program ended.")

main()

print("BOop")
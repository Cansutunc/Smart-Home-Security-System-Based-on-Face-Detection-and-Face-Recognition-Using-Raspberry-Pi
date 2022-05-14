import cv2
import os 

name = 'person1' #face name
os.system(f"mkdir my_dataset/{name}")
cam = cv2.VideoCapture(0)

cv2.namedWindow("Space=take photo , ESC=quit", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Space=take photo , ESC=quit", 640, 480)

img_counter = 0

while True:
    ret, frame = cam.read()

    if not ret:
        print("Check your webcam connection")
        break

    cv2.imshow("Space=take photo , ESC=quit", frame)

    k = cv2.waitKey(1)

    if k%256 == 27: #ESC

        print("Closing..")
        break

    elif k%256 == 32: #Space 
        img_name = "my_dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
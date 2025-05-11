import cv2

load_img = cv2.imread("C:/Users/Quang5014/Downloads/z6584336532993_26726bc667b24fa19abb39cb97a03635.jpg")

img = cv2.resize(load_img, (640, 480))
cv2.imwrite("resized_image.jpg", img)

#tuner for our ball finding algorithm

import cv2
import numpy as np
from skimage.morphology import dilation

# Set up capture device
cap = cv2.VideoCapture(0)

# Set up windows with sliders
cv2.namedWindow('image')
cv2.namedWindow('mask')
def dummyCallback():
    pass
cv2.createTrackbar('minHue', 'mask', 0, 255, dummyCallback)
cv2.createTrackbar('maxHue', 'mask', 255, 255, dummyCallback)
cv2.createTrackbar('minSaturation', 'mask', 0, 255, dummyCallback)
cv2.createTrackbar('maxSaturation', 'mask', 255, 255, dummyCallback)
cv2.createTrackbar('minValue', 'mask', 0, 255, dummyCallback)
cv2.createTrackbar('maxValue', 'mask', 255, 255, dummyCallback)

while True:

    # Image
    re, img = cap.read()

    # Convert image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold hsv image within hue range
    minHue = cv2.getTrackbarPos('minHue', 'mask')
    maxHue = cv2.getTrackbarPos('maxHue', 'mask')
    minSaturation = cv2.getTrackbarPos('minSaturation', 'mask')
    maxSaturation = cv2.getTrackbarPos('maxSaturation', 'mask')
    minValue = cv2.getTrackbarPos('minValue', 'mask')
    maxValue = cv2.getTrackbarPos('maxValue', 'mask')

    mask = cv2.GaussianBlur(hsv,(5,5),0)
    
    mask = 255 * (
                    (hsv[:,:,0] > minHue) & (hsv[:,:,0] < maxHue) \
                  & (hsv[:,:,1] > minSaturation) & (hsv[:,:,1] < maxSaturation) \
                  & (hsv[:,:,2] > minValue) & (hsv[:,:,2] < maxValue) \
                 ).astype(np.uint8)

    # Dilate mask to remove holes from noise
   
    mask = dilation(mask, np.ones((3, 3)))
    cv2.imshow('mask', mask) # display mask here because findContours modifies it

    # Find contours in image
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largestContourIdx = np.argmax([len(c) for c in contours])
    cv2.drawContours(img, contours, largestContourIdx, (0,255,0), 3)

    # Display images
    cv2.imshow('image', img)

    # Exit if q is pressed
    if cv2.waitKey(1) == ord('q'):
        break


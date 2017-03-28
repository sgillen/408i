import cv2
import numpy as np
from skimage.morphology import dilation

# Set up capture device
cap = cv2.VideoCapture(0)
# Set up windows with sliders
cv2.namedWindow('image')
cv2.namedWindow('mask')

while True:
    # Image
    re, img = cap.read()
    # Convert image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Threshold hsv image within hue range
    # minHue = cv2.getTrackbarPos('minHue', 'mask')
    # maxHue = cv2.getTrackbarPos('maxHue', 'mask')
    # minSaturation = cv2.getTrackbarPos('minSaturation', 'mask')
    # maxSaturation = cv2.getTrackbarPos('maxSaturation', 'mask')
    # minValue = cv2.getTrackbarPos('minValue', 'mask')
    # maxValue = cv2.getTrackbarPos('maxValue', 'mask')


    # Threshold hsv image within hue range
    minHue = 27
    maxHue = 55
    minSaturation = 163
    maxSaturation = 225
    minValue = 62
    maxValue = 190

    mask = 255 * (
        (hsv[:,:,0] > minHue) & (hsv[:,:,0] < maxHue) \
        & (hsv[:,:,1] > minSaturation) & (hsv[:,:,1] < maxSaturation) \
        & (hsv[:,:,2] > minValue) & (hsv[:,:,2] < maxValue) \
    ).astype(np.uint8)
    # Dilate mask to remove holes from noise
    mask = dilation(mask, np.ones((10, 10)))
    cv2.imshow('mask', mask)
    # display mask here because findContours modifies it
    # Find contours in image
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours):
        largestContourIdx = np.argmax([len(c) for c in contours])
        
        cv2.drawContours(img, contours, largestContourIdx, (0,255,0), 3)
        # Display images
    

        M = cv2.moments(contours[largestContourIdx])
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
        print center
        
    cv2.imshow('image', img)
    
    # Exit if q is pressed
    if cv2.waitKey(1) == ord('q'):
        break
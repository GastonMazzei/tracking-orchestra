import numpy as np
import cv2

cap = cv2.VideoCapture('videos/ants.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    contrast = 1.6
    brightness = 60
    frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

import sys
sys.exit(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

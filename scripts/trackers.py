import numpy as np
import imutils
import cv2
from random import randint
import sys

trackerName = ['csrt','kcf','boosting','mil','tld','medianflow','mosse'][1]
try:
  videoPath = 'videos/'+sys.argv[1]
except:
  videoPath = "videos/newresult.mp4"

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()
cap = cv2.VideoCapture(videoPath)
tracks_positions = []
counter = 0
KONTRASTER = [True,False][1]
ctr, br = 1.7, 1.5
while cap.isOpened():

    ret, frame = cap.read()
    if frame is None:
        break
    if KONTRASTER:
        contrast = ctr
        brightness = br 
        frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

    try:
      tracks_positions.append(boxes)
    except: pass
    # WHY DO WE RESIZZE? CHECK PLZZ

    (success, boxes) = trackers.update(frame)

    # loop over the bounding boxes and draw them on the frame
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(f'tracked_frames/{counter:03}.png',frame, )
    counter+=1

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if counter==12:
    #if True:
        colors = []
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        frame = imutils.resize(frame,)
        box = cv2.selectROIs("Frame", frame, fromCenter=False,
                             showCrosshair=True)
        box = tuple(map(tuple, box)) 
        for bb in box:
            tracker = OPENCV_OBJECT_TRACKERS[trackerName]()
            trackers.add(tracker, frame, bb)
     
        with open('data/number_of_boxes.txt','w') as f:
            f.write(f'{len(box)}\n{frame.shape[1]}\n{frame.shape[0]}')
    elif key == ord("q"):
        break
np.save('data/tracks_positions_multiple.npy',np.asarray(tracks_positions))
cap.release()
cv2.destroyAllWindows()

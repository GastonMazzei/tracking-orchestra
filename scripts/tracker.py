import cv2
import sys
import numpy as np

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use

    index = 1 #original:2
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[index]
    # https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/#opencv-tracking-api explanation!
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture("videos/newresult.mp4")

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    
    # Define an initial bounding box
    #bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box

    print('RECIEVED AN ANSWER!')
    #cv2.waitKey(5)
    #cv2.destroyAllWindows()
    # Initialize tracker with first frame and bounding box
    KONTRASTER = [True,False][1]
    ctr, br = 1.3, 0.7
    if KONTRASTER:
      contrast = ctr
      brightness = br
      frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
      frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

    bbox = cv2.selectROI(frame, True)
    ok = tracker.init(frame, bbox)
    print('advancing!')
    tracks_positions = []
    counter = 0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()

        if KONTRASTER:
            contrast = ctr
            brightness = br
            frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

        # Update tracker
        tracks_positions.append(bbox)
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # SAVE
        cv2.imwrite(f'tracked_frames/{counter:03}.png',frame, )
        counter+=1

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 30 : break
                #27
    np.save('data/tracks_positions.npy',np.asarray(tracks_positions))
   



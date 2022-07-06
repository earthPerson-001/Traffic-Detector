import string
import cv2 as cv
import sys

import os


'''
The video path must be provided separately through different program.
The use of file selector like GUI is prefererable.
'''


#the threshold area of contour to be detected
THRESHOLD_AREA = 1000


def traffic_detector(video_capture_location: string) -> any:

    if(video_capture_location == "NOT_SET" or not os.path.exists(video_capture_location)):

        video_capture_location = input("Enter the video path: \n")

        if(video_capture_location == "NOT_SET" or not os.path.exists(video_capture_location)):
            sys.exit("Video path is not valid")

    
    # loading the video
    video_capture = cv.VideoCapture(video_capture_location)
    
    # background subtractor to separate the foreground from background
    foreground_detector = cv.createBackgroundSubtractorMOG2(history=1000, detectShadows=False, varThreshold=50)

    if(not video_capture.isOpened()):
        sys.exit("Couldn't open video.")

    while(video_capture.isOpened()):
        return_value, frame = video_capture.read()
        frame = cv.resize(frame, (1000, 800)) #resising the image

        if return_value:
    
            # cropped image
            '''cropped_frame = frame[245:frame.shape[0], 0:290]
            print("Cropped_frame -> shape: ") 
            print(cropped_frame.shape)
            cv.imshow("Cropped video", cropped_frame)'''

            # masked original video
            original_masked_image = foreground_detector.apply(frame)

            # separating out the continuous white points
            frame_ret, frame_thresh = cv.threshold(original_masked_image, 254, 255, cv.THRESH_BINARY)
            frame_contours, frame_hierarchy = cv.findContours(frame_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # only considring those contours having area greater than the threshold area
            for frame_contour in frame_contours:
                if cv.contourArea(frame_contour) > THRESHOLD_AREA:
                    # Highlight the detected contours
                    '''cv.drawContours(frame, [frame_contour], -1, (0,255,0), 3)'''

                    # drawing bounding reactangle
                    x,y,w,h = cv.boundingRect(frame_contour)
                    cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            
            # original video
            cv.imshow("Original video, fast traffic", frame)
            cv.imshow("Original Masked Video, fast traffic", original_masked_image)

            # for pausing
            if cv.waitKey(25) & 0xFF == ord('p'):
                print("\nPaused\n")
                cv.waitKey(0)

            # Press q on keyboard to  exit
            if cv.waitKey(25) & 0xFF == ord('q'):
                sys.exit("\nExited as per user's request\n")

        else:
            break
         
    cv.destroyAllWindows()
    video_capture.release()
 
if __name__ == "__main__":

    video_capture_location = "NOT_SET"

    traffic_detector(video_capture_location)
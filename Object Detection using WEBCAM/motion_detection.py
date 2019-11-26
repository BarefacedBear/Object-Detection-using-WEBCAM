# Program to capture video from webcam
import cv2, time, pandas, glob # OpenCV library for image & video processing, time is used to provide time to process any operation
from datetime import datetime
from matplotlib import pyplot as py

alpha_frame = None
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=["Start","End"])
video = cv2.VideoCapture(0) # Function for video frame capture n '0' for webcam
c = 1
while True:
	status = 0
	check, frame = video.read()
	frame = cv2.flip(frame,1,frame)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(21,21),0) # To blur the gray image

	if alpha_frame is None:
		alpha_frame = gray
		continue

	beta_frame = cv2.absdiff(alpha_frame,gray)
	delta_frame = cv2.threshold(beta_frame,30,255,cv2.THRESH_BINARY)[1]
	delta_frame = cv2.dilate(delta_frame, None, iterations=2) # For making smooth threshold, > iterations = smooth
	(cnts,_) = cv2.findContours(delta_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # For identifying the object
	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue # Skip pixel with size <10000
		status = 1
		(x, y, w, h) = cv2.boundingRect(contour) # Bounding the object with a rectangle
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2) # Drawing the rectangle
		print('Object Detected')
		c += 1

	status_list.append(status)
	if status_list[-1] == 1 and status_list[-2] == 0:
		times.append(datetime.now())
	if status_list[-1] == 0 and status_list[-2] == 1:
		times.append(datetime.now())
	
	# cv2.imshow("Alpha Frame",gray) # Gray Frame
	# cv2.imshow("Beta Frame",beta_frame) # Mixed Frame
	cv2.imshow("Delta Frame",delta_frame) # Threshold Frame
	cv2.imshow("Main Frame", frame) # Colored Frame
	
	x = cv2.waitKey(1)
	if x == ord('l'):
		if status == 1:
			times.append(datetime.now())
		break

for i in range(0,len(times),2):
	df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)
df.to_csv("Times.csv")
video.release() # To release the camera
cv2.destroyAllWindows()

from datetime import datetime
import cv2
import time
import pandas
from bokeh.plotting import figure, output_file, show

# Accessing the webcam
video = cv2.VideoCapture(0)

# Storing the first frame of the video
first_frame = None

# Storing the status and time related data
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

# Infinite loop to continuously capture frames
while True:

    # Checking if the video capture is successful
    check, frame = video.read()

    # Initializing status as 0
    status = 0

    # Converting the frame to grayscale and applying Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Storing the first frame for future reference
    if first_frame is None:
        first_frame = gray
        continue

    # Finding the difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray)

    # Creating a threshold for the delta frame
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=2)

    # Finding contours in the threshold delta
    (cnts, _) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyzing each contour
    for countour in cnts:
        # Filtering out small contours
        if cv2.contourArea(countour) < 10000:
            continue
        # If a significant contour is found, update status and draw rectangle around it
        status = 1
        (x, y, w, h) = cv2.boundingRect(countour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Appending the status to the status list
    status_list.append(status)

    # Keeping only the last two statuses for comparison
    status_list = status_list[-2:]

    # Tracking the time when motion is detected or ends
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    # Displaying different frames
    cv2.imshow("gray frame", gray)
    cv2.imshow("Capturing", delta_frame)
    cv2.imshow("Threshold frame", thresh_delta)
    cv2.imshow("Color frame", frame)

    # Allowing the user to quit by pressing 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

# Printing times and status list
print(times)
print(status_list)

# Appending time data to a DataFrame and saving it as a CSV file
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)
df.to_csv("Times.csv")

# Releasing the video and closing all OpenCV windows
video.release()
cv2.destroyAllWindows()

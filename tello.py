from djitellopy import Tello
import cv2
import time
import numpy as np
import argparse
import imutils
import time
import cv2
import os
#import keras

######################################################################
width = 320  # WIDTH OF THE IMAGE
height = 240  # HEIGHT OF THE IMAGE
startCounter =1  #  0 FOR FIGHT 1 FOR TESTING
######################################################################


# CONNECT TO TELLO
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

ctr=0

me.streamoff()
me.streamon()

labelsPath = "yolo-coco/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

weightsPath = "yolo-coco/yolov3.weights"
configPath = "yolo-coco/yolov3.cfg"

print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


writer = None
(W, H) = (None, None)


sus = {'knife', 'scissors', 'cell phone'}

while True:

    # GET THE IMGAE FROM TELLO
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    frame = img

    if W is None or H is None:
		(H, W) = frame.shape[:2]

    # TO GO UP IN THE BEGINNING
    if startCounter == 0:
        me.takeoff()
        time.sleep(8)
        me.rotate_clockwise(90)
        time.sleep(3)
        me.move_left(35)
        time.sleep(3)
        me.land()
        startCounter = 1

	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	boxes = []
	confidences = []
	classIDs = []

	#print(len(layerOutputs), layerOutputs[0].shape)

	for output in layerOutputs:
		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if confidence > args["confidence"]:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")


				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))


				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)


	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])

	if len(idxs) > 0:
		for i in idxs.flatten():
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

			label = LABELS[classIDs[i]]
			if label.lower() in sus:
				coords = g.latlng
				coords = str(coords[0])+' ' +str(coords[1])

				if not coords in added:

					db.reference("coordinates").child('coord' + str(ctr) ).set(coords)
					print("illegal")

					ctr+=1

					added.add(coords)

			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)





    # # SEND VELOCITY VALUES TO TELLO
    # if me.send_rc_control:
    #     me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)

    # DISPLAY IMAGE
    cv2.imshow("MyResult", img)

    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break


print("[INFO] cleaning up...")
cv2.destroyAllWindows()

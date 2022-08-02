import numpy as np
import cv2

# Yolo v3 files(yolo.names, yolov3.cfg, yolov3.weights) download link: https://pjreddie.com/darknet/yolo/

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return


def onCook(scriptOp):
	img = op('null6').numpyArray(delayed=True)
	
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	gray = np.float32(gray)

	# 1회 호출 코드
	# classes = []
	# YOLO_net = cv2.dnn.readNet("yolov2.weights","yolov2.cfg")
	# with open("yolo.names", "r") as f:
    # 	classes = [line.strip() for line in f.readlines()]
	# layer_names = YOLO_net.getLayerNames()
	# output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

	# 반복 호출 필요 코드
	# while True:
	# 	# 웹캠 프레임
	# 	ret, frame = VideoSignal.read()
	# 	h, w, c = frame.shape

	# 	# YOLO 입력
	# 	print(type(ret)) # → bool
	# 	print(type(frame)) # → numpy.ndarray
	# 	print((frame.shape)) # → (480, 640, 3)

	# 	blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
	# 	YOLO_net.setInput(blob)
	# 	outs = YOLO_net.forward(output_layers)

	# 	class_ids = []
	# 	confidences = []
	# 	boxes = []

	# 	for out in outs:

	# 		for detection in out:

	# 			scores = detection[5:]
	# 			class_id = np.argmax(scores)
	# 			confidence = scores[class_id]

	# 			if confidence > 0.5:
	# 				# Object detected
	# 				center_x = int(detection[0] * w)
	# 				center_y = int(detection[1] * h)
	# 				dw = int(detection[2] * w)
	# 				dh = int(detection[3] * h)
	# 				# Rectangle coordinate
	# 				x = int(center_x - dw / 2)
	# 				y = int(center_y - dh / 2)
	# 				boxes.append([x, y, dw, dh])
	# 				confidences.append(float(confidence))
	# 				class_ids.append(class_id)

	# 	indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


	# 	for i in range(len(boxes)):
	# 		if i in indexes:
	# 			x, y, w, h = boxes[i]
	# 			label = str(classes[class_ids[i]])
	# 			score = confidences[i]

	# 			# 경계상자와 클래스 정보 이미지에 입력
	# 			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
	# 			cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, 
	# 			(255, 255, 255), 1)

	# 	cv2.imshow("YOLOv3", frame)

	# 	if cv2.waitKey(100) > 0:
	# 		break

	dst = cv2.cornerHarris(gray, 2, 3, 0.04)
	dst = cv2.dilate(dst, None)

	img[dst > 0.01*dst.max()] = [0, 0, 255, 255]

	scriptOp.copyNumpyArray(img)

	page = scriptOp.appendCustomPage('Custom1')
	page.appendFloat('X1')

	return

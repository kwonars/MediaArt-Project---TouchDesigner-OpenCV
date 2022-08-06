import cv2
import numpy as np
import socket
from _thread import *

HOST = '127.0.0.1'
PORT = 7000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        data = client_socket.recv(1024)

        print("recive : ",repr(data.decode()))
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(1)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("/Users/sinpl/Desktop/TEsting/yolov3.weights","/Users/sinpl/Desktop/TEsting/yolov3.cfg")
#YOLO_net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")

# YOLO NETWORK 재구성
classes = []
with open("/Users/sinpl/Desktop/TEsting/yolo.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
#print((YOLO_net.getUnconnectedOutLayers()[0]))
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    # YOLO 입력
    # print(type(ret))
    # print(type(frame))
    # print((frame.shape))
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for idx, detection in enumerate(out):

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected

                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                # print(str(idx) + str(" ") + str(center_x))

                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

    personNum = 0
    coordinates = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, dw, dh = boxes[i]
            label = str(classes[class_ids[i]])

            # score = confidences[i]
            if label == "person":
                personNum += 1
                coordinates.append([round(((2*x+dw)/2)*4/w-2,2), round(((2*y+dh)/2)*(-2/h)+1,2)])

                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + dw, y + dh), (0, 0, 255), 5)
                # cv2.rectangle(frame, (0, 0), (dw, dh), (255, 0, 0), 5)
                # cv2.rectangle(frame, (0, 0), (w, h), (0, 255, 0), 5)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5,
                (255, 255, 255), 1)

    # coordinates.sort() # 동작 확인 필요

    if personNum == 0:
    	CoordsOut = [0,0,0,0,0]
    elif personNum == 1:
        CoordsOut = [coordinates[0][0], coordinates[0][1], 0, 0, 1]
    else:
        CoordsOut = [coordinates[0][0], coordinates[0][1], coordinates[-1][0], coordinates[-1][1], 2]

    datFormat = ''
    for idx, coord in enumerate(CoordsOut):
        datFormat = datFormat + str(coord) + "/"

    client_socket.send(datFormat.encode())
    # print(CoordsOut)

    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(100) > 0:
        break
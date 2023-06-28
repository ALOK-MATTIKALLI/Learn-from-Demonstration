# color detector with HSV values 
# but values are not saved 

#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import numpy as np

def empty(a):
    pass
 
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

# Connect to device and start pipeline
with dai.Device() as device:
    # Create pipeline
    pipeline = dai.Pipeline()
    cams = device.getConnectedCameraFeatures()
    streams = []
    for cam in cams:
        print("type")
        print(type(cam))
        print(str(cam), str(cam.socket), cam.socket)
        c = pipeline.create(dai.node.Camera)
        x = pipeline.create(dai.node.XLinkOut)
        c.isp.link(x.input)
        c.setBoardSocket(cam.socket)
        c.setPreviewSize(500, 500)
        stream = str(cam.socket)
        if cam.name:
            stream = f'{cam.name} ({stream})'
        x.setStreamName(stream)
        streams.append(stream)

    # Start pipeline
    device.startPipeline(pipeline)
    fpsCounter = {}
    lastFpsCount = {}
    tfps = time.time()
    while not device.isClosed():
        queueNames = device.getQueueEvents(streams)
        for stream in queueNames:
            if stream == 'color (CameraBoardSocket.RGB)':
                messages = device.getOutputQueue(stream).tryGetAll()
                fpsCounter[stream] = fpsCounter.get(stream, 0.0) + len(messages)
                for message in messages:
                    # Display arrived frames
                    if type(message) == dai.ImgFrame:
                        # render fps
                        fps = lastFpsCount.get(stream, 0)
                        frame = message.getCvFrame()
                        wth = frame.shape[1]
                        hgt = frame.shape[0]
                        w = int(wth * 0.6)
                        h = int(hgt * 0.6)
                        
                        frame = cv2.resize(frame,(w,h))
                        crop = frame[1:650, 260:900]

                        cropHsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
 
                        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
                        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
                        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
                        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
                        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
                        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
                    
                        lower = np.array([h_min, s_min, v_min])
                        upper = np.array([h_max, s_max, v_max])
                        mask = cv2.inRange(cropHsv, lower, upper)
                        result = cv2.bitwise_and(crop, crop, mask=mask)
                    
                        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                        hStack = np.hstack([crop, mask, result])
                        cv2.imshow('Horizontal Stacking', hStack)

        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows
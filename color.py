# this code will detect the block according to the input lower and upper Value
# change the values in lower and upper to get different colors 

#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import numpy as np
cx = 0
cy = 0
lower = (0,140,70)
upper = (255,255,255)

# Connect to device and start pipeline
with dai.Device() as device:
    # Create pipeline
    pipeline = dai.Pipeline()
    cams = device.getConnectedCameraFeatures()
    streams = []
    for cam in cams:
        # print("type")
        # print(type(cam))
        # print(str(cam), str(cam.socket), cam.socket)
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
                        W = int(wth * 0.6)
                        H = int(hgt * 0.6)
                        
                        frame = cv2.resize(frame,(W,H))
                        crop = frame[1:625, 280:880]
                        cropHsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
                        mask = cv2.inRange(cropHsv, lower, upper)
                        contours, hierarcy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        
                        ######################
                        if len(contours) != 0:
                            for contour in contours:
                                if cv2.contourArea(contour)>1000:
                                    x,y,w,h = cv2.boundingRect(contour)
                                    cv2.rectangle(crop, (x,y), (x+w, y+h), (0,0,255),2)
                                    cv2.circle(crop, (int(x+(w/2)), int(y+(h/2))), 5, (0,255,255), -1)
                        
                        ######################
                        # blank = np.zeros_like(crop)
                        # # blank = cv2.cvtColor(blank, cv2.COLOR_GRAY2BGR)
                        # for i in contours:
                        #     M = cv2.moments(i)
                        #     if M['m00'] != 0:
                        #         cx = int(M['m10']/M['m00'])
                        #         cy = int(M['m01']/M['m00'])
                        #         cv2.drawContours(blank, [i], -1, (0, 255, 0), 2)
                        #         cv2.circle(blank, (cx, cy), 7, (0, 0, 255), -1)
                        #         cv2.putText(blank, "center", (cx - 20, cy - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        #     print(f"x: {cx} y: {cy}")
                        # combine = cv2.addWeighted(crop, 0.9, blank, 1, 0)
                        # cv2.imshow('combine', combine)
                        #################

                        # cv2.imshow(stream, frame)
                        cv2.imshow('roi', crop)
                        cv2.imshow('mask', mask)

        if cv2.waitKey(1) == ord('q'):
            break
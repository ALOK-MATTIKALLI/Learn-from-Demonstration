#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import numpy as np

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
                        crop = frame[1:625, 280:880]

                        cv2.imshow(stream, frame)
                        cv2.imshow('roi', crop)

        if cv2.waitKey(1) == ord('q'):
            break
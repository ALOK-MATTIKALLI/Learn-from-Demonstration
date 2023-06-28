# this prigram will create file b1, b2, b3 for block 1,2, and 3
# the file has min and max HSV values
##################

#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import numpy as np

camRes = dai.ColorCameraProperties.SensorResolution.THE_1080_P
camSocket = dai.CameraBoardSocket.RGB
ispScale = (1,2)

def getMesh(calibData, ispSize):
    M1 = np.array(calibData.getCameraIntrinsics(camSocket, ispSize[0], ispSize[1]))
    d1 = np.array(calibData.getDistortionCoefficients(camSocket))
    R1 = np.identity(3)
    mapX, mapY = cv2.initUndistortRectifyMap(M1, d1, R1, M1, ispSize, cv2.CV_32FC1)

    meshCellSize = 16
    mesh0 = []
    # Creates subsampled mesh which will be loaded on to device to undistort the image
    for y in range(mapX.shape[0] + 1): # iterating over height of the image
        if y % meshCellSize == 0:
            rowLeft = []
            for x in range(mapX.shape[1]): # iterating over width of the image
                if x % meshCellSize == 0:
                    if y == mapX.shape[0] and x == mapX.shape[1]:
                        rowLeft.append(mapX[y - 1, x - 1])
                        rowLeft.append(mapY[y - 1, x - 1])
                    elif y == mapX.shape[0]:
                        rowLeft.append(mapX[y - 1, x])
                        rowLeft.append(mapY[y - 1, x])
                    elif x == mapX.shape[1]:
                        rowLeft.append(mapX[y, x - 1])
                        rowLeft.append(mapY[y, x - 1])
                    else:
                        rowLeft.append(mapX[y, x])
                        rowLeft.append(mapY[y, x])
            if (mapX.shape[1] % meshCellSize) % 2 != 0:
                rowLeft.append(0)
                rowLeft.append(0)

            mesh0.append(rowLeft)

    mesh0 = np.array(mesh0)
    meshWidth = mesh0.shape[1] // 2
    meshHeight = mesh0.shape[0]
    mesh0.resize(meshWidth * meshHeight, 2)

    mesh = list(map(tuple, mesh0))

    return mesh, meshWidth, meshHeight

def create_pipeline(calibData):
    pipeline = dai.Pipeline()

    cam = pipeline.create(dai.node.ColorCamera)
    cam.setIspScale(ispScale)
    cam.setBoardSocket(camSocket)
    cam.setResolution(camRes)

    manip = pipeline.create(dai.node.ImageManip)
    mesh, meshWidth, meshHeight = getMesh(calibData, cam.getIspSize())
    manip.setWarpMesh(mesh, meshWidth, meshHeight)
    manip.setMaxOutputFrameSize(cam.getIspWidth() * cam.getIspHeight() * 3 // 2)
    cam.isp.link(manip.inputImage)

    cam_xout = pipeline.create(dai.node.XLinkOut)
    cam_xout.setStreamName("Undistorted")
    manip.out.link(cam_xout.input)

    dist_xout = pipeline.create(dai.node.XLinkOut)
    dist_xout.setStreamName("Distorted")
    cam.isp.link(dist_xout.input)

    return pipeline

cx = 0
cy = 0

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

with dai.Device() as device:

    calibData = device.readCalibration()
    pipeline = create_pipeline(calibData)
    device.startPipeline(pipeline)

    queues = [device.getOutputQueue(name, 4, False) for name in ['Undistorted', 'Distorted']]

    while True:
        for q in queues:
            if q.getName()=='Undistorted':
                # print(q.getName())
                frame = q.get().getCvFrame()
                crop = frame[3:535, 232:745]
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
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                hStack = np.hstack([crop, mask, result])
                cv2.imshow('Horizontal Stacking', hStack)
                # cv2.imshow(stream, frame)
                # cv2.imshow('roi', crop)
                # cv2.imshow('mask', mask)

        if cv2.waitKey(1) == ord('q'):
            break
cv2.destroyAllWindows

print(h_min,s_min,v_min)
print(h_max,s_max, v_max)

block = int(input('enter "1" for block 1, "2" for block 2, and "3" for block 3 :\n'))

if block == 1:
    file = 'b1'
    file = file + '.txt'
if block == 2:
    file = 'b2'
    file = file + '.txt'
if block == 3:
    file = 'b3'
    file = file + '.txt'

print(str(h_min) + str(' ') + str(s_min) + str(' ') + str(v_min) + '\n' + 
      str(h_max) + str(' ') + str(s_max) + str(' ') + str(v_max), file=open(file, 'w'))

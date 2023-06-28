# this code will detect the block b1, b2, and b3 
# using the file b1.txt, b2.txt, b3.txt

#!/usr/bin/env python3
import cv2
import depthai as dai
import time
import numpy as np
block = ''
def l_u(block):
    lower = ()
    upper = ()
    lower = list(lower)
    upper = list(upper)
    file_name = block + '.txt'
    with open(file_name, "r") as file:
        data = file.readlines()
        i = 1
        for line in data:
            hsv = line.split()
            j = 0
            for val in hsv:
                if i==1 and j<=2:
                    lower.append(int(val))
                elif i ==2:
                    upper.append(int(val))
                j = j + 1
            i = i+1
    lower = tuple(lower)
    upper = tuple(upper)
    return lower, upper

b1_lower, b1_upper = l_u('b1')
b2_lower, b2_upper = l_u('b2')
b3_lower, b3_upper = l_u('b3')

def coordinate(block, contours, img):
    points = []
    cx = 0
    cy = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 0)
    thickness = 2
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                # cv2.drawContours(img, contour, -1, (255,0,0), 2)
                # cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
                
                x1, y1, x2, y2 = x, y, x+w, y+h
                if x1>x2:
                    xmax = x1
                    xmin = x2
                else:
                    xmax = x2
                    xmin = x1
                if y1>y2:
                    ymax = y1
                    ymin = y2
                else:
                    ymax = y2
                    ymin = y1
                points.append([x,y])
                points.append([x+w,y])
                points.append([x,y+h])
                points.append([x+w,y+h])
                cv2.circle(img, (xmax,ymax), 3, (0,255,255), -1)
                cv2.circle(img, (xmax,ymin), 3, (0,255,255), -1)
                cv2.circle(img, (xmin,ymax), 3, (0,255,255), -1)
                cv2.circle(img, (xmin,ymin), 3, (0,255,255), -1)
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)
                cx = int(x+(w/2))
                cy = int(y+(h/2))
                cv2.circle(img, (cx, cy), 5, (0,255,255), -1)
                cv2.putText(img, '  ' + block, (cx, cy), font, font_scale, color,thickness)
                # print(block, points)
    return img, cx, cy

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

with dai.Device() as device:

    calibData = device.readCalibration()
    pipeline = create_pipeline(calibData)
    device.startPipeline(pipeline)

    queues = [device.getOutputQueue(name, 4, False) for name in ['Undistorted', 'Distorted']]

    while True:
        for q in queues:
            if q.getName() == 'Undistorted':
                frame = q.get().getCvFrame()
                crop = frame[3:535, 232:745]

                cropHsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
                mask1 = cv2.inRange(cropHsv, b1_lower, b1_upper)
                mask2 = cv2.inRange(cropHsv, b2_lower, b2_upper)
                mask3 = cv2.inRange(cropHsv, b3_lower, b3_upper)
                contours1, hierarcy1 = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours2, hierarcy2 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours3, hiearcy3 = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (0, 255, 255)
                thickness = 2
                
                crop, cx1, cy1 = coordinate('1',contours1, crop)
                crop, cx2, cy2 = coordinate('2',contours2, crop)
                crop, cx3, cy3 = coordinate('3',contours3, crop)

                # cv2.imshow(q.getName(), frame)
                cv2.imshow(q.getName() + ' crop', crop)

        if cv2.waitKey(1) == ord('q'):
            if cx1 != 0 and cy1 != 0:
                print('b1 is at:', cx1, cy1)
                print(cropHsv[cx1][cy1])
            if cx2 != 0 and cy2 != 0:
                print('b2 is at:', cx2, cy2)
            if cx3 != 0 and cy3 != 0:
                print('b3 is at:', cx3, cy3)
            print(crop.shape)
            break
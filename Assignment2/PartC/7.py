#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(500, 400)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)

#image stiching
def image_stiching(img1,img2,img3):
    imgs = []
    imgs.append(cv2.imread(img1))
    imgs.append(cv2.imread(img2))
    imgs.append(cv2.imread(img3))
    stitchy=cv2.Stitcher.create()
    (dummy,output)=stitchy.stitch(imgs)
    if dummy != cv2.STITCHER_OK:
            print("stitching ain't successful")
    else:
            print('Your Panorama is ready!!!')
    cv2.imshow('final result',output)
    cv2.waitKey(0)
    
# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
    first_frame = 0
    while True:
        videoIn = video.get()
        cv2.imshow("video", videoIn.getCvFrame())
        if cv2.waitKey(1) == ord('c'):
            cv2.imwrite('rgb_image'+str(first_frame)+'.jpg', videoIn.getCvFrame())
            first_frame += 1
        if cv2.waitKey(1) == ord('q'):
            break
    image_stiching('rgb_image0.jpg','rgb_image1.jpg','rgb_image2.jpg')       

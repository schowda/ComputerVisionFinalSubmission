
# corner detection with Harris Corner Detection Method
 

import cv2
import numpy as np
 
image = cv2.imread('pavan.jpeg')
 
operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
operatedImage = np.float32(operatedImage)
 
corners = cv2.cornerHarris(operatedImage, 2, 5, 0.07)
 
corners = cv2.dilate(corners, None)
 

image[corners > 0.01 * corners.max()]=[0, 0, 255]
 
cv2.imshow('Image with Borders', image)

cv2.imwrite("output1.jpeg",image)
 
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
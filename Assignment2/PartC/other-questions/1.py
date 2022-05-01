import numpy as np
import os
import cv2
import matplotlib.pyplot as plt



def make_img_grey(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def make_img_gaussian(img):
    return cv2.GaussianBlur(img, (5, 5), 1.4)

def pre_process_image(img):
    img = make_img_grey(img)
    img = make_img_gaussian(img)
    return img

def get_polar_co_ordinated(img):
    gx = cv2.Sobel(np.float32(img), cv2.CV_64F, 1, 0, 3)
    gy = cv2.Sobel(np.float32(img), cv2.CV_64F, 0, 1, 3)
    mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees = True)
    return mag, ang

def edge_detector(img, weak_th = None, strong_th = None):
    
    img = pre_process_image(img)
    
    mag, ang = get_polar_co_ordinated(img)

       
    mag_max = np.max(mag)
    if not weak_th: weak_th = mag_max * 0.1
    if not strong_th: strong_th = mag_max * 0.5
    
    height, width = img.shape
    grad_threshold = 22.5
    rotation = 45

    for i_x in range(width):
        for i_y in range(height):
               
            grad_ang = ang[i_y, i_x]
            grad_ang = abs(grad_ang-180) if abs(grad_ang)>180 else abs(grad_ang)
            
            if grad_ang<= grad_threshold:
                x_1, y_1 = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y

            if grad_ang>grad_threshold and grad_ang<=(grad_threshold + rotation):
                x_1, y_1 = i_x-1, i_y-1
                neighb_2_x, neighb_2_y = i_x + 1, i_y + 1
            
            if grad_ang>(grad_threshold + rotation) and grad_ang<=(grad_threshold + (rotation*2)):
                x_1, y_1 = i_x, i_y-1
                neighb_2_x, neighb_2_y = i_x, i_y + 1
            
            if grad_ang>(grad_threshold + (rotation*2)) and grad_ang<=(grad_threshold + (rotation*3)):
                x_1, y_1 = i_x-1, i_y + 1
                neighb_2_x, neighb_2_y = i_x + 1, i_y-1
            
            if grad_ang>(grad_threshold + (rotation*3)) and grad_ang<=(grad_threshold + (rotation*4)):
                x_1, y_1 = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y
            
            if width>x_1>= 0 and height>y_1>= 0:
                if mag[i_y, i_x]<mag[y_1, x_1]:
                    mag[i_y, i_x]= 0
                    continue
   
            if width>neighb_2_x>= 0 and height>neighb_2_y>= 0:
                if mag[i_y, i_x]<mag[neighb_2_y, neighb_2_x]:
                    mag[i_y, i_x]= 0

    ids = np.zeros_like(img)
       
    for i_x in range(width):
        for i_y in range(height):
              
            grad_mag = mag[i_y, i_x]
              
            if grad_mag<weak_th:
                mag[i_y, i_x]= 0
            elif strong_th>grad_mag>= weak_th:
                ids[i_y, i_x]= 1
            else:
                ids[i_y, i_x]= 2
       
    return mag
   
frame = cv2.imread('pavan.jpeg')
canny_img = edge_detector(frame)
   

plt.figure()
f, plots = plt.subplots(2, 1) 
plots[0].imshow(frame)
plots[1].imshow(canny_img)
cv2.imwrite("Output.jpeg",canny_img)

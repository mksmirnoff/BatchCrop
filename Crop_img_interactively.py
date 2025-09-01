# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 13:19:32 2025

@author: msmirnov
"""

import cv2
import numpy as np

# Global variables to store shape position and drawing state
drawing = False
x_shape, y_shape = -1, -1

# Create a black image
# img = np.zeros((500, 500, 3), np.uint8)

img = cv2.imread("Original.png")
img0 = img.copy()

def draw_shape_on_mouse(event, x, y, flags, param):
    global drawing, x_shape, y_shape

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_shape, y_shape = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Clear the previous drawing of the shape
            # img[:] = 0  # Fill the image with black (or redraw background)            
            img[:] = img0[:]
            # Draw the shape at the current mouse position
            cv2.circle(img, (x, y), 200, (0, 0, 255), 2) # Example: green circle
            x_shape, y_shape = x, y # Update shape position
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Create window and set mouse callback
cv2.namedWindow('ROI selection')
cv2.setMouseCallback('ROI selection', draw_shape_on_mouse)

while True:
    cv2.imshow('ROI selection', img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27: # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
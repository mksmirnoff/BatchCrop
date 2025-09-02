# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 13:19:32 2025

@author: msmirnov

Manual:
1. Set up folder with uncropped images in line 20.
2. Run the script.
3. For each image:
    - Click and drag red rectangle to desired position.
    - Repeat the preveous item if necessary.
    - Press 'Esc' to exit program.
    - Press any other key to preview the cropped image.
    - Press any key to save the cropped image
      and proceed to the next photo.
"""

import cv2
import os
import sys

import tkinter as tk
from tqdm import tqdm

img_folder = 'GoPro'   #Set up image folder here !!!!!!!

jpg_list = []
for filename in os.listdir(img_folder):
    if filename.lower().endswith((".jpg", ".jpeg")) and os.path.isfile(os.path.join(img_folder, filename)):
        jpg_list.append(os.path.join(img_folder, filename))
        
Njpg = len(jpg_list)
print(f'\n{Njpg} jpg images found in folder {img_folder}\n')        

# Check if the directory exists, and create it if it doesn't
crop_folder = os.path.join(img_folder, 'Cropped')
if not os.path.exists(crop_folder):
    os.makedirs(crop_folder) # Use makedirs to create intermediate directories if needed
    print(f"Directory '{crop_folder}' created.")
else:
    print(f"Directory '{crop_folder}' already exists.")

#Find screen size
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy() # Close the Tkinter root window

for img_fname in tqdm(jpg_list):
    _, img_file = os.path.split(img_fname)
    print(img_file)
    #img_fname = os.path.join(img_folder, img_file)
    
    # Global variables to store shape position and drawing state
    drawing = False
    x_shape, y_shape = -1, -1
    
    img = cv2.imread(img_fname)
    img0 = img.copy()
    h0, w0 = img.shape[:2]  #height and width of original image
    hh = int(w0 * 9 / 16)   #cropped height 
    yyy = int(hh/2)
    
    def draw_shape_on_mouse(event, x, y, flags, param):
        global drawing, x_shape, y_shape, yyy
    
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x_shape, y_shape = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                # Clear the previous drawing of the shape
                # img[:] = 0  # Fill the image with black (or redraw background)            
                img[:] = img0[:]
                # Draw the shape at the current mouse position
                #cv2.circle(img, (x, y), 200, (0, 0, 255), 2) # Example: green circle
                cv2.rectangle(img, (0, int(y - hh/2)), (w0, int(y + hh/2)), (0, 0, 255), 7 )
                x_shape, y_shape = x, y # Update shape position            
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            yyy = y_shape
    
    # Create window and set mouse callback
    cv2.namedWindow('ROI selection', cv2.WINDOW_KEEPRATIO)
    
    height1 = int(0.8 * screen_height)
    width1 = int(height1 * w0 /h0)
    cv2.resizeWindow('ROI selection', width1, height1)
    cv2.setMouseCallback('ROI selection', draw_shape_on_mouse)
    
    while True:
        cv2.imshow('ROI selection', img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27: # Press 'Esc' to exit program
            cv2.destroyAllWindows()
            sys.exit('Stopped by user')
        if key != 255: # Press any key to proceed to next photo       
            break    
       
    # Cropping image:
    x_start = 0
    x_end = w0
    y_start = int(yyy - hh/2)
    y_end = int(yyy + hh/2)    
    cropped_image = img0[y_start:y_end, x_start:x_end]  
    
    
    cv2.namedWindow('Cropped image', cv2.WINDOW_NORMAL)
    width2 = int(0.8 * screen_width)
    height2 = int(width2 * hh / w0)
    cv2.resizeWindow('Cropped image', width2, height2) 
    
    cv2.imshow('Cropped image', cropped_image) 
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    img_fname_cropped = os.path.join(crop_folder, img_file)    
    cv2.imwrite(img_fname_cropped, cropped_image)

print('All Photos Cropped!!!')
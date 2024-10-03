import cv2
import pywt
import numpy as np



def wavelett_trans(img, mode='haar', level=1):
    img_arr = img
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    
    img_arr = np.float32(img_arr)
    img_arr = img_arr/255
    
    coeffs = pywt.wavedec2(img_arr, mode, level=level)
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0
    
    img_arr_H = pywt.waverec2(coeffs_H, mode)
    img_arr_H *= 255
    img_arr_H = np.uint8(img_arr_H)
    
    return img_arr_H
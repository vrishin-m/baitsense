import cv2
import numpy as np
import sys

def get_average_saturation(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    avg_saturation = np.mean(saturation)
    return avg_saturation/255

print(get_average_saturation(r"C:\Users\mahad\Desktop\Vrishin's Office\Blender\Projects\Renders\medieval-house.png"))


import numpy as np
import math
def vincenty_inverse(x1, y1, x2, y2):#,z1):
    result = {}
    cor1 = np.array([x1,y1])
    cor2 = np.array([x2, y2])
    #correct_angle = -z1*math.pi/180.0
    vec = cor2 - cor1
    distance = np.linalg.norm(cor1-cor2)
    angle = np.arctan2(vec[0], vec[1]) # correct_angle
    result["distance"] = distance
    result["angle"] = angle
    return result
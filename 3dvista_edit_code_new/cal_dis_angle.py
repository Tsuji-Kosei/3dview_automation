import numpy as np
def vincenty_inverse(x1, y1, x2, y2):
    result = {}
    cor1 = np.array([x1,y1])
    cor2 = np.array([x2, y2])
    vec = cor2 - cor1
    distance = np.linalg.norm(cor1-cor2)
    angle = np.arctan2(vec[0], vec[1])
    result["distance"] = distance
    result["angle"] = angle
    return result
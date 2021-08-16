import argparse
import os
import zipfile
import glob
import json
import shutil
import cv2
import numpy as np
from extract_gui_data import unzipping
from make_project import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name',type=str, help='.vtpを抜いたプロジェクトファイル名を入力する')
    parser.add_argument('--database', action='store_true')
    parser.add_argument('--copy', action='store_true')
    args = parser.parse_args()

    # unzipping()
    # path_list, angle_list = taking_image_path()
    # print(path_list)
    # print(angle_list)
    # for i in range(len(path_list)):
    #     image = cv2.imread(path_list[i])
    #     height, width = image.shape[:2]
    #     img_merge = image_shift(image, angle_list[i])
    #     cv2.imwrite(os.path.join("Images", os.path.basename(path_list[i])), img_merge, [cv2.IMWRITE_JPEG_QUALITY, 100])
    # RPA
    edit_vista(args)
    #preview

if __name__ == "__main__":
    main()

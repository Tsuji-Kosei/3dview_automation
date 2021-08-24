import os
import zipfile
import glob
import json
import shutil
import cv2
import numpy as np

def mv_info():
    json_open = open("Images/coordinates.json", "r")
    json_load = json.load(json_open)
    json_next_load = json_load["markers"]
    info_image_path = []
    # destination_info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project")
    # os.mkdir("Image_info")
#print(json_next_load.keys())
    for key in json_next_load.keys():
        # print(json_next_load[key][2].keys())
        flug_nothing = False
        if len(json_next_load[key])== 2: flug_nothing =True
        if not flug_nothing:
            if "Info" in json_next_load[key][2].keys():
                for i in range(len(json_next_load[key][2]["Info"])):
                    info_image_path.append(os.path.basename(
                        json_next_load[key][2]["Info"][i][0]))
            else: pass
        

    # print(info_image_path)
    for i in range(len(info_image_path)):
        info_image_path[i] = os.path.join("Images", info_image_path[i])

    info_image_path = list(set(info_image_path))
    # print(info_image_path)

    for i in range(len(info_image_path)):
        try:
            shutil.move(info_image_path[i], "project")
        except shutil.Error as err:
            if os.path.isfile(info_image_path[i]):
                os.remove(info_image_path[i])
                print("already exist info image in project dir")


def unzipping():
    if os.path.isdir("Images"):
        print("A")
        shutil.rmtree("Images")

    destination_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    #create the folder to save the data from gui app

    #os.makedirs(destination_path, exist_ok=True)

    # if os.path.exists(os.path.join(destination_path, "Images")):
    #     os.remove(os.path.join(destination_path, "Images"))

    # decompress a zipped file from gui app
    zipfile_name_list = glob.glob('*.zip')
    if len(zipfile_name_list) == 1:
        zipfile_name = zipfile_name_list[0]
    else:
        print("connot identify the zip file from gui APP")
        return None

    print(zipfile_name)
    with zipfile.ZipFile(zipfile_name) as myzip:
        myzip.extractall(destination_path)

    mv_info()
    # delete the opened zipfile
    #os.remove(zipfile_name)

def taking_image_path():
    json_open = open("Images/coordinates.json","r")
    json_load = json.load(json_open)
    json_next_load = json_load["markers"]
    panorama_path = [] # panorama no path
    correction_angle = [] # images angles

    for json_path in json_next_load.keys():
        if json_path not in panorama_path:
            panorama_path.append(json_path)

    for i in range(len(panorama_path)):
            panorama_path[i] = os.path.join("Images/",panorama_path[i])
    
    for json_angle in json_next_load.values():
        correction_angle.append(json_angle[2])

    if len(panorama_path) != len(correction_angle) :
        print("!!! The number of data does not match the number of angle data !!!")

    return panorama_path, correction_angle

def image_shift(image, direction):
    height, width = image.shape[:2]

    ratio = 1 - direction/360

    img_translation1 = image[0:height, 0:int(width*ratio)]
    img_translation2 = image[0:height, int(width*ratio):width]


    img_merge = cv2.hconcat([img_translation2, img_translation1])
    height, width = img_merge.shape[:2]
    return img_merge	 



if __name__ == "__main__":
    unzipping()
    # path_list, angle_list = taking_image_path()
    # print(path_list)
    # print(angle_list)
    # for i in range(len(path_list)):
    #     image = cv2.imread(path_list[i])
    #     height, width = image.shape[:2]
    #     img_merge = image_shift(image, angle_list[i])
    #     cv2.imwrite(os.path.join("Images", os.path.basename(path_list[i])), img_merge, [cv2.IMWRITE_JPEG_QUALITY, 100])

import cv2
import numpy as np
import json
import os

def taking_image_path():
	json_open = open("coordinates_dummy.json","r")
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
	# print(height, width)

	# cv2.imshow("Originalimage", image)
	# cv2.imshow('Translation1', img_translation1)
	# cv2.imshow('Translation2', img_translation1)
	# cv2.imshow('Merged', img_merge)
	# cv2.waitKey()
	# cv2.destroyAllWindows()
	return img_merge		


if __name__=="__main__":
	path_list, angle_list = taking_image_path()
	print(path_list)
	print(angle_list)
	for i in range(len(path_list)):
		image =  cv2.imread(path_list[i])
		
		height, width = image.shape[:2]
		img_merge = image_shift(image, angle_list[i])
		cv2.imwrite(os.path.join("Images",os.path.basename(path_list[i])), img_merge,[cv2.IMWRITE_JPEG_QUALITY, 100])

	# image = cv2.imread('C:\\Users\\root\\Desktop\\3dview_automation\\3dvista_edit_code_new\\Images\\1.JPG')
	# height, width = image.shape[:2]
	# image = cv2.resize(image, dsize=(int(width/5), int(height/5))) ##ここをなくしたら余計に悪くなった

	#img_merge = image_shift(image, 90)
	# img_merge2 = cv2.resize(img_merge,dsize=(int(width*5), int(height*5)))
	# cv2.imshow("Originalimage", image)
	# cv2.imshow('Merged', img_merge)
	# cv2.imwrite("out_sample3.JPG", img_merge,[cv2.IMWRITE_JPEG_QUALITY, 100])
	# cv2.waitKey()
	# cv2.destroyAllWindows()
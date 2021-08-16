import json
import os
import shutil
#This code moves info image in Images-dir to project-dir. This is just made in a hurry, customize in anyway you want

json_open = open("Images/coordinates.json","r")
json_load = json.load(json_open)
json_next_load = json_load["markers"]
info_image_path = []

#print(json_next_load)
for json_data in json_next_load.values():
	if len(json_data) > 2 : #if you have cirrection angle, turn 2 to 3
		for i in [2,len(json_data)-1]:
			if os.path.basename(json_data[i][0]) not in info_image_path:
				info_image_path.append(os.path.basename(json_data[i][0]))

if len(info_image_path) == 0: 
	pass
elif len(info_image_path) == 1 :
	info_image_path[0] = os.path.join("Images/",info_image_path[0])
else :
	for i in len(info_image_path): #ここをrangeで書くと画像が認識できませんのエラーが良く出た
		info_image_path[i] = os.path.join("Images/",info_image_path[i])
if len(info_image_path) == 0:
	print("No info images")
else:
	print("info images are following ↓↓↓↓")
	print(info_image_path)

if len(info_image_path) == 0 :
	pass
elif len(info_image_path) == 1 :
	shutil.move(info_image_path[0], "project/Images_info")
else:
	for i in len(info_image_path):
		shutil.move(info_image_path[i],"project/Images_info")
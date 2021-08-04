import json
import os
import shutil

json_open = open("3dvista_edit_code_new/Image/coordinates.json","r")
json_load = json.load(json_open)
json_next_load = json_load["markers"]
info_image_path = []

#print(json_next_load)
for json_data in json_next_load.values():
	if len(json_data) > 2 : 
		for i in [2,len(json_data)-1]:
			if os.path.basename(json_data[i][0]) not in info_image_path:
				info_image_path.append(os.path.basename(json_data[i][0]))

if len(info_image_path) == 1 :
	info_image_path[0] = os.path.join("Images/",info_image_path[0])
else :
	for i in len(info_image_path):
		info_image_path[i] = os.path.join("Images/",info_image_path[i])
print(info_image_path)

if len(info_image_path) == 1 :
	shutil.move(info_image_path[0], "project")
else:
	for i in len(info_image_path):
		shutil.move(info_image_path[i],"project")
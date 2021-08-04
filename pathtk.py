import json
import os

def taking_path_and_angle():
	json_open = open("coordinates.json","r")
	json_load = json.load(json_open)
	json_next_load = json_load["markers"]
	panorama_path = []
	correction_angle = []

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

if __name__=="__main__":
	a,b = taking_path_and_angle()
	print(a)








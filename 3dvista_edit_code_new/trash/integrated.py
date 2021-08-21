import os
import sys
import shutil
import zipfile
from Edit_Script import Add_Json_Data
import create_database
import cv2

def edit_vista(args):
    vtp_name = args.name + ".vtp"
    zip_name = args.name + ".zip"
    vtp_copy_name = args.name + "_copy.vtp"
    project_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"project")
    vtp_path = os.path.join(project_directory_path,vtp_name)
    vtp_copy_path = os.path.join(project_directory_path,vtp_copy_name)
    zip_path = os.path.join(project_directory_path,zip_name)
    extractzip_directory_path = os.path.join(project_directory_path,args.name)
    cordinate_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Images/coordinates.json")
    data_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_base.js")
    script_path = os.path.join(extractzip_directory_path,"script.js")


    # コピーを作るなら、プロジェクトファイルをコピーする
    if os.path.exists(vtp_path):
        if args.copy:
            shutil.copyfile(vtp_path,vtp_copy_path)
    else:
        print("not exist the file")
        sys.exit(1)

    # (priject_name).vtpを(priject_name).zipに変える
    os.rename(vtp_path, zip_path)

    # 変換されたzipファイルを解凍
    with zipfile.ZipFile(zip_path) as existing_zip:
        existing_zip.extractall(extractzip_directory_path)

    # zipファイルを削除
    os.remove(zip_path)

    # プロジェクトファイルのscript.jsを編集
    create_database.create_db(cordinate_data_path,data_base_path)
    AJD = Add_Json_Data(script_path, data_base_path)
    AJD.insert_overlays()
    AJD.insert_areas_hotspot()
    AJD.insert_areas_info()
    AJD.insert_areas_url()
    AJD.insert_behaviours_hotspot()
    AJD.insert_behaviours_info()
    AJD.insert_behaviours_url()
    AJD.insert_behaviours_url_two()
    AJD.save_to_json(script_path)
    AJD.file_close()

    # 解凍したファイルを再びzipファイルに圧縮する
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        new_zip.write(os.path.join(extractzip_directory_path,"script.js"),"script.js")
        new_zip.write(os.path.join(extractzip_directory_path,"info"),"info")
        new_zip.write(os.path.join(extractzip_directory_path,"version"),"version")


    # databaseを残さないなら、database.jsを消去
    #if not args.database:
    #    os.remove(data_base_path)
    
    # zipファイルを.vtpに変換
    os.rename(zip_path, vtp_path)

    # 圧縮前のプロジェクトフォルダを消去
    shutil.rmtree(extractzip_directory_path)

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
	# print(height, width)

	# cv2.imshow("Originalimage", image)
	# cv2.imshow('Translation1', img_translation1)
	# cv2.imshow('Translation2', img_translation1)
	# cv2.imshow('Merged', img_merge)
	# cv2.waitKey()
	# cv2.destroyAllWindows()
	return img_merge




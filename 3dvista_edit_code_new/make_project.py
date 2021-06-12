import os
import sys
import shutil
import zipfile
import zlib
from Edit_Script import Add_Json_Data
import create_database_new
import time

def edit_vista(args):
    vtp_name = args.name + ".vtp"
    zip_name = args.name + ".zip"
    vtp_copy_name = args.name + "_copy.vtp"
    project_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"project")
    vtp_path = os.path.join(project_directory_path,vtp_name)
    vtp_copy_path = os.path.join(project_directory_path,vtp_copy_name)
    zip_path = os.path.join(project_directory_path,zip_name)
    extractzip_directory_path = os.path.join(project_directory_path,args.name)
    cordinate_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"coordinates2.json")
    data_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_base.js")
    script_path = os.path.join(extractzip_directory_path,"script.js")

    # print(project_directory_path)
    # print(vtp_path)
    # print(zip_path)
    # print(extractzip_directory_path)
    # print(cordinate_data_path)
    # print(data_base_path)
    # print(script_path)

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
    create_database_new.create_db(cordinate_data_path,data_base_path, distance_limit = args.distance)
    AJD = Add_Json_Data(script_path, data_base_path)
    AJD.insert_overlays()
    AJD.insert_areas()
    AJD.insert_behaviours()
    AJD.save_to_json(script_path)
    AJD.file_close()

    # 解凍したファイルを再びzipファイルに圧縮する
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        new_zip.write(os.path.join(extractzip_directory_path,"script.js"),"script.js")
        new_zip.write(os.path.join(extractzip_directory_path,"info"),"info")
        new_zip.write(os.path.join(extractzip_directory_path,"version"),"version")


    # databaseを残さないなら、database.jsを消去
    if not args.database:
        os.remove(data_base_path)
    
    # zipファイルを.vtpに変換
    os.rename(zip_path, vtp_path)

    # 圧縮前のプロジェクトフォルダを消去
    shutil.rmtree(extractzip_directory_path)
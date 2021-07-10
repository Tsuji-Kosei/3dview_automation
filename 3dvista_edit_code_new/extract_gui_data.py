import os
import zipfile
import glob
def main(): 

    destination_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Images")

    # create the folder to save the data from gui app
    os.makedirs(destination_path, exist_ok=True)

    # decompress a zipped file from gui app
    zipfile_name_list = glob.glob('*.zip')
    if len(zipfile_name_list)==1:
        zipfile_name = zipfile_name_list[0]
    else:
        print("connot identify the zip file from gui APP")
        return None

    print(zipfile_name)
    with zipfile.ZipFile(zipfile_name) as myzip:
        myzip.extractall(destination_path)

    # delete the opened zipfile
    os.remove(zipfile_name)

if __name__ == "__main__":
    main()

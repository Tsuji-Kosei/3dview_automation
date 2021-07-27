import json
from cal_dis_angle import vincenty_inverse

def create_db(original_path, data_path):
    json_open = open(original_path,'r')
    json_load = json.load(json_open)

    coordinates_info = json_load["markers"]
    line_segments = json_load["line_segments"]
    data_for_databese = {}

    #　hotspotに関する情報をまとめる
    for origin_image in line_segments: #origin_Imageは出発地点の画像の名前
        # print(origin_image)

        result_calculation = {}
        pre_result_calculation = [] #それぞれの写真に対してのhotspotで繋がっている画像名と座標のリストのリストを格納
        count = 0 # 次のloopで使用　リストに正しく格納するため

        for connected_image in line_segments[origin_image]:
            pre_result_calculation.append([])
            prepare_position = []
            prepare_position.append(coordinates_info[origin_image]) #taking original photos cord
            prepare_position.append(coordinates_info[connected_image]) #taking connected cord

            lat1 = prepare_position[0][0]  #出発地点の写真の座標
            lon1 = prepare_position[0][1]
            lat2 = prepare_position[1][0]   #つながる先の写真の座標
            lon2 = prepare_position[1][1]
            #correction_angle = prepare_position[0,2]

            result = vincenty_inverse(lat1, lon1, lat2, lon2)#,correction_angle) 

            pre_result_calculation[count].append(connected_image.split(".")[0])
            pre_result_calculation[count].append(result['angle'])
            count += 1

        result_calculation["hotspot"]=pre_result_calculation
        # dic_list =[] # infoの辞書とまとめるため急遽追加
        # dic_list.append(result_calculation)
        data_for_databese[origin_image.split(".")[0]] = result_calculation

    # infoに関する情報をまとめる
    for attached_image in coordinates_info: # attached_Imageが貼り付ける写真の画像名
        info_dic = {}
        info_list = []
        count=0
        for number_of_info in range(len(coordinates_info[attached_image])-2):
            info_list.append([])
            info_list[count]= coordinates_info[attached_image][number_of_info+2] #0,1には画像自体の座標が入っている。２個目以降がinfoに関する情報
            count +=1
        info_dic["info"] = info_list
        # print(info_dic)
        # print(data_for_databese[attached_image.split(".")[0]])
        data_for_databese[attached_image.split(".")[0]].update(info_dic)




    with open(data_path, mode='wt', encoding='utf-8') as file:
        json.dump(data_for_databese, file, ensure_ascii=False,indent=2)


def main():
    create_db("Images/coordinates.json","database.js")

if __name__ == "__main__":
    main()

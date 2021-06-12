import json
from cal_dis_angle import vincenty_inverse

def create_db(original_path, data_path, distance_limit = 100000):
    json_open = open(original_path,'r')
    json_load = json.load(json_open)
    
    panorama_name = []
    position = []
    result_calculation = []
    data_for_databese = {}
    for i in json_load.keys():
        panorama_name.append(i)
        position.append(json_load[i])
    
    
    if len(position)<=1:
        pass

    elif len(position)>1:
        for i in range(len(position)):
            result_calculation.append([])

        for i in range(len(position)):
            for j in range(len(position)):
                pre_result_calculation = []
                if i == j:
                    pass
                else:
                    lat1 = position[i][0]  
                    lon1 = position[i][1]
                    lat2 = position[j][0]
                    lon2 = position[j][1]
                    # print(lat1,lon1,lat2,lon2)
                    result = vincenty_inverse(lat1, lon1, lat2, lon2)
                    # print(result)
                    if result["distance"]<=distance_limit:
                        pre_result_calculation.append(panorama_name[j])
                        pre_result_calculation.append(result['distance'])
                        pre_result_calculation.append(result['angle'])
                        result_calculation[i].append(pre_result_calculation)
                    else:
                        pass
                    
        for i in range(len(panorama_name)):
            data_for_databese[panorama_name[i]] = result_calculation[i]

        with open(data_path, mode='wt', encoding='utf-8') as file:
            json.dump(data_for_databese, file, ensure_ascii=False, indent=2)

    else:
        pass

def main():
    create_db("first.js","test.js", distance_limit=1.1)

if __name__ == "__main__":
    main()

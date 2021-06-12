import json
from cal_dis_angle import vincenty_inverse

def create_db(original_path, data_path, distance_limit = 100000):
    json_open = open(original_path,'r')
    json_load = json.load(json_open)

    coordinates = json_load["markers"]
    line_segments = json_load["line_segments"]
    data_for_databese = {}

    for origin_image in line_segments:
        result_calculation = []
        for connected_image in line_segments[origin_image]:
            pre_result_calculation = []
            prepare_position = []

            prepare_position.append(coordinates[origin_image])
            prepare_position.append(coordinates[connected_image])

            lat1 = prepare_position[0][0]  
            lon1 = prepare_position[0][1]
            lat2 = prepare_position[1][0]
            lon2 = prepare_position[1][1]

            result = vincenty_inverse(lat1, lon1, lat2, lon2)

            # print(connected_image)
            pre_result_calculation.append(connected_image.split(".")[0])
            pre_result_calculation.append(result['angle'])
            result_calculation.append(pre_result_calculation)
        # print(result_calculation)
        data_for_databese[origin_image.split(".")[0]] = result_calculation

        with open(data_path, mode='wt', encoding='utf-8') as file:
            json.dump(data_for_databese, file, ensure_ascii=False, indent=2)

    else:
        pass

def main():
    create_db("coordinates.json","test.js", distance_limit=1.1)

if __name__ == "__main__":
    main()

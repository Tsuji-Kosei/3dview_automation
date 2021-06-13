import json
import os
import math
import time

class Add_Json_Data():
    def __init__(self, path, dbpath):
        self.path = path
        self.dbpath = dbpath
        self.json_open = open(self.path,'r', encoding='cp932', errors='ignore')
        self.db_open = open(self.dbpath,'r')
        self.json_load = json.load(self.json_open) #3Dvistaのプロジェクトファイルの中のscript.js
        self.db_load = json.load(self.db_open) #detabase.js
        self.number_panorama = 0      #登録されている写真の枚数
        self.connect_hotspot = {}      #{出発地点の画像名:[[繋がり先の画像名,x座標,y座標],[],  ,,}の辞書
        self.connect_info = {}      #{infoが貼られる画像名:[[ローカルの画像名,x座標,y座標],[],  ,,}の辞書
        self.number_info = {}       # 辞書(出発地点の画像名:3, ,, } (1枚目の写真に３個、、、)
        self.number_hotspot = {}    # 辞書(infoが貼られる画像名:3, ,, } (1枚目の写真に３個、、、)
        self.overlays = {}      #{出発地点の画像名:[overlayのid,overlayのid,,  ], } の辞書　(idは前から順番につなげる先の写真に対応)
        self.areas = []
        self.behaviours = []
        self._get_number_panorama() #　self.number_panoramaに登録されている写真の枚数を格納
        self._get_connect_hotspot() # self.conncect.hotspotに、[[[つなげる先の写真名、x,y],[] , ],[],[]]という形のリストが入っている。大きな塊は登録されている写真の順番になっている。
        self._get_number_hotspot() # self.number_hotspotに、それぞれの写真に何枚の写真が繋がっているかのリスト[3,4,5] (1枚目の写真に３枚、、、)　を格納
        self._get_connect_info()
        self._get_number_info() 
        print(self.number_hotspot)
        print(self.number_info)
        print(self.connect_hotspot)
        print(self.connect_info)
        # self.remember_panorama_info() # script.jsの中のパノラマに関する情報をクラス変数に格納(詳しくはこの関数の先に書いています)

        self._get_overlays() #self.overlaysに、{出発地点の画像名:[overlayのid,overlayのid,,  ], } の辞書を格納
        # self._get_areas()   #self.areasに、[[１枚目のパノラマのareas, , , ],[2枚目のパノラマのareas, , , ],[] ,[]]]というリストを格納
        # self._get_behaviours() #self.behavioursに、[[１枚目のパノラマのbehaviours, , , ],[2枚目のパノラマのbehaviours, , , ],[] ,[]]]というリストを格納
        
    
    def _get_number_panorama(self):
        json_definition = self.json_load["player"]["definitions"]
        count = 0
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    count+=1
        self.number_panorama = count
    
    def _get_connect_hotspot(self):
        
        for i in self.db_load.keys():
            print(i)
            pre_connect_hotspot = []
            for j in range(len(self.db_load[i]["hotspot"])):
                angle = self.db_load[i]["hotspot"][j][1]
                pre_connect_hotspot.append([self.db_load[i]["hotspot"][j][0],700+700*angle/math.pi, angle*180/math.pi])  ##connect_hotspotに名前,x, yでappendしたい
            self.connect_hotspot[i]=pre_connect_hotspot

    def _get_connect_info(self):
        
        for i in self.db_load.keys():
            pre_connect_info = []
            for j in range(len(self.db_load[i]["info"])):
                pre_connect_info.append([self.db_load[i]["info"][j][0],self.db_load[i]["info"][j][1],self.db_load[i]["info"][j][2]])  ##connect_hotspotに名前,x, yでappendしたい
            self.connect_info[i]=pre_connect_info

    def _get_number_hotspot(self):
        for i in self.connect_hotspot.keys():
            self.number_hotspot[i]=len(self.connect_hotspot[i])
    
    def _get_number_info(self):
        for i in self.connect_info.keys():
            self.number_info[i]=len(self.connect_info[i])
    
    def _get_overlays(self): # 辞書の上から順に命名していく
        count = 0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):
                if j == 0: #まずkey作成
                    self.overlays[i] = {"overlays":[f"this.overlay_C{count}_{j}"]}
                else: # value追加
                    self.overlays[i]["overlays"].append(f"this.overlay_C{count}_{j}")
    
    def _get_areas(self):
        for i in range(self.number_panorama):
            self.areas.append([])

        for i in range(self.number_panorama):
            for j in range(self.number_hotspot[i]):
                yaw = 10*j
                self.areas[i].append({"areas":[f"this.HotspotPanoramaOverlayArea_C{i}_{j}"],
                        "class":"HotspotPanoramaOverlayEditable",
                        "excludeClickGoMode":False,
                        "items":[{"visibleOnStop":False,
                        "hfov":7.616601683506721,
                        "playEvent":"start",
                        "label":"Arrow 01",
                        "verticalAlign":"middle",
                        "width":33.33333333333333,
                        "loop":True,
                        "path":"hotspots/Hotspot_34559710_3D00_0B16_41B3_160403C9DC33.png",
                        "showFrameAtStart":0,
                        "stopEvent":"none",
                        "class":"HotspotPanoramaOverlayAnimatedBitmapImage",
                        "yaw":self.connect_hotspot[i][j][2],
                        "libraryData":{"type":"goToPanoramaWall",
                        "name":"arrow01",
                        "element":"IHotspotOverlayBitmapImage",
                        "family":"animated"},
                        "pitch":-20,
                        "pauseEvent":"none",
                        "x":self.connect_hotspot[i][j][1],
                        "fps":16,
                        "y":400,
                        "horizontalAlign":"center",
                        "scaleMode":"fit_inside",
                        "transparencyActive":True,
                        "factorHeight":3.751570132588974,
                        "distance":100,
                        "height":30,
                        "factorWidth":3.751570132588974}],
                        "rollOverDisplay":False,
                        "useHandCursor":True,
                        "maps":[],
                        "id":f"overlay_C{i}_{j}",
                        "hasChanges":True})

    def _get_behaviours(self):
        for i in range(self.number_panorama):
            self.behaviours.append([])

        for i in range(self.number_panorama):
            for j in range(self.number_hotspot[i]):
                connect_hotspot_id = self.remember_name_id[f"{self.connect_hotspot[i][j][0]}"] ##名前とidの辞書からパノラマのid取得
                self.behaviours[i].append({"class":"HotspotPanoramaOverlayArea",
                            "id":f"HotspotPanoramaOverlayArea_C{i}_{j}",
                            "behaviours":[{"media":f"this.{connect_hotspot_id}",    ###パノラマのid反映
                            "class":"PanoramaBehaviour",
                            "event":"click",
                            "startPointView":{"type":"smartPoint",
                            "class":"StartPointView"},
                            "sentences":[],
                            "inComponent":"this.MainViewer",
                            "action":"openPanorama",
                            "where":"inViewer"}]})

    def remember_context_panorama(self):
        self.remember_context = {}
        json_definition = self.json_load["player"]["definitions"]
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    self.remember_context[json_definition[i]["paths"].split(".")[0]]=json_definition[i]

    def remember_position_panorama(self):
        self.remember_number = []
        json_definition = self.json_load["player"]["definitions"]
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    self.remember_number.append(i)
    
    def remember_name_and_id_panorama(self):
        self.remember_path = [] # self.remember_pathにパノラマのローカルでのpathが格納される
        self.remember_id = [] # self.remember_idにパノラマに対応したidが格納される
        self.remember_filename = [] # self.remember_filenameに画像名の.JPGなどを抜いた名前が格納される
        self.remember_name_id = {}
        for i in range(len(self.remember_context)):
            self.remember_path.append(self.remember_context[i]["paths"])
            self.remember_id.append(self.remember_context[i]['id'])

        for i in range(len(self.remember_path)):
            self.remember_filename.append(os.path.basename(self.remember_path[i][0]).split(".")[0])
        
        count = 0
        for v in self.remember_filename:
            self.remember_name_id[f"{v}"] = self.remember_id[count]
            count += 1
    
    def remember_panorama_info(self): # script.jsのplayer->definitionsの中の"hfovMin"というキーを持つvalueがパノラマに関する情報
        self.remember_context_panorama() # {中身に対応する画像名:"hfovMin"というキーのvalueの中身,,,}がself.remember_contextに格納されてイル
        self.remember_position_panorama() # "hfovMin"というキーを持つ辞書が、definitionsの中の何番目にあったかを格納
        self.remember_name_and_id_panorama() # self.remember_name_idに{画像の名前(.JPG抜き): パノラマに対応したid} という辞書が格納される


    def insert_overlays(self):
        # overlayをそれぞれに追加
        for i in range(len(self.remember_context)):
            self.remember_context[i].update(self.overlays[i])

        # json_loadにoverlay追加したのを入れる
        count = 0
        for i in self.remember_number:
            self.json_load['player']['definitions'][i] = self.remember_context[count]
            count += 1
    
    def insert_areas(self):
        for i in range(self.number_panorama):
            for j in range(self.number_hotspot[i]):
                self.json_load["player"]["definitions"].append(self.areas[i][j])
    
    def insert_behaviours(self):
        for i in range(self.number_panorama):
            for j in range(self.number_hotspot[i]):
                self.json_load["player"]["definitions"].append(self.behaviours[i][j])

    # 編集したscript.jsを保存
    def save_to_json(self,save_path):
        with open(save_path, mode='wt', encoding='utf-8') as file:
            json.dump(self.json_load, file, ensure_ascii=False, indent=2)

    #　開いているjsonファイルを閉じる
    def file_close (self):
        self.json_open.close()
        self.db_open.close()


def main():
    AJD = Add_Json_Data("/Users/tsujikousei/Documents/rutelia/3dview_code/3dview_automation/3dvista_edit_code_new/script.js", "database.js")
    # AJD.insert_overlays()
    # AJD.insert_areas()
    # AJD.insert_behaviours()
    # AJD.save_to_json("script.json")
    # AJD.file_close()


if __name__ == "__main__":
    main()

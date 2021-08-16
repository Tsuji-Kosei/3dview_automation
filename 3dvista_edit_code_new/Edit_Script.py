import json
import os
import math
import time
from os.path import abspath, join, split


class Add_Json_Data():
    def __init__(self, path, dbpath):
        self.path = path
        self.dbpath = dbpath
        # self.info_dir_path =os.path.join(abspath(join(__file__, '../..')),"Images\info")
        self.json_open = open(self.path,'r', encoding='cp932', errors='ignore')
        self.db_open = open(self.dbpath,'r')
        self.json_load = json.load(self.json_open) #3Dvistaのプロジェクトファイルの中のscript.js
        self.db_load = json.load(self.db_open) #detabase.js
        self.number_panorama = 0      #登録されている写真の枚数
        self.connect_hotspot = {}      #{出発地点の画像名:[[繋がり先の画像名,x座標,y座標],[],  ,,}の辞書
        self.connect_info = {}      #{infoが貼られる画像名:[[ローカルの画像名,x座標,y座標],[],  ,,}の辞書
        self.connect_url = {}
        self.number_info = {}
        self.number_url = {}       # 辞書(出発地点の画像名:3, ,, } (1枚目の写真に３個、、、)
        self.number_hotspot = {}    # 辞書(infoが貼られる画像名:3, ,, } (1枚目の写真に３個、、、)
        self.overlays = {}      #{出発地点の画像名:[overlayのid,overlayのid,,  ], } の辞書　(idは前から順番につなげる先の写真に対応)
        self.areas_hotspot = [] #[[1つめのkey(貼られる画像の)overlayに対応したareasのリスト],[],,,]
        self.areas_info = [] ##[[1つめのkey(貼られる画像の)overlayに対応したareasのリスト],[],,,]
        self.areas_url = []
        self.behaviours_hotspot = [] ##[[1つめのbehaviour(貼られる画像の)overlayに対応したareasのリスト],[],,,]
        self.behaviours_info = [] ##[[1つめのbehaviour(貼られる画像の)overlayに対応したareasのリスト],[],,,]
        self.behaviours_url = []
        self._get_number_panorama() #　self.number_panoramaに登録されている写真の枚数を格納
        self._get_connect_hotspot() # self.conncect.hotspotに、{出発地点の画像名:[[繋がり先の画像名,x座標,y座標],[],  ,,}の辞書を格納
        self._get_number_hotspot() # self.number_hotspotに、辞書(infoが貼られる画像名:3, ,, } (1枚目の写真に３個、、、)　を格納
        self._get_connect_info()
        self._get_number_info() 
        self._get_connect_url()
        self._get_number_url() 

        self.remember_panorama_info() # script.jsの中のパノラマに関する情報をクラス変数に格納(詳しくはこの関数の先に書いています)

        self._get_overlays_hotspot() #self.overlaysに、{出発地点の画像名:[overlayのid,overlayのid,,  ], } の辞書を格納
        self._get_overlays_info()
        self._get_overlays_url()
        self._get_areas_hotspot()   #self.areas_hotspotに、[[１枚目のパノラマのareas, , , ],[2枚目のパノラマのareas, , , ],[] ,[]]]というリストを格納
        self._get_areas_info()
        self._get_areas_url()
        self._get_behaviours_hotspot() #self.behavioursに、[[１枚目のパノラマのbehaviours, , , ],[2枚目のパノラマのbehaviours, , , ],[] ,[]]]というリストを格納
        self._get_behaviours_info()
        self._get_behaviours_url()
    
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

    def _get_connect_url(self):
        
        for i in self.db_load.keys():
            pre_connect_url = []
            for j in range(len(self.db_load[i]["URL"])):
                pre_connect_url.append([self.db_load[i]["URL"][j][0],self.db_load[i]["URL"][j][1],self.db_load[i]["URL"][j][2]])  ##connect_hotspotに名前,x, yでappendしたい
            self.connect_url[i]=pre_connect_url

    def _get_number_hotspot(self):
        for i in self.connect_hotspot.keys():
            self.number_hotspot[i]=len(self.connect_hotspot[i])
    
    def _get_number_info(self):
        for i in self.connect_info.keys():
            self.number_info[i]=len(self.connect_info[i])

    def _get_number_url(self):
        for i in self.connect_url.keys():
            self.number_url[i]=len(self.connect_url[i])
    
    def _get_overlays_hotspot(self): # 辞書の上から順に命名していく
        count = 0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_C{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_C{count}_{j}")

            count +=1
    
    def _get_overlays_info(self): # 辞書の上から順に命名していく
        count = 0
        for i in self.number_info.keys():
            for j in range(self.number_info[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_D{count}_{j}",f"this.popup_D{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_D{count}_{j}")
                    self.overlays[i]["overlays"].append(f"this.popup_D{count}_{j}")

            count +=1

    def _get_overlays_url(self): # 辞書の上から順に命名していく
        count = 0
        for i in self.number_url.keys():
            for j in range(self.number_url[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_E{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_E{count}_{j}")

            count +=1
    
    def _get_areas_hotspot(self):
        for i in range(self.number_panorama):
            self.areas_hotspot.append([])

        count =0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):
                #yaw = 10*j
                self.areas_hotspot[count].append({"areas":[f"this.HotspotPanoramaOverlayArea_C{count}_{j}"],
                        "class":"HotspotPanoramaOverlayEditable",
                        "excludeClickGoMode":False,
                        "items":[{"visibleOnStop":False,
                        "playEvent":"start",
                        "label":"Arrow 01",
                        "verticalAlign":"middle",
                        "width":33.33333333333333,
                        "loop":True,
                        "path":"hotspots/Hotspot_34559710_3D00_0B16_41B3_160403C9DC33.png",
                        "showFrameAtStart":0,
                        "stopEvent":"none",
                        "class":"HotspotPanoramaOverlayAnimatedBitmapImage",
                        "libraryData":{"type":"goToPanoramaWall",
                        "name":"arrow01",
                        "element":"IHotspotOverlayBitmapImage",
                        "family":"animated"},
                        "pitch":-30,
                        "hfov":7.616601683506721,
                        "yaw":self.connect_hotspot[i][j][2],
                        "pauseEvent":"none",
                        "x":708+self.connect_hotspot[i][j][1]*math.sin(self.connect_hotspot[i][j][2]),
                        "fps":16,
                        "y":483,
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
                        "id":f"overlay_C{count}_{j}",
                        "hasChanges":True})
            count += 1
        
    def _get_areas_info(self):
        for i in range(self.number_panorama):
            self.areas_info.append([])

        count =0
        for i in self.number_info.keys():
            for j in range(self.number_info[i]):
                yaw = 10*j
                self.areas_info[count].append([{"excludeClickGoMode":False,
                                    "class":"HotspotPanoramaOverlayEditable",
                                    "areas":[f"this.HotspotPanoramaOverlayArea_D{count}_{j}"],
                                    "rollOverDisplay":False,
                                    "useHandCursor":True,
                                    "items":[{"x":self.connect_info[i][j][2]*1416/618.24,
                                    "class":"HotspotPanoramaOverlayBitmapImage",
                                    "transparencyActive":True,
                                    "y":self.connect_info[i][j][1]*700/1236.48,
                                    "label":"Image",
                                    "horizontalAlign":"center",
                                    "scaleMode":"fit_inside",
                                    "verticalAlign":"middle",
                                    "factorWidth":1.071877180739707,
                                    "libraryData":{"type":"round",
                                    "name":"blue",
                                    "family":"photos",
                                    "element":"IHotspotOverlayBitmapImage"},
                                    "width":33.3333,
                                    "distance":100,
                                    "factorHeight":1.071877180739707,
                                    "pitch":(618.24-self.connect_info[i][j][1])*90/618.24,
                                    "hfov":7.616601683506721,
                                    "yaw":(self.connect_info[i][j][2]-309.12)*180/309.12,#-6.9186093422888835,
                                    "height":30,
                                    "path":"hotspots/Hotspot_7E39A010_7A6C_4A10_41CC_55298DA3B325.png"}],
                                    "id":f"overlay_D{count}_{j}",
                                    "hasChanges":True,
                                    "maps":[]},
                                    {"rotationY":0,
                                    "class":"PopupPanoramaOverlayEditable",
                                    "hideEasing":"cubic_out",
                                    "showEasing":"cubic_in",
                                    "popupMaxWidth":"95%",
                                    "id":f"popup_D{count}_{j}",
                                    "rotationZ":0,
                                    "hasChanges":True,
                                    "popupMaxHeight":"95%",
                                    "showDuration":500,
                                    "hideDuration":500,
                                    "rotationX":0,
                                    "popupDistance":100,
                                    "path":os.path.basename(self.connect_info[i][j][0])}])
            count += 1
    def _get_areas_url(self):
        for i in range(self.number_panorama):
            self.areas_url.append([])
        count =0
        for i in self.number_url.keys():
            for j in range(self.number_url[i]):
                yaw = 10*j
                self.areas_url[count].append({"excludeClickGoMode":False, 
                                    "areas":[f"this.HotspotPanoramaOverlayArea_E{count}_{j}"], 
                                    "rollOverDisplay":False, 
                                    "useHandCursor":True, 
                                    "items":[{"x":587.85, 
                                    "transparencyActive":True, 
                                    "factorWidth":4.996282527881041, 
                                    "path":"hotspots/Hotspot_7E37A509_7A6C_4BF0_41C4_43F9C1B24379.png", 
                                    "label":"Image", 
                                    "horizontalAlign":"center", 
                                    "scaleMode":"fit_inside", 
                                    "verticalAlign":"middle", 
                                    "y":152.4, 
                                    "libraryData":{"type":"round", 
                                    "name":"blue", 
                                    "family":"link", 
                                    "element":"IHotspotOverlayBitmapImage"}, 
                                    "width":30, 
                                    "distance":50, 
                                    "factorHeight":4.996282527881041, 
                                    "pitch":33.99256505576208, 
                                    "hfov":8.321923226137582, 
                                    "yaw":21.697026022304847, 
                                    "height":30, 
                                    "class":"HotspotPanoramaOverlayBitmapImage"}], 
                                    "id":f"overlay_E{count}_{j}", 
                                    "hasChanges":True, 
                                    "class":"HotspotPanoramaOverlayEditable", 
                                    "maps":[]})
            count += 1
    def _get_behaviours_hotspot(self):
        for i in range(self.number_panorama):
            self.behaviours_hotspot.append([])

        count = 0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):

                connect_hotspot_panorama_id = self.remember_name_id[f"{self.connect_hotspot[i][j][0]}"] ##名前とidの辞書からパノラマのid取得
                self.behaviours_hotspot[count].append({"class":"HotspotPanoramaOverlayArea",
                            "id":f"HotspotPanoramaOverlayArea_C{count}_{j}",
                            "behaviours":[{"media":f"this.{connect_hotspot_panorama_id}",    ###パノラマのid反映
                            "class":"PanoramaBehaviour",
                            "event":"click",
                            "startPointView":{"type":"smartPoint",
                            "class":"StartPointView"},
                            "sentences":[],
                            "inComponent":"this.MainViewer",
                            "action":"openPanorama",
                            "where":"inViewer"}]})
            count +=1

    def _get_behaviours_info(self):
        for i in range(self.number_panorama):
            self.behaviours_info.append([])

        count = 0 #何番目のkeyか
        for i in self.number_info.keys():
            for j in range(self.number_info[i]):# jは何番目のvalueか
                connect_info_panorama_id = self.remember_name_id[i] ##名前とidの辞書からパノラマのid取得
                self.behaviours_info[count].append([{"id":f"HotspotPanoramaOverlayArea_D{count}_{j}",
                                        "class":"HotspotPanoramaOverlayArea",
                                        "behaviours":[{"autoCloseIfNotInteraction":False,
                                        "overlay":f"this.popup_D{count}_{j}",
                                        "class":"PopupPanoramaOverlayBehaviour",
                                        "event":"click",
                                        "sentences":[],
                                        "stopBackgroundAudio":False,
                                        "overlayerCallee":f"this.{connect_info_panorama_id}",
                                        "closeButton":f"this.CloseButton_D{count}_{j}",
                                        "action":"openPopupPanoramaOverlay",
                                        "milliseconds":10000}]},
                                        {"shadowSpread":1,
                                        "name":"CloseButton4187",
                                        "rollOverIconColor":6710886,
                                        "toolTipShadowColor":3355443,
                                        "toolTipHorizontalAlign":"center",
                                        "toolTipFontStyle":"normal",
                                        "toolTipTextShadowAngle":0,
                                        "paddingBottom":5,
                                        "id":f"CloseButton_D15309A1_D{count}_{j}",
                                        "toolTipBackgroundTransparent":False,
                                        "toolTipTextShadowBlurRadius":3,
                                        "paddingLeft":5,
                                        "shadowColor":0,
                                        "toolTipShadowOpacity":1,
                                        "toolTipShadowBlurRadius":3,
                                        "propagateClick":False,
                                        "toolTipShadowDistance":0,
                                        "backgroundOpacity":0.3,
                                        "toolTipBorderSize":1,
                                        "gap":5,
                                        "verticalAlign":"middle",
                                        "toolTipFontWeight":"normal",
                                        "paddingRight":5,
                                        "iconWidth":20,
                                        "arrangement":"horizontal",
                                        "toolTipFontSize":"1.11vmin",
                                        "iconLineWidth":5,
                                        "shadowBlurRadius":6,
                                        "horizontalAlign":"center",
                                        "toolTipPaddingTop":4,
                                        "borderColor":0,
                                        "borderSize":0,
                                        "toolTipShadowSpread":0,
                                        "iconHeight":20,
                                        "fontFamily":"Arial",
                                        "toolTipBorderColor":7763574,
                                        "pressedIconColor":8947848,
                                        "toolTipPaddingLeft":6,
                                        "textDecoration":"none",
                                        "backgroundColor":[14540253,15658734,16777215],
                                        "toolTipShadowAngle":45,
                                        "class":"CloseButton",
                                        "toolTipOpacity":1,
                                        "fontSize":"1.29vmin",
                                        "asHotspotVideo":False,
                                        "mode":"push",
                                        "toolTipBorderRadius":3,
                                        "toolTipTextShadowDistance":0,
                                        "minHeight":0,
                                        "backgroundColorAlphas":[1,1,1],
                                        "minWidth":0,
                                        "toolTipPaddingBottom":4,
                                        "borderRadius":0,
                                        "shadowDistance":3,
                                        "fontStyle":"normal",
                                        "shadow":False,
                                        "iconColor":0,
                                        "toolTipTextShadowOpacity":0,
                                        "backgroundColorDirection":"vertical",
                                        "fontColor":16777215,
                                        "backgroundColorRatios":[0,25,255],
                                        "toolTipDisplayTime":600,
                                        "visible":True,
                                        "toolTipPaddingRight":6,
                                        "toolTipFontFamily":"Arial",
                                        "paddingTop":5,
                                        "toolTipFontColor":6316128,
                                        "cursor":"hand",
                                        "toolTipTextShadowSpread":0,
                                        "fontWeight":"normal",
                                        "toolTipTextShadowColor":0,
                                        "toolTipBackgroundColor":16185078}])
            count +=1

    def _get_behaviours_url(self):
        for i in range(self.number_panorama):
            self.behaviours_url.append([])
        count = 0 #何番目のkeyか
        for i in self.number_url.keys():
            for j in range(self.number_url[i]):# jは何番目のvalueか
                connect_url_panorama_id = self.remember_name_id[i] ##名前とidの辞書からパノラマのid取得
                self.behaviours_url[count].append([{"id":f"HotspotPanoramaOverlayArea_E{count}_{j}",
                                    "class":"HotspotPanoramaOverlayArea", 
                                    "behaviours":[f"this.LinkBehaviour_E{count}_{j}"]},
                                    {"event":"click", 
                                    "sentences":[], 
                                    "method":"_blank", 
                                    "id":f"LinkBehaviour_E{count}_{j}", 
                                    "action":"openURL", 
                                    "class":"LinkBehaviour"}])

            count +=1


    def remember_context_panorama(self):
        self.remember_context = {}
        json_definition = self.json_load["player"]["definitions"]
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    self.remember_context[json_definition[i]["paths"][0].split(".")[0].split("/")[-1]]=json_definition[i]

    def remember_position_panorama(self):
        self.remember_number = {}
        json_definition = self.json_load["player"]["definitions"]
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    self.remember_number[os.path.basename(json_definition[i]["paths"][0]).split(".")[0]]=i
    
    def remember_name_and_id_panorama(self):
        self.remember_path = [] # self.remember_pathにパノラマのローカルでのpathが格納される
        self.remember_id = [] # self.remember_idにパノラマに対応したidが格納される
        self.remember_filename = [] # self.remember_filenameに画像名の.JPGなどを抜いた名前が格納される
        self.remember_name_id = {}
        for i in self.remember_context:
            self.remember_path.append(self.remember_context[i]["paths"][0])
            self.remember_id.append(self.remember_context[i]['id'])

        for i in range(len(self.remember_path)):
            self.remember_filename.append(os.path.basename(self.remember_path[i]).split(".")[0])
        
        count = 0
        
        for v in self.remember_filename:
            self.remember_name_id[f"{v}"] = self.remember_id[count]
            count += 1
    
    def remember_panorama_info(self): # script.jsのplayer->definitionsの中の"hfovMin"というキーを持つvalueがパノラマに関する情報
        self.remember_context_panorama() # {中身に対応する画像名:"hfovMin"というキーのvalueの中身,,,}がself.remember_contextに格納されてイル
        self.remember_position_panorama() # {中身に対応する画像名:hfovMin"というキーがdefinitionの何番目にあったか,,,}をself.remember_numberに格納
        self.remember_name_and_id_panorama() # self.remember_name_idに{パノラマ画像の名前: パノラマに対応したid} という辞書が格納される


    def insert_overlays(self):
        # overlayをそれぞれに追加
        for nameIm in self.remember_number.keys():
            self.remember_context[nameIm].update(self.overlays[nameIm])
            

        # json_loadにoverlay追加したのを入れる
        count = 0
        for nameIm in self.remember_number.keys():
            self.json_load['player']['definitions'][self.remember_number[nameIm]] = self.remember_context[nameIm]
            count += 1
    
    def insert_areas_hotspot(self):
        count =0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):
                self.json_load["player"]["definitions"].append(self.areas_hotspot[count][j])
            count+=1
    
    def insert_areas_info(self):
        count =0
        for i in self.number_info.keys():
            if self.number_info[i] == 0 :
                pass
            else :
                for j in range(self.number_info[i]):
                    for k in range(2):
                        self.json_load["player"]["definitions"].append(self.areas_info[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1
    
    def insert_areas_url(self):
        count =0
        for i in self.number_url.keys():
            if self.number_url[i] == 0 :
                pass
            else :
                for j in range(self.number_url[i]):
                    self.json_load["player"]["definitions"].append(self.areas_url[count][j])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1

    def insert_behaviours_hotspot(self):
        count =0
        for i in self.number_hotspot.keys():
            for j in range(self.number_hotspot[i]):
                self.json_load["player"]["definitions"].append(self.behaviours_hotspot[count][j])
            count +=1
    
    def insert_behaviours_info(self):
        count =0
        for i in self.number_info.keys():
            if self.number_info[i] == 0:
                pass
            else :
                for j in range(self.number_info[i]):
                    for k in range(2):
                        self.json_load["player"]["definitions"].append(self.behaviours_info[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1

    def insert_behaviours_url(self):
        count =0
        for i in self.number_url.keys():
            if self.number_url[i] == 0:
                pass
            else :
                for j in range(self.number_url[i]):
                    for k in range(2):
                        self.json_load["player"]["definitions"].append(self.behaviours_url[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1

    def insert_behaviours_url_two(self):
        count =0
        for i in self.number_url.keys():
            if self.number_url[i] == 0:
                pass
            else :
                for j in range(self.number_url[i]):
                    add_dict = {f"LinkBehaviour_E{count}_{j}.source":{"value":self.connect_url[i][j][0],"class":"LocaleValue"}}
                    self.json_load["locales"][0]["data"].update(add_dict)  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1


    # 編集したscript.jsを保存
    def save_to_json(self,save_path):
        with open(save_path, mode='wt', encoding='utf-8') as file:
            json.dump(self.json_load, file, ensure_ascii=False, indent=2)

    #　開いているjsonファイルを閉じる
    def file_close (self):
        self.json_open.close()
        self.db_open.close()


def main():
    AJD = Add_Json_Data("script.js", "data_base.js")
    AJD.insert_overlays()
    AJD.insert_areas_hotspot()
    AJD.insert_areas_info()
    AJD.insert_areas_url()
    AJD.insert_behaviours_hotspot()
    AJD.insert_behaviours_info()
    AJD.insert_behaviours_url()
    AJD.insert_behaviours_url_two()
    AJD.save_to_json("script.js")
    AJD.file_close()
    


if __name__ == "__main__":
    main()

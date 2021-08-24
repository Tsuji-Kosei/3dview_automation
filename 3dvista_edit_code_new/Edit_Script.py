import json
import os
import math
import time
from os.path import abspath, join, split


class Add_Json_Data():
    def __init__(self, script, db,remember_number, remember_context, hotspot, info, url, script_open, db_open):
        self.script_open = script_open
        self.db_open = db_open
        self.script = script
        self.db = db
        self.hotspot = hotspot
        self.info = info
        self.url = url
        self.remember_number = remember_number
        self.remember_context = remember_context

    def insert_hotspot(self):
        # overlayをそれぞれに追加
        for nameIm in self.hotspot.overlays.keys():
        	self.remember_context[nameIm].update(self.hotspot.overlays[nameIm])
        # scriptにoverlay追加したのを入れる
        count = 0
        for nameIm in self.hotspot.overlays.keys():
            self.script['player']['definitions'][self.remember_number[nameIm]] = self.remember_context[nameIm]
            count += 1

        # add areas
        count =0
        for nameIm in self.hotspot.number.keys():
            for j in range(self.hotspot.number[nameIm]):
                self.script["player"]["definitions"].append(self.hotspot.areas[count][j])
            count+=1
        
        # add behaviours
        count =0
        for nameIm in self.hotspot.number.keys():
            for j in range(self.hotspot.number[nameIm]):
                self.script["player"]["definitions"].append(self.hotspot.behaviours[count][j])
            count +=1

    def insert_info(self):

        # overlayをそれぞれに追加
        # print(self.remember_context)
        # print(self.info.overlays)
        for nameIm in self.info.overlays.keys():
            self.remember_context[nameIm]["overlays"] += self.info.overlays[nameIm]["overlays"]
        # scriptにoverlay追加したのを入れる #更新（最後のだけでいい）
        count = 0
        for nameIm in self.remember_number.keys():
            self.script['player']['definitions'][self.remember_number[nameIm]] = self.remember_context[nameIm]
            count += 1

        # add areas
        count =0
        for i in self.info.number.keys():
            if self.info.number[i] == 0 :
                pass
            else :
                for j in range(self.info.number[i]):
                    for k in range(2):
                        self.script["player"]["definitions"].append(self.info.areas[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1
        
        # add behaviour
        count =0
        for i in self.info.number.keys():
            if self.info.number[i] == 0:
                pass
            else :
                for j in range(self.info.number[i]):
                    for k in range(2):
                        self.script["player"]["definitions"].append(self.info.behaviours[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1
    
    def insert_url(self):
         # overlayをそれぞれに追加
        for nameIm in self.url.overlays.keys():
            self.remember_context[nameIm]["overlays"] += self.url.overlays[nameIm]["overlays"]
        # scriptにoverlay追加したのを入れる
        count = 0
        for nameIm in self.remember_number.keys():
            self.script['player']['definitions'][self.remember_number[nameIm]] = self.remember_context[nameIm]
            count += 1

        # add areas
        count =0
        for i in self.url.number.keys():
            if self.url.number[i] == 0 :
                pass
            else :
                for j in range(self.url.number[i]):
                    self.script["player"]["definitions"].append(self.url.areas[count][j])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1
        # add behaviour
        count =0
        for i in self.url.number.keys():
            if self.url.number[i] == 0:
                pass
            else :
                for j in range(self.url.number[i]):
                    for k in range(2):
                        self.script["player"]["definitions"].append(self.url.behaviours[count][j][k])  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1

        count =0
        for i in self.url.number.keys():
            if self.url.number[i] == 0:
                pass
            else :
                for j in range(self.url.number[i]):
                    add_dict = {f"LinkBehaviour_E{count}_{j}.source":{"value":self.url.connect[i][j][0],"class":"LocaleValue"}}
                    self.script["locales"][0]["data"].update(add_dict)  # countは何番目のkey　jは何番目のvalue kはvalueが要素数２のリストなので取り出している
            count+=1


    # 編集したscript.jsを保存
    def save_to_json(self,save_path):
        with open(save_path, mode='wt', encoding='utf-8') as file:
            json.dump(self.script, file, ensure_ascii=False, indent=2)

    #　開いているjsonファイルを閉じる
    def file_close (self):
        self.script_open.close()
        self.db_open.close()

class Prepare:
    def __init__ (self,script_path, db_path):
        self.script_path = script_path
        self.db_path = db_path
        self.script_open = open(self.script_path,'r', encoding='cp932', errors='ignore')
        self.db_open = open(self.db_path,'r')
        self.script = json.load(self.script_open) #3Dvistaのプロジェクトファイルの中のscript.js
        self.db = json.load(self.db_open) #detabase.js
        self._get_number_panorama()
        self.remember_panorama_info() # script.jsの中のパノラマに関する情報をクラス変数に格納(詳しくはこの関数の先に書いています)
    
    def _get_number_panorama(self):
        self.number_panorama = 0      #登録されている写真の枚数

        json_definition = self.script["player"]["definitions"]
        count = 0
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    count+=1
        self.number_panorama = count
        # print(self.number_panorama)
    def remember_context_panorama(self):
        self.remember_context = {}
        json_definition = self.script["player"]["definitions"]
        for i in range(len(json_definition)):
            for v in json_definition[i].keys():
                if(v=='hfovMin'):
                    self.remember_context[json_definition[i]["paths"][0].split(".")[0].split("/")[-1]]=json_definition[i]

    def remember_position_panorama(self):
        self.remember_number = {}
        json_definition = self.script["player"]["definitions"]
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

class Hotspot:
    def __init__(self, db, number_panorama, remember_name_id):
        self.db = db
        self.number_panorama  = number_panorama
        self.remember_name_id = remember_name_id

        self._get_connect()
        self._get_number()
        self._get_overlays()
        self._get_areas()
        self._get_behaviours()

    def _get_connect(self):
        self.connect= {}
        
        for i in self.db.keys():
            pre_connect = []  
            for j in range(len(self.db[i]["hotspot"])):
                angle = self.db[i]["hotspot"][j][1]
                pre_connect.append([self.db[i]["hotspot"][j][0],700+700*angle/math.pi, angle*180/math.pi])  ##connectに名前,x, yでappendしたい
            self.connect[i]=pre_connect

    def _get_number(self):
        self.number = {}

        for i in self.connect.keys():
            self.number[i]=len(self.connect[i])
    
    def _get_overlays(self): # 辞書の上から順に命名していく
        self.overlays = {}

        count = 0
        for i in self.number.keys():
            for j in range(self.number[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_C{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_C{count}_{j}")
            count +=1

    def _get_areas(self):
        self.areas = []
        # print(self.number_panorama)
        for i in range(self.number_panorama):
            self.areas.append([])

        count =0
        # print(self.connect)
        # print(self.number)
        for i in self.number.keys():
            for j in range(self.number[i]):
            	# print(i)
            	# print(j)

            	self.areas[count].append({"areas":[f"this.HotspotPanoramaOverlayArea_C{count}_{j}"],
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
                        "yaw":self.connect[i][j][2],
                        "pauseEvent":"none",
                        "x":708+self.connect[i][j][1]*math.sin(self.connect[i][j][2]),
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
    
    def _get_behaviours(self):
        self.behaviours = []

        for i in range(self.number_panorama):
            self.behaviours.append([])

        count = 0
        for i in self.number.keys():
            for j in range(self.number[i]):

                connect_hotspot_panorama_id = self.remember_name_id[f"{self.connect[i][j][0]}"] ##名前とidの辞書からパノラマのid取得
                self.behaviours[count].append({"class":"HotspotPanoramaOverlayArea",
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

class Info:
    def __init__(self, db, number_panorama, remember_name_id):
        self.db = db
        self.number_panorama  = number_panorama
        self.remember_name_id = remember_name_id

        self._get_connect()
        self._get_number()
        self._get_overlays()
        self._get_areas()
        self._get_behaviours()
    
    def _get_connect(self):
        self.connect ={}
        
        for i in self.db.keys():
            pre_connect = []
            for j in range(len(self.db[i]["info"])):
                pre_connect.append([self.db[i]["info"][j][0],self.db[i]["info"][j][1],self.db[i]["info"][j][2]])  ##connect_hotspotに名前,x, yでappendしたい
            self.connect[i]=pre_connect
    
    def _get_number(self):
        self.number = {}

        for i in self.connect.keys():
            self.number[i]=len(self.connect[i])
    
    def _get_overlays(self): # 辞書の上から順に命名していく
        
        self.overlays = {}

        count = 0
        for i in self.number.keys():
            for j in range(self.number[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_D{count}_{j}",f"this.popup_D{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_D{count}_{j}")
                    self.overlays[i]["overlays"].append(f"this.popup_D{count}_{j}")
            count +=1
    
    def _get_areas(self):
        self.areas = []

        for i in range(self.number_panorama):
            self.areas.append([])

        count =0
        for i in self.number.keys():
            for j in range(self.number[i]):
                yaw = 10*j
                self.areas[count].append([{"excludeClickGoMode":False,
                                    "class":"HotspotPanoramaOverlayEditable",
                                    "areas":[f"this.HotspotPanoramaOverlayArea_D{count}_{j}"],
                                    "rollOverDisplay":False,
                                    "useHandCursor":True,
                                    "items":[{"x":self.connect[i][j][2]*1416/618.24,
                                    "class":"HotspotPanoramaOverlayBitmapImage",
                                    "transparencyActive":True,
                                    "y":self.connect[i][j][1]*700/1236.48,
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
                                    "pitch":(618.24-self.connect[i][j][1])*90/618.24,
                                    "hfov":7.616601683506721,
                                    "yaw":(self.connect[i][j][2]-309.12)*180/309.12,#-6.9186093422888835,
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
                                    "path":os.path.basename(self.connect[i][j][0])}])
            count += 1
    
    def _get_behaviours(self):
        self.behaviours = []

        for i in range(self.number_panorama):
            self.behaviours.append([])

        count = 0 #何番目のkeyか
        for i in self.number.keys():
            for j in range(self.number[i]):# jは何番目のvalueか
                connect_info_panorama_id = self.remember_name_id[i] ##名前とidの辞書からパノラマのid取得
                self.behaviours[count].append([{"id":f"HotspotPanoramaOverlayArea_D{count}_{j}",
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

class URL:
    def __init__(self, db, number_panorama, remember_name_id):
        self.db = db
        self.number_panorama  = number_panorama
        self.remember_name_id = remember_name_id

        self._get_connect()
        self._get_number()
        self._get_overlays()
        self._get_areas()
        self._get_behaviours()
    
    def _get_connect(self):
        self.connect = {}
        
        for i in self.db.keys():
            pre_connect = []
            for j in range(len(self.db[i]["URL"])):
                pre_connect.append([self.db[i]["URL"][j][0],self.db[i]["URL"][j][1],self.db[i]["URL"][j][2]])  ##connect_hotspotに名前,x, yでappendしたい
            self.connect[i]=pre_connect
    
    def _get_number(self):
        self.number = {}

        for i in self.connect.keys():
            self.number[i]=len(self.connect[i])
    
    
    def _get_overlays(self): # 辞書の上から順に命名していく
        self.overlays = {}

        count = 0
        for i in self.number.keys():
            for j in range(self.number[i]):
                if not i in self.overlays:
                    self.overlays[i] = {"overlays":[f"this.overlay_E{count}_{j}"]}
                else:
                    self.overlays[i]["overlays"].append(f"this.overlay_E{count}_{j}")

            count +=1

    def _get_areas(self):
        self.areas = []

        for i in range(self.number_panorama):
            self.areas.append([])
        count =0
        for i in self.number.keys():
            for j in range(self.number[i]):
                yaw = 10*j
                self.areas[count].append({"excludeClickGoMode":False, 
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
                                    "pitch":(618.24-self.connect[i][j][1])*90/618.24, 
                                    "hfov":8.321923226137582, 
                                    "yaw":(self.connect[i][j][2]-309.12)*180/309.12, 
                                    "height":30, 
                                    "class":"HotspotPanoramaOverlayBitmapImage"}], 
                                    "id":f"overlay_E{count}_{j}", 
                                    "hasChanges":True, 
                                    "class":"HotspotPanoramaOverlayEditable", 
                                    "maps":[]})
            count += 1

    def _get_behaviours(self):
        self.behaviours =[]

        for i in range(self.number_panorama):
            self.behaviours.append([])
        count = 0 #何番目のkeyか
        for i in self.number.keys():
            for j in range(self.number[i]):# jは何番目のvalueか
                connect_url_panorama_id = self.remember_name_id[i] ##名前とidの辞書からパノラマのid取得
                self.behaviours[count].append([{"id":f"HotspotPanoramaOverlayArea_E{count}_{j}",
                                    "class":"HotspotPanoramaOverlayArea", 
                                    "behaviours":[f"this.LinkBehaviour_E{count}_{j}"]},
                                    {"event":"click", 
                                    "sentences":[], 
                                    "method":"_blank", 
                                    "id":f"LinkBehaviour_E{count}_{j}", 
                                    "action":"openURL", 
                                    "class":"LinkBehaviour"}])

            count +=1
    


def main():
    prepare = Prepare(script_path="script.js", db_path="data_base.js")
    script = prepare.script
    db = prepare.db
    number_panorama = prepare.number_panorama
    remember_number = prepare.remember_number
    remember_context = prepare.remember_context
    remember_name_id = prepare.remember_name_id
    hotspot = Hotspot(db, number_panorama, remember_name_id)
    info = Info(db, number_panorama, remember_name_id)
    url = URL(db, number_panorama, remember_name_id)
    AJD = Add_Json_Data(script, db,remember_number, remember_context, hotspot, info, url, prepare.script_open, prepare.db_open)
    AJD.insert_hotspot()
    AJD.insert_info()
    AJD.insert_url()
    AJD.save_to_json("script.js")
    AJD.file_close()
    


if __name__ == "__main__":
    main()

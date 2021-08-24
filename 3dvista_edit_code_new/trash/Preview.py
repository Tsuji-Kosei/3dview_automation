import pyautogui as pgui
import time
import tkinter
import os
import threading
import multiprocessing
import subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
CWD = os.getcwd()
CWD = CWD.split(':')
Images = CWD[1] + "\\Images"
Destination = CWD[1] + "\\project"
Name = args.name



def wait_appear(Image, conf, timeout):
	t = 0.0
	while pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
		time.sleep(0.5)
		t = t + 0.5
		if t == timeout:
			pgui.alert(text="画像が認識できませんでした。",title="エラー",button="終了")
			os.system('taskkill /f /im "3DVista Virtual Tour.exe" >nul')
			os.system('taskkill /f /im "python.exe" >nul')
	time.sleep(0.1)
			
def wait_disappear(Image, conf):
	while not pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
		time.sleep(0.5)
	time.sleep(0.1)
		


def Preview():

	#パノラマ編集
	subprocess.call("py main.py --copy " + Name)
	
	#プレビュー
	file_button = pgui.locateOnScreen(".\\screenshots\\File.jpg", grayscale=True, confidence=0.8)
	pgui.click(file_button)
	time.sleep(0.2)
	open_vtp_button = pgui.locateOnScreen(".\\screenshots\\Load.jpg", grayscale=True, confidence=0.8)
	pgui.click(open_vtp_button)
	wait_appear("Open_vtp", 0.8, 5)
	pgui.write(Destination + "\\" + Name + ".vtp")
	time.sleep(0.1)
	pgui.press("enter")
	time.sleep(1)
	wait_disappear("Loading_Project", 0.8)
	time.sleep(1)
	preview_button = pgui.locateOnScreen(".\\screenshots\\Preview.jpg", grayscale=True, confidence=0.8)
	pgui.click(preview_button)
	time.sleep(10)



#ポップアップの作成
displaysize = pgui.size()
psize_x = int(displaysize[0]/4)
psize_y = int(displaysize[1]/10)
loc_x = int(displaysize[0]/2 - psize_x/2)
loc_y = int(displaysize[1]/10)
root = tkinter.Tk()
root.attributes("-topmost", True)
root.title("動作中")
window = str(psize_x) + "x" + str(psize_y) + "+" + str(loc_x) + "+" + str(loc_y)
root.geometry(window)
message = "PCを操作しないでください。"
caution = tkinter.Label(text=message, font=("normal", "12", "normal"))
caution.pack(anchor="center", expand=1)



def popup_open():
	root.mainloop()



def main():
	t1 = multiprocessing.Process(target=popup_open)
	t2 = threading.Thread(target=Preview)
	t1.start()
	t2.start()
	t2.join()
	pgui.click(x=loc_x+psize_x-5, y=loc_y+5)



if __name__ == "__main__":
	main()
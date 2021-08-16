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
	print(".\\screenshots\\" + Image + ".jpg")
	while pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
		time.sleep(0.5)
		t = t + 0.5
		print(t)
		if t == timeout:
			pgui.alert(text="画像が認識できませんでした。",title="エラー",button="終了")
			os.system('taskkill /f /im "3DVista Virtual Tour.exe" >nul')
			os.system('taskkill /f /im "python.exe" >nul')
	time.sleep(0.1)
			
def wait_disappear(Image, conf):
	while not pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
		time.sleep(0.5)
	time.sleep(0.1)
		


def New_Project():

	#起動
	subprocess.Popen("\\Program Files\\3DVista\\3DVista Virtual Tour\\3DVista Virtual Tour.exe")
	wait_appear("No", 0.8, 20)
	No = pgui.locateOnScreen(".\\screenshots\\No.jpg", grayscale=True, confidence=0.8)
	pgui.click(No)

	wait_appear("New", 0.8, 20)
	New = pgui.locateOnScreen(".\\screenshots\\New.jpg", grayscale=True, confidence=0.8)
	pgui.click(New)
	#画像選択まで
	pgui.press(["tab", "tab", "enter"], interval=0.1)
	time.sleep(1.5)
	select_button = pgui.locateOnScreen(".\\screenshots\\Select.jpg", grayscale=True, confidence=0.8)
	pgui.click(select_button)
	time.sleep(1.5)
	pgui.press(["tab", "tab", "enter"], interval=0.1)
	time.sleep(1.5)
	pgui.press(["tab", "tab", "enter"], interval=0.1)

	#画像選択
	wait_appear("Open", 0.8, 8)
	pgui.write(Images)
	time.sleep(0.1)
	pgui.press("enter")
	time.sleep(1)
	pgui.hotkey("shiftleft", "tab")
	time.sleep(0.1)
	pgui.hotkey("ctrlleft", "a")
	time.sleep(0.1)
	pgui.press("enter")
	time.sleep(0.5)

	#画像読み込み待機
	wait_disappear("Loading", 0.8)
	time.sleep(0.1)
	if not pgui.locateOnScreen(".\\screenshots\\Apply.jpg", grayscale=True, confidence=0.8) is None:
		pgui.press(["tab", "space", "tab", "enter"], interval=0.1)
		time.sleep(0.5)
		wait_disappear("Loading", 0.8)

	#保存
	time.sleep(0.1)
	pgui.press("tab")
	time.sleep(0.1)
	pgui.hotkey("ctrlleft", "shiftleft", "s")
	wait_appear("Save", 0.8, 8)
	pgui.write(Destination + "\\" + Name + ".vtp")
	time.sleep(0.2)
	pgui.press("enter")
	time.sleep(0.5)
	wait_disappear("Saving", 0.8)
	time.sleep(0.5)

	



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
	os.system('taskkill /f /im "3DVista Virtual Tour.exe" 2>nul')
	t1 = multiprocessing.Process(target=popup_open)
	t2 = threading.Thread(target=New_Project)
	t1.start()
	t2.start()
	t2.join()
	pgui.click(x=loc_x+psize_x-5, y=loc_y+5)



if __name__ == "__main__":
	main()
import pyautogui as pgui
import time
import tkinter
import os
import threading
import multiprocessing
import subprocess

import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("name")
# args = parser.parse_args()
# CWD = os.getcwd()
# CWD = CWD.split(':')
# Images = CWD[1] + "\\Images"
# Destination = CWD[1] + "\\project"
# Name = args.name


class RPA:
	def __init__ (self, args, mode="create_vtp"):
		self.args = args
		self.Name = self.args.name
		CWD = os.getcwd()
		CWD = CWD.split(':')
		self.Images = CWD[1] + "\\Images"
		self.Destination = CWD[1] + "\\project"
		self.mode = mode
		self.t2_finish_flug = False

		#popup
		displaysize = pgui.size()
		self.psize_x = int(displaysize[0]/4)
		self.psize_y = int(displaysize[1]/10)
		self.loc_x = int(displaysize[0]/2 - self.psize_x/2)
		self.loc_y = int(displaysize[1]/10)

	def wait_appear(self,Image, conf, timeout):
		t = 0.0
		# print(".\\screenshots\\" + Image + ".jpg")
		while pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
			time.sleep(0.5)
			t = t + 0.5
			# print(t)
			if t == timeout:
				pgui.alert(text="画像が認識できませんでした。",title="エラー",button="終了")
				os.system('taskkill /f /im "3DVista Virtual Tour.exe" >nul')
				os.system('taskkill /f /im "python.exe" >nul')
		time.sleep(0.1)
				
	def wait_disappear(self,Image, conf):
		while not pgui.locateOnScreen(".\\screenshots\\" + Image + ".jpg", grayscale=True, confidence=conf) is None:
			time.sleep(0.5)
		time.sleep(0.1)
			


	def New_Project(self):

		#起動
		subprocess.Popen("\\Program Files\\3DVista\\3DVista Virtual Tour\\3DVista Virtual Tour.exe")
		self.wait_appear("No", 0.8, 20)
		No = pgui.locateOnScreen(".\\screenshots\\No.jpg", grayscale=True, confidence=0.8)
		pgui.click(No)

		self.wait_appear("New", 0.8, 20)
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
		self.wait_appear("Open", 0.8, 8)
		pgui.write(self.Images)
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
		self.wait_disappear("Loading", 0.8)
		time.sleep(0.1)
		if not pgui.locateOnScreen(".\\screenshots\\Apply.jpg", grayscale=True, confidence=0.8) is None:
			pgui.press(["tab", "space", "tab", "enter"], interval=0.1)
			time.sleep(0.5)
			self.wait_disappear("Loading", 0.8)

		#保存
		print("FF")
		time.sleep(0.1)
		pgui.press("tab")
		time.sleep(0.1)
		pgui.hotkey("ctrlleft", "shiftleft", "s")
		self.wait_appear("Save", 0.8, 8)
		pgui.write(self.Destination + "\\" + self.Name + ".vtp")
		time.sleep(0.2)
		pgui.press("enter")
		time.sleep(0.5)
		self.wait_disappear("Saving", 0.8)
		time.sleep(0.5)

	def Preview(self):
		print("RR")

	#パノラマ編集
		# subprocess.call("py main.py --copy " + self.Name)
		print("TT")
		
		#プレビュー
		file_button = pgui.locateOnScreen(".\\screenshots\\File.jpg", grayscale=True, confidence=0.8)
		pgui.click(file_button)
		time.sleep(0.2)
		open_vtp_button = pgui.locateOnScreen(".\\screenshots\\Load.jpg", grayscale=True, confidence=0.8)
		pgui.click(open_vtp_button)
		self.wait_appear("Open_vtp", 0.8, 5)
		pgui.write(self.Destination + "\\" + self.Name + ".vtp")
		time.sleep(0.1)
		pgui.press("enter")
		time.sleep(1)
		self.wait_disappear("Loading_Project", 0.8)
		time.sleep(1)
		preview_button = pgui.locateOnScreen(".\\screenshots\\Preview.jpg", grayscale=True, confidence=0.8)
		pgui.click(preview_button)
		time.sleep(10)

	def popup_open(self):
		
		#ポップアップの作成
		self.root = tkinter.Tk()
		self.root.attributes("-topmost", True)
		self.root.title("動作中")
		window = str(self.psize_x) + "x" + str(self.psize_y) + "+" + str(self.loc_x) + "+" + str(self.loc_y)
		self.root.geometry(window)
		message = "PCを操作しないでください。"
		caution = tkinter.Label(text=message, font=("normal", "12", "normal"))
		caution.pack(anchor="center", expand=1)

		self.check_quit_t2process()
		self.root.mainloop()

	def check_quit_t2process(self):
		if not self.t2_finish_flug:
			self.root.after(10, self.check_quit_t2process)
		else:
			self.root.destroy()
			self.root.quit()



	def main(self):
		if self.mode == "create_vtp":
			os.system('taskkill /f /im "3DVista Virtual Tour.exe" 2>nul')
		t1 = multiprocessing.Process(target=self.popup_open)
		if self.mode == "create_vtp":
			t2 = threading.Thread(target=self.New_Project)
		else:
			t2 = threading.Thread(target=self.Preview)
		t1.start()
		t2.start()
		t2.join()
		self.t2_finish_flug = True
		print("t2stop")
		t1.join()
		print("popupstop")
		# pgui.click(x=self.loc_x+self.psize_x-5, y=self.loc_y+5)



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('name',type=str, help='.vtpを抜いたプロジェクトファイル名を入力する')
	args = parser.parse_args()

	CV = RPA(args)
	CV.main()
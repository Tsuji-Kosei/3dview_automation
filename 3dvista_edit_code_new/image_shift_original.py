import cv2
import numpy as np

def image_shift(image, direction):
	height, width = image.shape[:2]

	ratio = 1 - direction/360

	img_translation1 = image[0:height, 0:int(width*ratio)]
	img_translation2 = image[0:height, int(width*ratio):width]


	img_merge = cv2.hconcat([img_translation2, img_translation1])
	height, width = img_merge.shape[:2]
	# print(height, width)

	# cv2.imshow("Originalimage", image)
	# cv2.imshow('Translation1', img_translation1)
	# cv2.imshow('Translation2', img_translation1)
	# cv2.imshow('Merged', img_merge)
	# cv2.waitKey()
	# cv2.destroyAllWindows()
	return img_merge	


if __name__=="__main__":
	image = cv2.imread('C:\\Users\\root\\Desktop\\3dview_automation\\3dvista_edit_code_new\\Images\\1.JPG')
	height, width = image.shape[:2]

	img_merge = image_shift(image, 90)
	# img_merge2 = cv2.resize(img_merge,dsize=(int(width*5), int(height*5)))
	cv2.imshow("Originalimage", image)
	cv2.imshow('Merged', img_merge)
	cv2.imwrite("out_sample3.JPG", img_merge,[cv2.IMWRITE_JPEG_QUALITY, 100])
	cv2.waitKey()
	cv2.destroyAllWindows()

	#########画質悪い#########
### This program :
# 1.Opens a web browser
# 2.Reads the webapp data.
# 3.Sends commands to the webapp.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import pyscreenshot as ImageGrab

def nn(image):
	# This function represents the neural network
	# INPUT image array (120x120x3)
	# OUTPUT tuple (throttle, left, right)

	return (0.5,1.0,0.0)

def convert_image(image, size):
	### convert file from row major format
	#image[0] is top left
	#then it goes across the top row of pixels
	#final element in array is bottom right of image
	width=size[0]
	height=size[1]
	formatted_array=[]
	for y in range(height):
		formatted_array.append(image[width*y:width*(y+1)])
	return formatted_array


def connect(ip):
	#CONSTANTS
	throttle_limit = 0.3
	test_duration = 10
	image_size=(2,2)

	#establish a connection
	web_address="http://"+ip+":8887/drive"
	chromeOptions = Options()
	chromeOptions.add_argument("--kiosk")
	driver = webdriver.Chrome(chrome_options=chromeOptions)
	# driver = webdriver.Chrome()
	driver.get(web_address)

	img_window=driver.find_element_by_xpath("//img[@id='mpeg-image']")
	img_location=img_window.location
	img_size=img_window.size
	img_location["y"]+=40

	#set the format for the POST command
	commmand_format = '''$.post("{0}",'{1}')'''
	instructions = {"angle":0,"throttle":0,"drive_mode":"user","recording":False}
	try:
		for i in range(4):
			time.sleep(0.5)

			# part of the screen
			img=ImageGrab.grab(bbox=(
				img_location["x"],
				img_location["y"],
				img_location["x"]+img_size["width"],
				img_location["y"]+img_size["height"]
			)) # X1,Y1,X2,Y2

			img=img.resize(image_size)
			image=list(img.getdata())
			nn_image=convert_image(image,image_size)
			# img.save("capture/grab{0}.bmp".format(i))

			instructions=nn(nn_image)

			#construct the javascript command
			instructions["angle"]=angle
			instructions["throttle"]=throttle*throttle_limit
			full_command=commmand_format.format(web_address,json.dumps(instructions))
			# print(full_command)

			#execute javascript
			# driver.execute_script(full_command)
	finally:
		time.sleep(1)
		instructions["angle"]=0
		instructions["throttle"]=0
		full_command=commmand_format.format(web_address,json.dumps(instructions))
		# driver.execute_script(full_command)

connect("192.168.43.14")
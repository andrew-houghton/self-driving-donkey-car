### This program :
# 1. Opens a web browser
# 2. Reads the webapp data using screenshots.
# 3. Sends the screenshots to the neural network and gets instructions.
# 4. Sends commands to the webapp using javascript.

### Libraries
from selenium import webdriver #for changing web browser
from selenium.webdriver.chrome.options import Options #for opening chrome in the right mode
import time #for waiting for pages to load
import json #for sending the json data in post requests from the webapp
from PIL import Image #can't remember
import pyscreenshot as ImageGrab #grab screenshots
import numpy as np

def nn(data):
	### This function represents the neural network
	model_filename="3615.h5"
	# INPUT image numpy array (120x120x3)
	# OUTPUT tuple (throttle, left, right)

	print(data.shape)

	import SelfDrivingTraining
	from datetime import datetime
	finalModel = SelfDrivingTraining.buildModel()
	finalModel.load_weights(model_filename) #this needs to point to a valid model
	
	before=datetime.now()
	output = finalModel.predict(data)
	after=datetime.now()

	print("before\t{0}\tafter\t{1}".format(before,after))

	print(output)

	list_output=output.tolist()[0] #left, straight, right

	print("list_output\t{0}".format(list_output))

	return list_output

def nn2(data):
	### If the top half of the image is brighter than the bottom turn left.
	#this function is used to test that the image is being understood in the right way.
	if (len(data)==2 and len(data[0])==2):
		if sum(data[0][0])+sum(data[0][1])>sum(data[1][0])+sum(data[1][1]):
			return (1,1,0) #top half greater than bottom = left
		else:
			return (1,0,1) #bottom greater = right
	else:
		print("invalid image size")
		return (0.5,1.0,0.0) #placeholder

def convert_image(image, size):
	### Splits a list into a list of list representing rows.
	#image[0] is top left, then it goes across the top row of pixels, final element in array is bottom right of image
	formatted_array=[]
	for y in range(size[1]):
		formatted_array.append(image[size[0]*y:size[0]*(y+1)])
	return formatted_array

def connect(ip):
	#CONSTANTS
	throttle_limit = 0.3
	image_size=(120,120)
	web_address="http://"+ip+":8887/drive"
	loop_duration=10
	browser_header_height=40 #magic number. Represents the height of the top of the chrome browser

	#establish a browser connection to the webapp
	# driver = webdriver.Chrome()
	# driver.maximize_window()
	chromeOptions = Options()
	chromeOptions.add_argument("--kiosk")
	driver = webdriver.Chrome(chrome_options=chromeOptions) #driver is the webdriver which controls the browser
	driver.get(web_address)

	#find the location of the image within the window
	img_window=driver.find_element_by_xpath("//img[@id='mpeg-image']")
	img_location=img_window.location
	img_size=img_window.size
	img_location["y"]+=browser_header_height # this is a magic number which represents the height of the browser window header.

	#set the format for the POST command
	commmand_format = '''$.post("{0}",'{1}')''' #first POST argument is URL, second post arg is driving instructions
	instructions = {"angle":0,"throttle":0,"drive_mode":"user","recording":False}

	#wait for user input
	# input("Press Enter to start driving.")

	try: #using a try/finally block to make sure that the car is stopped when the script finishes.
		for i in range(loop_duration):
			# Take the screenshot
			screenshot=ImageGrab.grab(bbox=(
				img_location["x"],img_location["y"],
				img_location["x"]+img_size["width"],img_location["y"]+img_size["height"]
			)) # X1,Y1,X2,Y2

			# Save the image
			screenshot.save("capture/grab{0}.bmp".format(i))

			#resize the image to the desired size
			screenshot=screenshot.resize(image_size) #argument is (width,height)
			image_array=list(screenshot.getdata()) #convert the image to an array
			image_array=convert_image(image_array,image_size) #convert the array to a
			# now that convert_image has been run: red pixel at x 2 y 3 would be image_array[3][2][0]

			#send the image to the neural network to be processed
			nn_output=nn(np.asarray([image_array]))
			# nn_output=nn2(image)

			#construct the javascript command
			#angle control
			if nn_output[0]==1: #left
				instructions["angle"]=-1
			if nn_output[1]==1:
				instructions["angle"]=0
			if nn_output[2]==1: #right
				instructions["angle"]=1
			else:
				instructions["angle"]=0

			#throttle control
			if nn_output[1]==1:
				instructions["throttle"]=throttle_limit #throttle is limited to prevent car driving too fast to control
			else:
				instructions["throttle"]=0.8*throttle_limit #throttle is limited to prevent car driving too fast to control

			#construct the command to send to the webserver
			full_command=commmand_format.format(web_address,json.dumps(instructions))
			print(full_command)

			# run the javascript command from the browser window (will be immediately executed on the car)
			driver.execute_script(full_command)
	finally:
		# Try to stop the car
		instructions["angle"]=0
		instructions["throttle"]=0
		full_command=commmand_format.format(web_address,json.dumps(instructions))
		driver.execute_script(full_command)

#Ip address of raspberry pi
connect("192.168.43.14")

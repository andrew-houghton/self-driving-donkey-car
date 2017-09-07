### This program :
# 1.Opens a web browser
# 2.Reads the webapp data.
# 3.Sends commands to the webapp.

print("Importing libraries")
from selenium import webdriver
import time
import json
print("Finished importing")

# def nn(image):
# 	# This function represents the neural network
# 	# INPUT image array (3x150x150)
# 	# OUTPUT tuple (throttle, left, right)
#
# 	return (0.5,1.0,0.0)

def connect(ip):
	#CONSTANTS
	throttle_limit = 0.3
	test_duration = 10

	#establish a connection
	web_address="http://"+ip+":8887/drive"
	driver = webdriver.Chrome()
	driver.get(web_address)

	#set the format for the POST command
	commmand_format = '''$.post("{0}",'{1}')'''
	instructions = {"angle":0,"throttle":0,"drive_mode":"user","recording":False}
	try:
		for i in range(10):
			time.sleep(1)

			#swerving (instead of NNs)
			throttle=i%2
			if (i/2%4==0):
				angle=-1
			else:
				angle=1

			#construct the javascript command
			instructions["angle"]=angle
			instructions["throttle"]=throttle*throttle_limit
			full_command=commmand_format.format(web_address,json.dumps(instructions))
			print(full_command)

			#execute javascript
			driver.execute_script(full_command)
	finally:
		time.sleep(1)
		instructions["angle"]=0
		instructions["throttle"]=0
		full_command=commmand_format.format(web_address,json.dumps(instructions))
		driver.execute_script(full_command)

connect("192.168.43.14")
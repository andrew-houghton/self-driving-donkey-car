### This program :
# 1.Opens a web browser
# 2.Reads the webapp data.
# 3.Sends commands to the webapp.

print("Importing libraries")
from selenium import webdriver
import time
import urllib
print("Finished importing")

def nn(image):
	# This function represents the neural network
	# INPUT image array (3x150x150)
	# OUTPUT tuple (throttle, left, right)

	return (0.5,1.0,0.0)

def connect(ip):
	webaddr="http://"+ip+":8887/video"
	save_path="/home/andrew/Dropbox/Uni assignments/COMP3615/selfdriving/web_fetch/"
	driver = webdriver.Chrome()

	print(webaddr)

	driver.get(webaddr)
	driver.get_screenshot_as_file('/tmp/screen.png')
	print("saved screenshot")

	time.sleep(10)

connect("192.168.43.14")
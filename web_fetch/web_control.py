### This program :
# 1.Opens a web browser
# 2.Reads the webapp data.
# 3.Sends commands to the webapp.

print("Importing libraries")
from selenium import webdriver
print("Finished importing")

def nn(image):
	# This function represents the neural network
	# INPUT image array (3x150x150)
	# OUTPUT tuple (throttle, left, right)

	return (0.5,1.0,0.0)

def connect(ip):
	webaddr="http://"+ip+":8887"
	driver = webdriver.Chrome()

	print(webaddr)

	driver.get(webaddr)
	# img_window=driver.find_element_by_xpath("//img[@id='mpeg-image']")
	# img_src = img_window.get_attribute("src")
	# urllib.urlretrieve(src, "captcha.png")
	# print(img_src)

connect("192.168.43.14")
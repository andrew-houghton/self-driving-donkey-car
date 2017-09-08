ip="192.168.43.14"

from selenium import webdriver #for changing web browser

web_address="http://"+ip+":8887/drive"

driver = webdriver.Chrome()
driver.get(web_address)

commmand_format = '''$.post("{0}",'{1}')''' #first POST argument is URL, second post arg is driving instructions
instructions = {"angle":0,"throttle":0,"drive_mode":"user","recording":False}
full_command=commmand_format.format(web_address,json.dumps(instructions))

driver.execute_script(full_command)
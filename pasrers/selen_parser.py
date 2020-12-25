from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


speciality = 'БТС'
kafedra_code = 43    # Физика
test_name = 'Контрольная работа по механике'


driver = webdriver.Chrome()
driver.get("https://testirov.rusoil.net/startrehearsal")
input_spec = Select(driver.find_element_by_id('specy'))
input_spec.select_by_value(speciality)
input_kafedra = Select(driver.find_element_by_id('allkafedra'))
input_kafedra.select_by_value(str(kafedra_code))





time.sleep(5)
driver.close()

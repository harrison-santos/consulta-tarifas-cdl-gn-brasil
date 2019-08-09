from selenium import webdriver
from datetime import date
import sergas_screenshot
import bahiagas_screenshot
import algas_screenshot

today = str(date.today().strftime("%d-%m-%Y"))

options = webdriver.FirefoxOptions()
options.add_argument("--proxy-server='direct://'");
options.add_argument("--proxy-bypass-list=*");
options.headless = True
driver = webdriver.Firefox(executable_path=r'C:\Program Files\GeckoDriver\geckodriver.exe')

#sergas_screenshot.captura(driver, today)
#bahiagas_screenshot.captura(driver, today)
algas_screenshot.captura(driver, today)
driver.quit()




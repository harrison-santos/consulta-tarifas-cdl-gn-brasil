from selenium import webdriver
from datetime import date
import sergas_screenshot


today = str(date.today().strftime("%d-%m-%Y"))

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)


sergas_screenshot.captura(driver, today)
driver.quit()
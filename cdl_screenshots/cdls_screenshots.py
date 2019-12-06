from selenium import webdriver
from datetime import date
import sergas_screenshot
import algas_screenshot
import cegas_screenshot
import comgas_screenshot
import compagas_screenshot
import copergas_screenshot
import gasbrasiliano_screenshot
import gasmig_screenshot
import pbgas_screenshot
import potigas_screenshot



def captura():
    today = date.today().strftime("%d-%m-%Y")

    #Instancia Driver
    options = webdriver.FirefoxOptions()
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.headless = False
    driver = webdriver.Firefox(options=options)

    #REQUESTS FALTA: BAHIAGAS, GASMIG, SULGAS, scgas
    algas_screenshot.captura(driver, today)
    cegas_screenshot.captura(driver, today)
    comgas_screenshot.captura(driver, today)
    compagas_screenshot.captura(driver, today)
    copergas_screenshot.captura(driver, today)
    gasbrasiliano_screenshot.captura(driver, today)
    gasmig_screenshot.captura(driver, today)
    pbgas_screenshot.captura(driver, today)
    potigas_screenshot.captura(driver, today)
    sergas_screenshot.captura(driver, today)
    driver.quit()

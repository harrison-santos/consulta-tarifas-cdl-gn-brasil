from selenium import webdriver
from datetime import date

def captura():
    today = date.today().strftime("%d-%m-%Y")
    cdls= [{'name': 'bahiagas', 'url': 'http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp'},
           {'name': 'sergas', 'url':'https://www.sergipegas.com.br/cms/tarifas'}]
    #dir = r'C:\consulta-tarifas-cdl-gn-brasil\cdl_tarifas\cdl_tarifas\files\img\bahiagas_{}.png'.format(today)
    main_dir = r'C:\consulta-tarifas-cdl-gn-brasil\files\img\{}\{}.png'

    #Instancia Driver
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    ##

    #Requisicao

    for cdl in cdls:
        dir = main_dir.format(cdl['name'], cdl['name'])
        driver.get(cdl['url'])
        #driver.implicitly_wait(90)
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
        driver.find_element_by_tag_name('body').screenshot(dir)
        driver.implicitly_wait(300)
    driver.quit()


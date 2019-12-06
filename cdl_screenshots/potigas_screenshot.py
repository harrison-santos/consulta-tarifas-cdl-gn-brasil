import time

url = "https://www.potigas.com.br/sistema-tarifario"
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/potigas'

def captura(driver, data):
    driver.get(url)
    #driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    driver.find_element_by_id('internas').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
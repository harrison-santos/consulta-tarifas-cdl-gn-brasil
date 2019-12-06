import time

url = "http://cegas.com.br/tabela-de-tarifas-atual/"
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/cegas'

def captura(driver, data):
    driver.get(url)
    driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
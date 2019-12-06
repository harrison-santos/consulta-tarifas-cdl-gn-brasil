import time

url = "https://www.copergas.com.br/atendimento-ao-cliente/tarifas"
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/copergas'

def captura(driver, data):
    driver.get(url)
    driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
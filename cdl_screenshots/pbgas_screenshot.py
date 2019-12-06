import time

url = "http://www.pbgas.com.br/?page_id=1477'"
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/pbgas'

def captura(driver, data):
    driver.get(url)
    driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
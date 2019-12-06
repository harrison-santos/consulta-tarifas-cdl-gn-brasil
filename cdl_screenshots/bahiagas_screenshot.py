import time

url = 'http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp'
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/bahiagas'


def captura(driver, data):
    driver.get(url)
    driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
import time

url = 'http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp'
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/bahiagas'


def captura(driver, data):
    driver.get(url)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(main_dir + '/geral_{}.png'.format(data))
    time.sleep(5)
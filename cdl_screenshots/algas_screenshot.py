import time
urls = [('INDUSTRIAL', 'http://algas.com.br/gas-natural/gas-industrial'),
                       ('COMERCIAL', 'http://algas.com.br/gas-natural/gas-comercial'),
                       ('RESIDENCIAL', 'http://algas.com.br/gas-natural/gas-residencial/'),
                       ('COGERACAO', 'http://algas.com.br/gas-natural/geracao-e-cogeracao-de-energia'),
                       ('VEICULAR', 'http://algas.com.br/gas-natural/gnv')]

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/algas'


def captura(driver, data):
    for url in urls:
        driver.get(url[1])
        time.sleep(1)
        #S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        #driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
        #driver.set_window_size(1583, 4310)  # May need manual adjustment
        if 'industrial' in str(url[0]).lower():
            print('CAPTURA INDUSTRIAL')
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/industrial/industrial_{}.png'.format(data))

        elif 'cogeracao' in str(url[0]).lower():
            print('CAPTURA COGERAÇÃO')
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/cogeracao/cogeracao_{}.png'.format(data))

        elif 'veicular' in str(url[0]).lower():
            print('CAPTURA VEICULAR')
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        elif 'residencial' in str(url[0]).lower():
            print('CAPTURA RESIDENCIAL')
            driver.find_element_by_tag_name('body').screenshot(
                main_dir + '/residencial/residencial_{}.png'.format(data))

        elif 'comercial' in str(url[0]).lower():
            print('CAPTURA COMERCIAL')
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))

        time.sleep(1)

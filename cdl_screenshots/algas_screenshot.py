import time

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/algas'
urls = [('INDUSTRIAL', 'http://algas.com.br/gas-natural/gas-industrial'),
                       ('COMERCIAL', 'http://algas.com.br/gas-natural/gas-comercial'),
                       ('RESIDENCIAL', 'http://algas.com.br/gas-natural/gas-residencial/'),
                       ('COGERACAO', 'http://algas.com.br/gas-natural/geracao-e-cogeracao-de-energia'),
                       ('VEICULAR', 'http://algas.com.br/gas-natural/gnv')]



def captura(driver, data):
    for url in urls:
        segmento = str(url[0]).lower()
        link = str(url[1])
        driver.get(link)

        if segmento == 'industrial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/industrial/industrial_{}.png'.format(data))

        elif segmento == 'cogeracao':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/cogeracao/cogeracao_{}.png'.format(data))

        elif segmento == 'veicular':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        elif segmento == 'residencial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/residencial/residencial_{}.png'.format(data))

        elif segmento == 'comercial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))

        time.sleep(2)

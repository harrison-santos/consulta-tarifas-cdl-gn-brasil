import time

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/gasmig'
urls = [('RESIDENCIAL', 'http://www.gasmig.com.br/NossosServicos/Residencial/Paginas/Tarifas.aspx'),
                        ('COMERCIAL', 'http://www.gasmig.com.br/NossosServicos/Comercial/Paginas/Tarifas.aspx'),
                        ('VEICULAR', 'http://www.gasmig.com.br/NossosServicos/Veicular/Paginas/Tarifas.aspx'),
                        ('INDUSTRIAL', 'http://www.gasmig.com.br/NossosServicos/Industrial/Paginas/Tarifas.aspx'),
                        ('COGERACAO', 'http://www.gasmig.com.br/NossosServicos/Cogeracao/Paginas/Tarifas.aspx'),
                        ('COMPRIMIDO', 'http://www.gasmig.com.br/NossosServicos/GNCeGNL/Paginas/Tarifas.aspx')]

def captura(driver, data):
    for url in urls:
        segmento = str(url[0]).lower()
        link = str(url[1])
        driver.get(link)

        if segmento == 'residencial':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/residencial/residencial_{}.png'.format(data))

        elif segmento == 'comercial':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))

        elif segmento == 'industrial':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/industrial/industrial_{}.png'.format(data))

        elif segmento == 'veicular':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        elif segmento == 'cogeracao':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/cogeracao/cogeracao_{}.png'.format(data))

        elif segmento == 'comprimido':
            driver.find_element_by_tag_name('html').screenshot(main_dir + '/comprimido/comprimido_{}.png'.format(data))

        time.sleep(2)




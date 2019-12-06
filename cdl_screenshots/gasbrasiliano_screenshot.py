import time

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/gasbrasiliano'
urls = [('RESIDENCIAL', 'http://www.gasbrasiliano.com.br/residencial/tarifas/'),
                        ('COMERCIAL', 'http://www.gasbrasiliano.com.br/comercial/tarifas/'),
                        ('VEICULAR', 'http://www.gasbrasiliano.com.br/automotivo/tarifas/'),
                        ('INDUSTRIAL', 'http://www.gasbrasiliano.com.br/industrial/tarifas/')]

def captura(driver, data):
    for url in urls:
        segmento = str(url[0]).lower()
        link = str(url[1])
        driver.get(link)

        if segmento == 'residencial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/residencial/residencial_{}.png'.format(data))

        elif segmento == 'comercial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))

        elif segmento == 'industrial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/industrial/industrial_{}.png'.format(data))

        elif segmento == 'veicular':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        time.sleep(2)




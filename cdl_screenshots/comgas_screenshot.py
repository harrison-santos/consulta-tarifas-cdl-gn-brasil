import time

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/comgas'
urls = [("RESIDENCIAL", "https://www.comgas.com.br/tarifas/residencial"),
                        ("COMERCIAL", "https://www.comgas.com.br/tarifas/comercial/"),
                        ("INDUSTRIAL", "https://www.comgas.com.br/tarifas/industrial/"),
                        ("VEICULAR", "https://www.comgas.com.br/tarifas/gas-natural-veicular-gnv/"),
                        ("COMPRIMIDO", "https://www.comgas.com.br/tarifas/gas-natural-comprimido-gnc/")]

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

        elif segmento == 'comprimido':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comprimido/comprimido_{}.png'.format(data))

        time.sleep(2)




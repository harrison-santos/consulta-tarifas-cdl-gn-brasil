import time

main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/compagas'
urls = [("COMERCIAL", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=2"),
    ("INDUSTRIAL", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=1"),
    ("RESIDENCIAL MEDICAO COLETIVA",
     "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=17"),
    ("RESIDENCIAL MEDICAO INDIVIDUAL",
     "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=4"),
    ("VEICULAR", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=3")
]


def captura(driver, data):
    for url in urls:
        segmento = str(url[0]).lower()
        link = str(url[1])
        driver.get(link)

        if segmento == 'comercial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))
        elif segmento == 'industrial':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/industrial/industrial_{}.png'.format(data))
        elif segmento == 'residencial medicao coletiva':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/residencial/residencial_medicao_coletiva_{}.png'.format(data))
        elif segmento == 'residencial medicao individual':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/residencial/residencial_medicao_individual_{}.png'.format(data))
        elif segmento == 'veicular':
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        time.sleep(2)




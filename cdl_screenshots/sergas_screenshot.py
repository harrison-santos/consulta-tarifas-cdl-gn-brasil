import time

url = 'https://www.sergipegas.com.br/cms/tarifas'
main_dir = r'C:/consulta-tarifas-cdl-gn-brasil/files/img/sergas'

def captura(driver, data):
    driver.get(url)
    time.sleep(2)
    elements = driver.find_element_by_xpath("//select[@name='segmentos']")
    all_options = elements.find_elements_by_xpath("//option[@value!='']")
    body = driver.find_element_by_tag_name('body')

    for option in all_options:
        segmento = option.get_attribute("text")
        print("Value is: %s" % option.get_attribute("text"))
        option.click()
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
        #body.screenshot(main_dir.join("/ %s" % str(option))
        print(option)
        if 'industrial' in str(segmento).lower():
            print('CAPTURA INDUSTRIAL')
            driver.find_element_by_tag_name('body').screenshot(main_dir+'/industrial/industrial_{}.png'.format(data))

        elif 'cogeração' in str(segmento).lower():
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/cogeracao/cogeracao_{}.png'.format(data))

        elif 'veicular' in str(segmento).lower():
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/veicular/veicular_{}.png'.format(data))

        elif 'residencial' in str(segmento).lower():
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/residencial/residencial_{}.png'.format(data))

        elif 'comercial' in str(segmento).lower():
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comercial/comercial_{}.png'.format(data))

        elif 'comprimido' in str(segmento).lower():
            driver.find_element_by_tag_name('body').screenshot(main_dir + '/comprimido/comprimido_{}.png'.format(data))

        time.sleep(5)


#EXISTE GNC NO SEGMENTO INDUSTRIAL, COMERCIAL E VEICULAR NA SULGA. OS VALORES DE TARIFAS SÃO OS MESMO MAS EM INDUSTRIAL E VEICULAR EXISTE UMA PARCELA FIXA.
#25/10/2018 -> GASBRASILIANO POSSUI SEGMENTO AUTOMOTIVO ONDE NÃO CAPTUREI OS DADOS.
#25/10/2018 -> VERIFICAR VEICULAR DAS GASMIG.
#EXCLUIDOS: COMGAS GNC POIS SEU VALOR ESTÁ EM CASCATA.


import scrapy
import sys
import urllib
import bs4
from datetime import date
#sys.path.insert(0, 'C:\Users\harrison.santos\PycharmProjects\PyCharm\PythonScrapy\cdl_tarifas\arquivos')
sys.path.insert(1, 'C:\consulta-tarifas-cdl-gn-brasil\cdl_tarifas\cdl_tarifas\spiders')
from empresa import Empresa


class ConsultaTarifasSpider(scrapy.Spider):

    #faixa_auxiliar
    name = 'consulta_comprimido_veicular'
    allowed_domains = ['www.sergipegas.com.br', 'bahiagas.com.br', 'gasmig.com.br', 'compagas.com.br', 'sulgas.rs.gov.br', 'comgas.com.br', 'potigas.com.br',
                       'msgas.com.br', 'copergas.com.br', 'algas.com.br', 'pbgas.com.br', 'scgas.com.br', 'cegas.com.br']
    start_urls = ['http://www.cegas.com.br']


    def parse(self, response):
        #YIELDS
        yield scrapy.Request(url="https://www.sergipegas.com.br/cms/tarifas/", callback=self.envia_sergas, priority=1)
        yield scrapy.Request(url="http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp", callback=self.envia_bahiagas)

        yield scrapy.Request(url="https://www.potigas.com.br/sistema-tarifario", callback=self.envia_potigas)
        yield scrapy.Request(url="http://www.pbgas.com.br/?page_id=1477", callback=self.envia_pbgas)
        yield scrapy.Request(url="https://www.copergas.com.br/atendimento-ao-cliente/tarifas", callback=self.envia_copergas)
        yield from self.envia_compagas()#BEAUTIFUL  SOUP
        #NAOOK yield from self.envia_msgas()#BEAUTIFUL  SOUP
        #NAOOK yield scrapy.Request(url="http://www.cegas.com.br/index.php?option=com_content&view=article&id=322&Itemid=163", callback=self.envia_cegas())
        #NAOOK yield from self.envia_cegas()
        #YIELDS

        #COMGAS
        comgas_links = [("VEICULAR", "https://www.comgas.com.br/tarifas/gas-natural-veicular-gnv/"),
                        ("GNC", "https://www.comgas.com.br/tarifas/gas-natural-comprimido-gnc/")]
        for link in comgas_links:
            callback = lambda response, l=link[0]: self.envia_comgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #COMGAS

        #GASMIG
        gasmig_links = [('VEICULAR', 'http://www.gasmig.com.br/NossosServicos/Veicular/Paginas/Tarifas.aspx'),
                        ('GNC', 'http://www.gasmig.com.br/NossosServicos/GNCeGNL/Paginas/Tarifas.aspx')]
        for link in gasmig_links:
            callback = lambda response, l = link[0]: self.envia_gasmig(response,l)
            yield scrapy.Request(url=link[1], callback=callback)#FUNCIONANDO <- MELHORAR
        #GASMIG

        #SULGAS
        sulgas_links = [("VEICULAR", "http://www.sulgas.rs.gov.br/sulgas/veicular/tabela-de-precos")]
        for link in sulgas_links:
            callback = lambda response, l = link[0]: self.envia_sulgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #SULGAS

        #ALGAS
        algas_links = [("VEICULAR", "http://algas.com.br/gas-natural/gnv")]
        for link in algas_links:
            callback = lambda response, l = link[0]: self.envia_algas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #ALGAS

        #SCGAS
        scgas_links =[("VEICULAR", "http://www.scgas.com.br/conteudos/tarifav")]
        for link in scgas_links:
            callback = lambda response, l = link[0]: self.envia_scgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #SCGAS

    def envia_sergas(self, response):
        sergas = Empresa('SERGAS')
        faixa_auxiliar = "1 a 999.999.999"

        #SERGAS VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 1]/text()').extract()
        vetor_tarifas.extend(response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 2]/p/text()').extract())
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #SERGAS VEICULAR

        #GNC
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab6"]/table/tbody/tr/td[position() < 3]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "GNC", "NAO POSSUI", "POSSUI")
        faixa_auxiliar = [faixa_auxiliar[0]]
        #GNC

    def envia_bahiagas(self, response):
        bahiagas = Empresa("BAHIAGAS")
        faixa_auxiliar = "1 a 999.999.999"
        faixa_auxiliar_max = "999.999.999"

        #VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('/html/body/table[2]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
        #VEICULAR

        #GNC
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//html/body/table[6]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "GNC", "NAO POSSUI", "POSSUI")
        #GNC

    #VERIFICAR VEICULAR GASMIG
    def envia_gasmig(self, response, segmento_):
        gasmig = Empresa('GASMIG')
        faixa_auxiliar = "1 a 999.999.999"

        """elif segmento_ == 'COMERCIAL':
            #PEQUENO CLIENTE NÃO RESIDENCIAL
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de 2.000', '2.001 a 999.999.999')
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 2 orposition() = 4] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "PEQUENO CLIENTE NAO RESIDENCIAL", "POSSUI")
            #PEQUENO CLIENTE NÃO RESIDENCIAL

            #USO GERAL
            primeira_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[1]/td/text()').extract()
            primeira_faixa[0] = primeira_faixa[0].replace('***', '')
            vetor_faixa = [primeira_faixa[0]]
            vetor_faixa.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[position() >= 2 and position() <= 7] / td[1] / text()').extract())
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de 25.000', '25.001 a 999.999.999')
            #vetor tarifas excluindo a primeira faixa com suas tarifas
            vetor_tarifas = ['0', '0']
            vetor_tarifas.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[position() >= 2 and position() <= 7] / td[position() >= 2] / text()').extract())
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            dados[0] = (1, primeira_faixa[0], '0', '0', primeira_faixa[1], primeira_faixa[2])
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "USO GERAL", "POSSUI")
            #USO GERAL

            #elif segmento == 'VEICULAR':
            vetor_faixa = [faixa_auxiliar]
            vetor_tarifas = ['-1']#VERIFICAR O QUE É MVA. POSSUI MVA E ICMS SUBSTITUTO
            tarifa_unica = response.xpath('//*[@id="cbqwpctl00_ctl58_g_31671810_1cd5_491d_92b5_44fe4795928c"]/table/tbody/tr/td[1]/text()').extract()
            vetor_tarifas.extend(tarifa_unica)
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, gasmig.nome, "VEICULAR", "NAO POSSUI")"""

        if segmento_ == 'GNC':
            vetor_faixa = [faixa_auxiliar]
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_334aeb65_c0ce_4a74_a128_881c365a535a"]/table/tbody/tr/td/text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")

    def envia_compagas(self):
        compagas = Empresa("COMPAGAS")
        links = [("VEICULAR", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=3")]
        for link in links:
            segmento = link[0]
            subsegmento = link[1]
            url = link[2]

            s = urllib.request.urlopen(url)#COMANDO CHAVE
            soup = s.read().decode('ISO-8859-1')
            soup = soup.replace("</fo<td>", "</td>")
            #print(soup)
            soup = bs4.BeautifulSoup(soup, "html.parser") #raw text para html
            #print(soup)
            table = soup.find('table', attrs={'class': 'data'})
            #print(table)
            total = len(table.findAll("tr"))
            #print(total)
            row_count = 0
            vetor_faixa = []
            vetor_tarifas = []
            for row in table.findAll("tr"):
                td_count = 0
                if (row_count >= 2) and (row_count <= (total - 2)):
                    dados = ' '
                    for cell in row("td"):
                        valor = cell.get_text().strip()
                        if td_count <= 1:  # 0 1 2 3 = 4
                            vetor_faixa.append(valor)

                        elif td_count == 2 or td_count == 3:
                            vetor_tarifas.append(valor)

                        td_count += 1
                    #linha = str(dados)
                    #print(linha)
                row_count += 1
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
                if (i != 0) and (i % 2 == 0):
                    vetor_faixa[i] = str(int(vetor_faixa[i]) + 1)

            for i in range(0, len(vetor_faixa) - 1):
                vetor_faixa[i] = str(vetor_faixa[i])

            vetor_faixa = compagas.organiza_faixa(vetor_faixa)
            dados = compagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            #print("FX: {}".format(vetor_faixa))
            #print("TRFA: {} Tamanho: {}".format(vetor_tarifas, len(vetor_tarifas)))
            yield from self.envia_dados(dados, compagas.nome, segmento, subsegmento, "NAO POSSUI")

    def envia_sulgas(self, response, segmento_):
        faixa_auxiliar = ["1 a 999.999.999"]
        sulgas = Empresa("SULGAS")
        self.icms = 12.0
        self.pis = 1.65
        self.confins = 7.6

        if(segmento_ == "INDUSTRIAL"):#GNC DENTRO DO LINK DE INDUSTRIAL
            #INDUSTRIAL GNC
            vetor_faixa = faixa_auxiliar
            consulta = response.xpath('/html/body/div[3]/article/div[2]/table[11]/tbody/tr[2]/td[position() > 1]/p/text()').extract()#posicao1 tarifa, posicao2 mmbtu
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, [consulta[0]])
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, [consulta[1]])
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "GNC", "POSSUI")
            #INDUSTRIAL GNC

        elif(segmento_ == "VEICULAR"):
            #VEICULAR
            vetor_faixa = faixa_auxiliar
            vetor_auxiliar = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[2] / td[position() > 1] / text()').extract()
            vetor_tarifas = [vetor_auxiliar[0].replace('\xa0', ' ')]
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = [vetor_auxiliar[1].replace('\xa0', ' ')]
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")
            #VEICULAR

    def envia_comgas(self, response, segmento_):
        comgas = Empresa("COMGAS")
        faixa_auxiliar = ["1 a 999.999.999"]

        if segmento_ == "VEICULAR":
            sub_segmentos = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td / strong / text()').extract()
            vetor_faixa = []
            for i in range(0, 3):
                vetor_faixa.append(faixa_auxiliar[0])
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/ tbody / tr[position() > 2] / td[position() >= 2] / text()').extract()
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            for i in range(0, len(sub_segmentos)):
                yield from self.envia_dados([dados[i]], comgas.nome, segmento_, sub_segmentos[i], "POSSUI")

        """elif segmento_ == "GNC":
            vetor_faixa = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2]/td[2]/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')

            vetor_faixa[0] = vetor_faixa[0].replace('Até 50000,00', '1 a 50000,00')
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('> 2000000,00', '2000001,00 a 999.999.999')
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_parcelas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 3 or position() = 5] / text()').extract()
            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")"""

    #INCOMPLETO
    def envia_cegas(self):
        cegas = Empresa('CEGAS')
        faixa_auxiliar = "1 a 999.999.999"
        vetor_faixa = []
        link = "http://www.cegas.com.br/index.php?option=com_content&view=article&id=322&Itemid=163"
        #necessario segmentos em ordem.
        segmentos = [('VEICULAR', 'NAO POSSUI'), ('VEICULAR', 'COMPRIMIDO')]


        s = urllib.request.urlopen(link)
        soup = s.read().decode('ISO-8859-1')
        soup = bs4.BeautifulSoup(soup, 'html.parser')
        tables = soup.findAll('table', attrs={'bgcolor': '#333399'})
        tam = len(tables)

        if(tam == len(segmentos)):
            tb_count = 1
            tr_count = 1
            td_count = 1
            sp_count = 1

            for table in tables:
                segmento = segmentos[tb_count-1][0]
                subsegmento = segmentos[tb_count - 1][1]

                if(tb_count <= 2):
                    vetor_faixa = []
                    vetor_tarifas = []
                    for tr in table.findAll('tr'):
                        if(tr_count > 1):
                            #print("Linha: {}".format(tr_count))
                            for span in tr.findAll('span'):
                                #print("Span Numero {}".format(sp_count))
                                #print(span.get_text().strip())
                                if(sp_count == 2):
                                    vetor_faixa.append(span.get_text().strip())
                                    #print("Valor: {}  ".format(span.get_text().strip()))
                                elif(sp_count == 3):
                                    vetor_tarifas.append(span.get_text().strip())
                                    #print("Valor: {}  X".format(span.get_text().strip()))
                                elif (sp_count == 4):
                                    vetor_tarifas.append(span.get_text().strip())
                                    #print("Valor: {} S".format(span.get_text().strip()))
                                sp_count = sp_count+1
                            sp_count = 1
                        tr_count= tr_count+1

                    print('{} e {}'.format(segmento, subsegmento))
                    tam = len(vetor_faixa)
                    if(tb_count == 1):
                        vetor_faixa[tam-1] = vetor_faixa[tam-1].replace('60.001 acima', '60.001 a 999.999.999')
                    elif(tb_count == 2):
                        vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('670.001 acima', '670.001 a 999.999.999')


                    dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
                    yield from self.envia_dados(dados, cegas.nome, segmento, subsegmento, "NAO SEI")




                    tr_count = 1
                elif(tb_count >= 3 and tb_count <= 5):
                    vetor_faixa.append(faixa_auxiliar)
                    for tr in table.findAll('tr'):
                       pass
                elif(tb_count >= 6):
                    pass

                tb_count = tb_count+1

        else:
            print("Nao. Variavel Tam: {} e Segmentos: {}".format(tam, len(segmentos)))

        print(dados)

        #for table in tables:
          #  aux = table.findAll('span')
        #print(vetor_faixa)
        #print(vetor_tarifas)
        #dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        #print(dados)

    def envia_potigas(self, response):
        potigas = Empresa("POTIGAS")
        faixa_auxiliar = ["1 a 999.999.999"]


        #GNC
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[3]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome, "GNC", "NAO POSSUI", "NAO POSSUI")
        #GNC

        #VEICULAR
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[4]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR


    #INCOMPLETO
    def envia_msgas(self):###FALTA FAZER
        pass

    def envia_pbgas(self, response):
        pbgas = Empresa("PBGAS")
        faixa_auxiliar = ["1 a 999999999"]

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[5]/tr[position() >=3]/td[position() >= 3]/text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from self.envia_dados(dados, pbgas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #GNC
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[6]/tr[position() >= 3] / td[position() >= 3] / text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from self.envia_dados(dados, pbgas.nome, "GNC", "NAO POSSUI", "NAO POSSUI")
        #GNC

    def envia_copergas(self, response):
        copergas = Empresa("COPERGAS")
        faixa_auxiliar = ['1 a 999.999.999']

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[9]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        dados = copergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, copergas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
        #VEICULAR

    def envia_algas(self, response, segmento_):
        def algas_organiza_faixa(vetor_faixa):
            vetor_aux = []
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace(',', '.')
                aux = vetor_faixa[i].split('a')
                vetor_aux.append(str(int(round(float(aux[0]), 0) + 1)) + ' a ' + aux[1])

            return vetor_aux

        algas = Empresa("ALGAS")
        faixa_auxiliar = ["0 a 999.999.999"]

        if segmento_ == 'VEICULAR':
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")

    #INCOMPLETO
    def envia_gasbrasiliano(self, response, segmento_):
        self.icms = 15
        self.pis = 1.65
        self.confins = 7.60
        gasbrasiliano = Empresa("GAS BRASILIANO")
        def organiza_faixa(vetor_faixa):
            vetor_aux = []
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
                vetor_faixa[i] = vetor_faixa[i].replace(',', '.')
                aux = vetor_faixa[i].split('a')
                vetor_aux.append(str(int(round(float(aux[0]), 0) + 1)) + ' a ' + aux[1])

            return vetor_faixa


    def envia_scgas(self, response, segmento_):
        faixa_auxiliar = ["1 a 999.999.999"]
        scgas = Empresa("SCGAS")

        if segmento_ == "VEICULAR":
            icms = 17
            pis = 1.65
            confins = 7.60
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, segmento_, "NAO POSSUI", "NAO POSSUI")

    def envia_dados(self, dados, nome_empresa, segmento, subsegmento, reducao):
        data_atual = date.today()
        data_atual = data_atual.strftime('%d/%m/%Y')
        volume_acumulado = 0
        fat_acumulado = 0
        fxa_igual = "VERDADEIRO"
        #parcela_fxa = "NAO"
        #reducao = "NAO" #É DEFINIDO COMO RED B CÁLCULO "POSSUI", AQUELAS QUE POSUEM VALOR ABAIXO DO CÁLUCO: ICMS+(7.60+1.65)
        #if (segmento == "COGERACAO" or segmento == "INDUSTRIAL"):

        for i in range(0, len(dados), 1):#percorrer dados pegando sempre o valor de faixa

            if str(dados[i][4]) != '0' or str(dados[i][5]) != '0':
                parcela_fxa = "SIM"
            if 'a' or 'à' in dados[i][1]:#se possuir algum tipo de divisor entre as faixas #ISDIGIT()
                print('dados : {}'.format(dados))
                if 'a' in dados[i][1]:
                    valor = dados[i][1].split('a')#['1 a 70'] com split-> ['1', '70']
                    print('VALOR: {}'.format(valor))
                elif 'à' in dados[i][1]:
                    valor = dados[i][1].split('à')
                    print('VALOR: {}'.format(valor))

                #arredondamento de valores
                valor[0] = round(float(valor[0].replace(',01', '').replace(',00', '')))
                valor[1] = round(float(valor[1].replace(',01', '').replace(',00', '')))
                ##
                if ("999999999" in str(valor[1]) or "9999999" in str(valor[1]) and str(valor[0]) != "0"):
                    valor[1] = str(int(valor[0])*2)
                elif(str(valor[0]) == "0"):
                    valor[1] = "1"

                if int(valor[0]) % 2 != 0:
                    valor[0] = int(valor[0])-1


                valor[0] = int(valor[0])
                valor[1] = int(valor[1])
                volume = valor[1] - valor[0]
                tarifa = float(dados[i][2].replace(',', '.'))
                #print("Volume: {}".format(volume))
                #print("TARIFA: {}".format(tarifa))
                #print(tarifa)
                fat_fxo = str(round(volume*tarifa, 2)).replace('.', ',')
                #print("FATURA: {}".format(fat_fxo))


                if(i == 0):
                    volume_acumulado = volume
                    fat_acumulado = fat_fxo
                    if(volume_acumulado != 0):
                        tarifa_media = str(round(float(fat_acumulado.replace(',', '.'))/volume_acumulado, 4)).replace('.', ',')
                    else:
                        tarifa_media = 0
                else:
                    volume_acumulado += volume#VOLUME ATUAL + VOLUME ANTERIOR
                    fat_acumulado = str(float(fat_acumulado.replace(',', '.'))+float(fat_fxo.replace(',', '.'))).replace('.', ',')
                    tarifa_media = str(round(float(fat_acumulado.replace(',', '.')) / volume_acumulado, 4)).replace('.', ',')

                    ###VERIFICANDO SE O INICIO DA PRÓXIMA FAIXA É IGUAL AO FINAL DA FAIXA ANTERIOR
                    fxa_anterior = dados[i-1][1]#dados na posicao anterior. Ex: '1 a 70'
                    if('a' in fxa_anterior):
                        valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('a')[1])
                        if(valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"
                        else:
                            valor[0] = valor2
                            if(valor[0] == valor2):
                                fxa_igual = "VERDADEIRO"


                    elif('à' in fxa_anterior):
                        valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('à')[1])
                        if (valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"
                        else:
                            fxa_igual = "FALSO"
                    ###

                yield{#Para cada valor envie as mesma informações.
                    "DTA_CNSLTA": data_atual,
                    "CDL": nome_empresa,
                    "SEG": segmento,
                    "SBSEG": subsegmento,
                    "TAR_SIMP": dados[i][2],
                }





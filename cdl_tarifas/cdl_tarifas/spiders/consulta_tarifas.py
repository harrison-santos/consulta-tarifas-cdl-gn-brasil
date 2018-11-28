


import scrapy
import sys
import urllib
import bs4
from datetime import date
sys.path.insert(1, 'C:\consulta-tarifas-cdl-gn-brasil\cdl_tarifas\cdl_tarifas\spiders')
from empresa import Empresa


class ConsultaTarifasSpider(scrapy.Spider):
    name = 'consulta_tarifas'
    allowed_domains = ['sergipegas.com.br', 'bahiagas.com.br', 'gasmig.com.br', 'compagas.com.br', 'sulgas.rs.gov.br', 'comgas.com.br', 'potigas.com.br',
                       'msgas.com.br', 'copergas.com.br', 'algas.com.br', 'pbgas.com.br', 'scgas.com.br', 'cegas.com.br']
    start_urls = ['http://www.bahiagas.com.br']


    def parse(self, response):
        #YIELDS
        yield scrapy.Request(url="https://www.sergipegas.com.br/cms/tarifas/",
                             callback=self.envia_sergas, priority=1)
        yield scrapy.Request(url="http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp",
                             callback=self.envia_bahiagas)
        yield scrapy.Request(url="https://www.potigas.com.br/sistema-tarifario",
                             callback=self.envia_potigas)
        yield scrapy.Request(url="http://www.pbgas.com.br/?page_id=1477",
                             callback=self.envia_pbgas)
        yield scrapy.Request(url="https://www.copergas.com.br/atendimento-ao-cliente/tarifas",
                             callback=self.envia_copergas)
        yield scrapy.Request(url="http://cegas.com.br/tabela-de-tarifas-atual/",
                             callback=self.envia_cegas)
        yield from self.envia_compagas()#BEAUTIFUL  SOUP
        #NAOOK yield from self.envia_msgas()#BEAUTIFUL  SOUP
        #YIELDS

        #COMGAS
        comgas_links = [("RESIDENCIAL", "https://www.comgas.com.br/tarifas/residencial"),
                        ("COMERCIAL", "https://www.comgas.com.br/tarifas/comercial/"),
                        ("INDUSTRIAL", "https://www.comgas.com.br/tarifas/industrial/"),
                        ("VEICULAR", "https://www.comgas.com.br/tarifas/gas-natural-veicular-gnv/"),
                        ("COMPRIMIDO", "https://www.comgas.com.br/tarifas/gas-natural-comprimido-gnc/")]
        for link in comgas_links:
            callback = lambda response, l=link[0]: self.envia_comgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #COMGAS

        #GASMIG
        gasmig_links = [("RESIDENCIAL", "http://www.gasmig.com.br/NossosServicos/Residencial/Paginas/Tarifas.aspx"),
                        ('COMERCIAL', 'http://www.gasmig.com.br/NossosServicos/Comercial/Paginas/Tarifas.aspx'),
                        ('VEICULAR', 'http://www.gasmig.com.br/NossosServicos/Veicular/Paginas/Tarifas.aspx'),
                        ('INDUSTRIAL', 'http://www.gasmig.com.br/NossosServicos/Industrial/Paginas/Tarifas.aspx'),
                        ('COGERACAO', 'http://www.gasmig.com.br/NossosServicos/Cogeracao/Paginas/Tarifas.aspx'),
                        ('COMPRIMIDO', 'http://www.gasmig.com.br/NossosServicos/GNCeGNL/Paginas/Tarifas.aspx')]
        for link in gasmig_links:
            callback = lambda response, l = link[0]: self.envia_gasmig(response,l)
            yield scrapy.Request(url=link[1], callback=callback)#FUNCIONANDO <- MELHORAR
        #GASMIG

        #SULGAS
        sulgas_links = [("INDUSTRIAL", "http://www.sulgas.rs.gov.br/sulgas/industrial/tabela-de-precos"),
                        ("COMERCIAL", "http://www.sulgas.rs.gov.br/sulgas/comercial/tabela-de-precos"),
                        ("RESIDENCIAL", "http://www.sulgas.rs.gov.br/sulgas/residencial/tabela-precos"),
                        ("VEICULAR", "http://www.sulgas.rs.gov.br/sulgas/veicular/tabela-de-precos")]
        for link in sulgas_links:
            callback = lambda response, l = link[0]: self.envia_sulgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #SULGAS

        #ALGAS
        algas_links = [("INDUSTRIAL", "http://algas.com.br/gas-natural/gas-industrial"),
                       ("COMERCIAL", "http://algas.com.br/gas-natural/gas-comercial"),
                       ("RESIDENCIAL", "http://algas.com.br/gas-natural/gas-residencial/"),
                       ("COGERACAO", "http://algas.com.br/gas-natural/geracao-e-cogeracao-de-energia"),
                       ("VEICULAR", "http://algas.com.br/gas-natural/gnv")]
        for link in algas_links:
            callback = lambda response, l = link[0]: self.envia_algas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #ALGAS

        #SCGAS
        scgas_links =[("RESIDENCIAL", "http://www.scgas.com.br/conteudos/tarifar"),
                      ("COMERCIAL", "http://www.scgas.com.br/conteudos/tarifac"),
                      ("VEICULAR", "http://www.scgas.com.br/conteudos/tarifav"),
                      ("INDUSTRIAL TG1", "http://www.scgas.com.br/site/industrial/conteudos/tg1"),
                      ("INDUSTRIAL TG2", "http://www.scgas.com.br/site/industrial/conteudos/tg2"),
                      ("INDUSTRIAL TG3", "http://www.scgas.com.br/site/industrial/conteudos/tg3")
                      ]
        for link in scgas_links:
            callback = lambda response, l = link[0]: self.envia_scgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)
        #SCGAS

    def envia_sergas(self, response):
        sergas = Empresa('SERGAS')
        faixa_auxiliar = "0 a 999.999.999"

        #INDUSTRIAL
        vetor_faixa = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr/td[1]/span/text()").extract()
        #Existe um valor de tarifa que está dentro de um tag span, diferente de todos os outros que estão somente dentro de uma tag td,
        valor_span = response.xpath('//div[contains(@id, "tab1")]/table/tbody/tr[8]/td[3]/span/text()').extract()[0]
        anterior_td = response.xpath('//div[contains(@id, "tab1")]/table/tbody/tr[8]/td[2]/text()').extract()[0]
        vetor_tarifas = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr/td[position() >= 2]/text()").extract()
        vetor_tarifas.insert(vetor_tarifas.index(anterior_td)+1, valor_span)#Tarifa 'valor_span' não foi capturado no response acima mas agora foi adicionado com relacao ao seu anterior.
        ##
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "INDUSTRIAL", "NAO POSSUI", "NAO POSSUI")
        #INDUSTRIAL

        #COGERACAO
        vetor_faixa = response.xpath('//*[@id="tab2"]/table/tbody/tr/td[1]/text()').extract()
        vetor_tarifas = response.xpath('//*[@id="tab2"]/table/tbody/tr/td[position() > 1]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "COGERACAO", "NAO POSSUI", "NAO POSSUI")
        #COGERACAO

        #VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 1]/text()').extract()
        vetor_tarifas.extend(response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 2]/p/text()').extract())
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #RESIDENCIAL
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab4"]/table/tbody/tr/td/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "RESIDENCIAL", "NAO POSSUI", "NAO POSSUI")
        #RESIDENCIAL

        #COMERCIAL
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab5"]/table/tbody/tr/td/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome,  "COMERCIAL", "NAO POSSUI", "NAO POSSUI")
        #COMERCIAL

        #COMPRIMIDO
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab6"]/table/tbody/tr/td[position() < 3]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, sergas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
        #COMPRIMIDO

    def envia_bahiagas(self, response):
        bahiagas = Empresa("BAHIAGAS")
        faixa_auxiliar = "0 a 999.999.999"
        faixa_auxiliar_max = "999.999.999"

        #INDUSTRIAL
        vetor_faixa = response.xpath("//table[1]//tr[position() >= 3 and position() <= 16] / td[position() <= 2] / div / font / span / text()").extract()
        vetor_faixa[len(vetor_faixa)-1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath("//table[1]//tr[position() >= 3 and position() <= 16]/td[position() >= 3]/div/text()").extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "INDUSTRIAL", "NAO POSSUI", "POSSUI")
        #INDUSTRIAL

        #VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('/html/body/table[2]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
        #VEICULAR


        #COMERCIAL
        vetor_faixa = response.xpath('/html/body/table[3]/tr[position() >= 3 and position()<= 15]/td[position() <=2]/div/font/span/text()').extract()
        vetor_faixa[len(vetor_faixa) - 1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('/html/body/table[3]/tr[position() >= 3 and position() <= 15] / td[position() >= 3] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")
        #COMERCIAL



        #Geração, Cogeração e Climatização Comercial
        vetor_faixa = response.xpath('//html/body/table[4]/tr[position() >= 3 and position() <= 15]/td[position() <= 2]/div/font/span/text()').extract()
        vetor_faixa[len(vetor_faixa)-1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('//html/body/table[4]/tr[position() >= 3 and position() <= 15]/td[position() >= 3]/div/text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")
        #Geração, Cogeração e Climatização Comercial


        #COMPRIMIDO
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//html/body/table[6]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, bahiagas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
        #COMPRIMIDO

        #RESIDENCIAL
        vetor_faixa = response.xpath('/html/body/table[7]/tr[position() >= 3]/td[position() <= 2] / div / font / span / text()').extract()
        vetor_faixa[len(vetor_faixa) - 1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('/html/body/table[7]/tr[position() >= 3] / td[position() = 4 or position() = 6] / div / text()').extract()
        vetor_parcelas = response.xpath('/html/body/table[7]/tr[position() >=3] / td[position() = 3 or position() = 5] / div / font / span / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, bahiagas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")
        #RESIDENCIAL

    #VERIFICAR TARIFAS DO VEICULAR. NAO POSSUI SEM IMPOSTO.
    def envia_gasmig(self, response, segmento_):
        gasmig = Empresa('GASMIG')
        faixa_auxiliar = "0 a 999.999.999"

        if segmento_ == "RESIDENCIAL":
            #MEDICAO INDIVIDUAL
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_9f154d0c_f442_4cbd_99ac_040c90b4abc5"]/div/table/tbody/tr/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+ ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_9f154d0c_f442_4cbd_99ac_040c90b4abc5"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_9f154d0c_f442_4cbd_99ac_040c90b4abc5"]/div/table/tbody/tr/td[position() = 2 or position() = 4]/text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "MEDICAO INDIVIDUAL", "POSSUI")
            #MEDICAO INDIVIDUAL

            # MEDICAO COLETIVA
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_e8ccddb0_a1bc_4397_a93b_9da0cdb86a18"]/div/table/tbody/tr/td[position() = 1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam-1]+ ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_e8ccddb0_a1bc_4397_a93b_9da0cdb86a18"]/div/table/tbody/tr/td[position() = 3 or position() = 5] / text()').extract()
            #faixa_tarifas = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_e8ccddb0_a1bc_4397_a93b_9da0cdb86a18"]/div/table/tbody/tr/td[position() = 2 orposition() = 4] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "MEDICAO COLETIVA", "POSSUI")
            #MEDICAO COLETIVA


        elif segmento_ == 'COMERCIAL':
            #PEQUENO CLIENTE NÃO RESIDENCIAL
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_86a48297_f0e3_436f_831d_52708cc6448c"]/div/table/tbody/tr/td[position() = 2 orposition() = 4] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "PEQUENO CLIENTE", "POSSUI")
            #PEQUENO CLIENTE NÃO RESIDENCIAL

            #NAO POSSUI
            primeira_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[1]/td/text()').extract()
            primeira_faixa[0] = primeira_faixa[0].replace('***', '')
            vetor_faixa = [primeira_faixa[0]]
            vetor_faixa.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[position() >= 2 and position() <= 7] / td[1] / text()').extract())
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            #vetor tarifas excluindo a primeira faixa com suas tarifas
            vetor_tarifas = ['0', '0']
            vetor_tarifas.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_d2480188_710f_4ebe_b624_20664a29c517"]/div/table/tbody/tr[position() >= 2 and position() <= 7] / td[position() >= 2] / text()').extract())
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            dados[0] = (1, primeira_faixa[0], '0', '0', primeira_faixa[1], primeira_faixa[2])
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")
            #NAO POSSUI

            """elif segmento == 'VEICULAR':
            vetor_faixa = [faixa_auxiliar]
            vetor_tarifas = ['-1']#VERIFICAR O QUE É MVA. POSSUI MVA E ICMS SUBSTITUTO
            tarifa_unica = response.xpath('//*[@id="cbqwpctl00_ctl58_g_31671810_1cd5_491d_92b5_44fe4795928c"]/table/tbody/tr/td[1]/text()').extract()
            vetor_tarifas.extend(tarifa_unica)
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, gasmig.nome, "VEICULAR", "NAO POSSUI")"""

        elif segmento_ == 'INDUSTRIAL':
            #INDUSTRIAL
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_bc88c2cf_fffb_47bc_bd06_01685cb485de"]/div/table/tbody/tr[position() >= 1 and position() <= 13]/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa[tam - 2] = vetor_faixa[tam - 2].replace('\t', '')
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_bc88c2cf_fffb_47bc_bd06_01685cb485de"]/div/table/tbody/tr[position() >= 1 and position() <= 13] / td[position() >= 2] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")
            #INDUSTRIAL

            #NAO POSSUI
            primeira_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_3841b951_522d_4f47_b5cb_f98857249109"]/div/table/tbody/tr[1]/td/text()').extract()
            primeira_faixa[0] = primeira_faixa[0].replace('***', '')
            vetor_tarifas = ['0', '0']
            vetor_faixa = [primeira_faixa[0]]
            vetor_faixa.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_3841b951_522d_4f47_b5cb_f98857249109"]/div/table/tbody/tr[position() >= 2 and position() <= 7]/td[1]/text()').extract())
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas.extend(response.xpath('//*[@id="cbqwpctl00_ctl58_g_3841b951_522d_4f47_b5cb_f98857249109"]/div/table/tbody/tr[position() >= 2 and position() < 8]/td[position() >= 2] / text()').extract())
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            #primeira faixa
            dados[0] = (1, primeira_faixa[0], '0', '0', primeira_faixa[1], primeira_faixa[2])
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "USO GERAL", "POSSUI")
            #NAO POSSUI

        elif segmento_ == 'COGERACAO':
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr[position() >= 1]/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr/td[position() = 2 or position() = 4]/text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COMPRIMIDO':
            vetor_faixa = [faixa_auxiliar]
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_334aeb65_c0ce_4a74_a128_881c365a535a"]/table/tbody/tr/td/text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")

    def envia_compagas(self):
        faixa_auxiliar = "0 a 999.999.999"
        compagas = Empresa("COMPAGAS")
        links = [
            ("COMERCIAL", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=2"),
            ("INDUSTRIAL", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=1"),
            ("RESIDENCIAL", "MEDICAO COLETIVA",
             "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=17"),
            ("RESIDENCIAL", "MEDICAO INDIVIDUAL",
             "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=4"),
            ("VEICULAR", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=3")
            ]
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
        faixa_auxiliar = ["0 a 999.999.999"]
        sulgas = Empresa("SULGAS")
        self.icms = 12.0
        self.pis = 1.65
        self.confins = 7.6

        if(segmento_ == "INDUSTRIAL"):
            #INDUSTRIAL FIRME
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa), ):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
                vetor_faixa[i] = vetor_faixa[i].replace('  ', '')

            tarifa_s_impsto = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1 and position() <= 5] / td[2] / p / text()').extract()
            tarifa_s_impsto.extend(response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 5] / td[2] / text()').extract())

            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, tarifa_s_impsto)
            vetor_parcelas = response.xpath('//article/div[2]/table[1]/tbody/tr[position() > 1] / td[3] / p / text()').extract()
            vetor_parcelas.extend(response.xpath('//article/div[2]/table[1]/tbody/tr[position() > 5] / td[3] / text()').extract())
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "FIRME", "POSSUI")
            #INDUSTRIAL FIRME

            #INDUSTRIAL DE PEQUENO PORTE
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[3]/ tbody / tr[2] / td / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[1] / p / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('\xa0', ' ')

            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[2] / p / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('\xa0', '')
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[3] / p / text()').extract()
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "PEQUENO PORTE", "POSSUI")
            #INDUSTRIAL DE PEQUENO PORTE

            #INDUSTRIAL INTERRUPTIVEL
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[5]/ tbody / tr / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 1 and position() <= 5] / td[2] / p / text()').extract()
            vetor_tarifas.extend(response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 5] / td[2] / text()').extract())
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 1 and position() <= 3] / td[3] / p / text()').extract()
            vetor_parcelas.extend(response.xpath('/html/body/div[3]/article/div[2]/ table[5] / tbody / tr[position() >= 4] / td[3] / text()').extract())
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "INTERRUPTIVEL", "POSSUI")
            #INDUSTRIAL INTERRUPTIVEL

            #COGERAÇÃO PPT
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
            if vetor_faixa[len(vetor_faixa) - 1] == ' ':
                vetor_faixa.pop()

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[3] / text()').extract()
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, "COGERACAO", "PPT", "POSSUI")
            #COGERAÇÃO PPT

            # COGERAÇÃO, CLIMATIZACAO E GERAÇÃO HORARIO PONTA
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[1] / p / span / text()').extract()
            vetor_faixa.extend(response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[1] / p / text()').extract())
            vetor_faixa[0] = vetor_faixa[0].replace('\xa0', ' ')
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)

            #ABAIXO ESTÁ SENDO FEITO A SOMA DE MMBTU E PARCELA FIXA DEFINIDA PARA O VALOR DE PARCELA FIXA
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            vetor_parcelas[2] = vetor_parcelas[2].replace(',00', '')
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms,self.pis,self.confins,vetor_parcelas)
            tam = len(vetor_parcelas)
            vetor_parcelas[tam-1] = vetor_parcelas[tam-1].replace(',', '')#C IMPOSTO
            vetor_parcelas[tam - 2] = vetor_parcelas[tam - 2].replace(',', '')#S IMPOSTO
            vetor_mmbtu = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[4] / p / text()').extract()
            vetor_mmbtu.insert(1, response.xpath('/html/body/div[3]/article/div[2]/ table[9] / tbody / tr[3] / td[4] / text()').extract()[0])
            vetor_mmbtu = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, vetor_mmbtu)
            vetor_parcelas = sulgas.soma_listas(vetor_parcelas, vetor_mmbtu)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            #CAPTURA ABAIXO yield from self.envia_dados(dados, sulgas.nome, segmento_, "COGERACAO, CLIMATIZACAO E GERAÇAO HORARIO PONTA", "POSSUI")
            yield from self.envia_dados(dados, sulgas.nome, "COGERACAO", "HORARIO PONTA", "POSSUI")#MESMOS VALORES PARA COMERCIAl
            #COGERAÇÃO, CLIMATIZACAO E GERAÇÃO HORARIO PONTA

            #INDUSTRIAL COMPRIMIDO
            vetor_faixa = faixa_auxiliar
            consulta = response.xpath('/html/body/div[3]/article/div[2]/table[11]/tbody/tr[2]/td[position() > 1]/p/text()').extract()#posicao1 tarifa, posicao2 mmbtu
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, [consulta[0]])
            vetor_parcelas = sulgas.calcula_imposto_parcela(self.icms, self.pis, self.confins, [consulta[1]])
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
            #INDUSTRIAL COMPRIMIDO

        elif segmento_ == "COMERCIAL":
            #COMERCIAL
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1]/tbody / tr[position() > 1] / td[1] / p / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')

            vetor_parcelas = sulgas.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")
            #COMERCIAL

        elif(segmento_ == "RESIDENCIAL"):
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1]/tbody/tr[position() > 1]/td[1]/p/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas.append(response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[8] / td[3] / text()').extract()[0])
            vetor_tarifas = sulgas.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')
            vetor_parcelas = sulgas.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")

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
        faixa_auxiliar = ["0 a 999.999.999"]
        if segmento_ == "RESIDENCIAL":
            #MEDICAO INDIVIDUAL
            vetor_faixa = response.xpath('//table[1]//tbody/tr/td/table[1]/tbody/tr[position() > 2] / td[2] / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
            tam = len(vetor_faixa)
            vetor_faixa[tam - 2] = vetor_faixa[tam - 2].replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '').replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+ ' a 999.999.999'

            vetor_tarifas = response.xpath('//table[1]//tbody/tr/td/table[1]/tbody/ tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('–', '0')
            vetor_tarifas[1] = vetor_tarifas[1].replace('–', '0')
            vetor_parcelas = response.xpath('//table[1]//tbody/tr/td/table[1]/tbody / tr[position() > 2] / td[position() = 3 or position() = 5] / text()').extract()

            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "MEDICAO INDIVIDUAL", "POSSUI")
            #MEDICAO INDIVIDUAL

            #MEDICAO COLETIVA
            vetor_faixa = response.xpath('//table/tbody/tr/td/table[2]/tbody/tr/td[2]/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')

            vetor_faixa[0] = vetor_faixa[0].replace('até ', '').replace('Até ', '')
            vetor_faixa[0] = '1 a '+vetor_faixa[0]
            vetor_faixa[2] = vetor_faixa[2].replace('>', '')
            vetor_faixa[2] = vetor_faixa[2]+' a 999.999.999'
            vetor_tarifas = response.xpath('//table/tbody/tr/td/table[2]/tbody/tr/td[position() = 4 or position() = 6] / text()').extract()
            vetor_parcelas = response.xpath('//table/tbody/tr/td/table[2]/tbody/tr/ td[position() = 3 or position() = 5] / text()').extract()

            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "MEDICAO COLETIVA", "POSSUI")
            #MEDICAO COLETIVA

        elif segmento_ == "COMERCIAL":
            vetor_faixa = response.xpath('//table/tbody/tr/td//table/tbody/tr/td[2]/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
            vetor_faixa[0] = vetor_faixa[0].replace('0 – 0', '0 a 0')
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '').replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+ ' a 999.999.999'
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr/td[position() = 4 or position() = 6] / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('–', '0')
            vetor_tarifas[1] = vetor_tarifas[1].replace('–', '0')
            vetor_parcelas = response.xpath('//table/tbody/tr/td//table/tbody/tr/td[position() = 3 or position() = 5] / text() ').extract()
            vetor_parcelas[9] = vetor_parcelas[9].replace('\xa0', '')
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')

            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")

        elif segmento_ == "INDUSTRIAL":
            vetor_faixa = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2]/td[2]/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a '+vetor_faixa[0]
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '').replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'

            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_parcelas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 3 or position() = 5] / text()').extract()
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')

            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")


        elif segmento_ == "VEICULAR":
            sub_segmentos = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td / strong / text()').extract()
            vetor_faixa = []
            for i in range(0, 3):
                vetor_faixa.append(faixa_auxiliar[0])
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/ tbody / tr[position() > 2] / td[position() >= 2] / text()').extract()
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            for i in range(0, len(sub_segmentos)):
                yield from self.envia_dados([dados[i]], comgas.nome, segmento_, sub_segmentos[i], "POSSUI")

        elif segmento_ == "COGERACAO":
            vetor_faixa = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2]/td[2]/text()').extract()

            #COGERACAO DE ENERGIA ELETRICA PARA CONSUMO PROPIO/VENDA CONSUMIDOR FINAL
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '').replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 3 or position() = 5] / text()').extract()
            vetor_tarifas[9] = vetor_tarifas[9].replace('\xa0', '')
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "CNSUMO_PROPRIO/CNSMIDOR_FNAL", "POSSUI")
            #COGERACAO DE ENERGIA ELETRICA PARA CONSUMO PROPRIO/VENDA CONSUMIDOR FINAL

            #COGERACAO DE ENERGIA ELETRICA PARA REVENDA A DISTRIBUIDOR
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_tarifas[8] = vetor_tarifas[8].replace('\xa0', '')
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "REVENDA DISTRIBUIDOR", "POSSUI")
            #COGERACAO DE ENERGIA ELETRICA PARA REVENDA A DISTRIBUIDOR

        elif segmento_ == "COMPRIMIDO":
            vetor_faixa = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2]/td[2]/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')

            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '').replace('.', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_parcelas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 3 or position() = 5] / text()').extract()
            dados = comgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")

    #INCOMPLETO - NAO CAPTURADO
    def envia_cegas(self, response):
        cegas = Empresa('CEGAS')
        faixa_auxiliar = ["0 a 999.999.999"]

        #INDUSTRIAL
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[1]/tbody/tr[position() >= 2]/td[2]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam-1] = cegas.remove_string_acima(vetor_faixa[tam-1])
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[1]/tbody/tr[position() >= 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, cegas.nome, 'INDUSTRIAL', 'NAO POSSUI', 'NAO POSSUI')
        #INDUSTRIAL

        #COGERAÇÃO
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[2]/tbody/tr[position() >= 2]/td[2]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[2]/tbody/tr[position() >= 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, cegas.nome, 'COGERACAO', 'NAO POSSUI', 'NAO POSSUI')
        #COGERAÇÃO

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[3]/tbody/tr[position() = 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, cegas.nome, 'VEICULAR', 'NAO POSSUI', 'NAO POSSUI')
        #VEICULAR

        #COMPRIMIDO FINS INDUSTRIAIS
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[5]/tbody/tr[position() = 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, cegas.nome, 'COMPRIMIDO', 'NAO POSSUI', 'NAO POSSUI')
        #COMPRIMIDO FINS INDUSTRIAIS


        #COMERCIAL
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody/tr[position() >= 3]/td[1]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])

        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody/tr[position() >= 3]/td[position() = 3 or position() = 5]/text()').extract()
        vetor_tarifas[0] = vetor_tarifas[0].replace('–', '0')
        vetor_tarifas[1] = vetor_tarifas[1].replace('–', '0')
        vetor_parcelas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody/tr[position() >= 3]/td[position() = 2 or position() = 4]/text()').extract()
        dados = cegas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, cegas.nome, 'COMERCIAL', 'NAO POSSUI', 'NAO POSSUI')
        #COMERCIAL

        #RESIDENCIAL
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/div/table/tbody/tr[position() >= 3]/td[1]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])

        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/div/table/tbody/tr[position() >= 3]/td[position() = 3 or position() = 5]/text()').extract()
        vetor_tarifas[0] = vetor_tarifas[0].replace('–', '0')
        vetor_tarifas[1] = vetor_tarifas[1].replace('–', '0')
        vetor_parcelas = response.xpath('//article[contains(@id, "post-327")]/div[2]/div/table/tbody/tr[position() >= 3]/td[position() = 2 or position() = 4]/text()').extract()
        dados = cegas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, cegas.nome, 'RESIDENCIAL', 'NAO POSSUI', 'NAO POSSUI')
        #RESIDENCIAL


    def envia_potigas(self, response):
        potigas = Empresa("POTIGAS")
        faixa_auxiliar = ["0 a 999.999.999"]

        #INDUSTRIAL
        vetor_faixa = response.xpath('//*[@id="internas"]/table[1]/tbody/tr[position() > 1] / td[1] / text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam-1] = vetor_faixa[tam-1].replace('Acima de ', '')
        vetor_faixa[tam-1] = vetor_faixa[tam-1]+' a 999.999.999'
        faixa_inicio = [1]

        for i in range(0, tam-1):
            faixa_inicio.append(int(vetor_faixa[i].replace('.', ''))+1)

        vetor_faixa = potigas.agrupa_duas_faixa(faixa_inicio, vetor_faixa)
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[1]/tbody/tr[position() > 1] / td[position() = 2 or position() = 3] / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome,"INDUSTRIAL","NAO POSSUI", "NAO POSSUI")
        #INDUSTRIAL

        #COMPRIMIDO
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[3]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome, "COMPRIMIDO", "NAO POSSUI", "NAO POSSUI")
        #COMPRIMIDO

        #VEICULAR
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[4]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #RESIDENCIAL E COMERCIAL
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[5]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, potigas.nome, "RESIDENCIAL", "NAO POSSUI", "NAO POSSUI")
        yield from self.envia_dados(dados, potigas.nome, "COMERCIAL", "NAO POSSUI", "NAO POSSUI")
        #RESIDENCIAL E COMERCIAL

    #INCOMPLETO - NAO CAPTURADO
    def envia_msgas(self):###FALTA FAZER
        pass

    def envia_pbgas(self, response):
        pbgas = Empresa("PBGAS")
        faixa_auxiliar = ["0 a 999999999"]

        #INDUSTRIAL
        vetor_faixa1 = response.xpath('//*[@id="colLeft"]/table[2]/tr[position() >= 3] / td[position() = 2] / text()').extract()
        for i in range(0, len(vetor_faixa1)):
            vetor_faixa1[i] = str(int(vetor_faixa1[i].replace('.', '')) + 1)
        vetor_faixa2 = response.xpath('//*[@id="colLeft"]/table[2]/tr[position() >= 3] / td[position() = 3] / text()').extract()
        tam = len(vetor_faixa2)
        vetor_faixa2[tam - 1] = vetor_faixa2[tam - 1].replace('-', '999.999.999')
        vetor_faixa = pbgas.agrupa_duas_faixa(vetor_faixa1, vetor_faixa2)
        tarifa_s_imposto = response.xpath('//*[@id="colLeft"]/table[2]/tr[position() >= 3] / td[position() = 5] / text()').extract()
        tarifa_c_imposto = response.xpath('//*[@id="colLeft"]/table[2]/tr[position() >= 3] / td[position() = 4] / text()').extract()
        vetor_tarifas = pbgas.organiza_tarifa_s_c_imposto(tarifa_s_imposto, tarifa_c_imposto)
        dados = pbgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, pbgas.nome, "INDUSTRIAL", "NAO POSSUI", "POSSUI")
        #INDUSTRIAL

        #COMERCIAL
        ####FAIXA 1 VERIFICAR
        vetor_tarifas = ['0', '0']
        parcela_s_imposto = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() = 3] / td[position() = 5] / text()').extract()[0]
        parcela_c_imposto = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() = 3] / td[position() = 4] / text()').extract()[0]
        ####
        vetor_faixa1 = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() >= 3] / td[position() = 2] / text()').extract()
        for i in range(0, len(vetor_faixa1)):
            vetor_faixa1[i] = str(int(vetor_faixa1[i].replace('.', '')) + 1)
        vetor_faixa2 = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() >= 3] / td[position() = 3] / text()').extract()
        tam = len(vetor_faixa2)
        vetor_faixa2[tam - 1] = vetor_faixa2[tam - 1].replace('-', '999.999.999')
        vetor_faixa = pbgas.agrupa_duas_faixa(vetor_faixa1, vetor_faixa2)
        tarifa_s_imposto = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() >= 4] / td[position() = 5] / text()').extract()
        tarifa_c_imposto = response.xpath('//*[@id="colLeft"]/table[3]/tr[position() >= 4] / td[position() = 4] / text()').extract()
        vetor_tarifas.extend(pbgas.organiza_tarifa_s_c_imposto(tarifa_s_imposto, tarifa_c_imposto))
        dados = pbgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        ####ND
        dados[0] = (dados[0][0], dados[0][1], dados[0][2], dados[0][3], parcela_s_imposto, parcela_c_imposto)
        yield from self.envia_dados(dados, pbgas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")
        #COMERCIAL

        #RESIDENCIAL
        vetor_faixa1 = response.xpath('//*[@id="colLeft"]/table[4]/tr[position() >= 3] / td[position() = 2] / text()').extract()
        for i in range(0, len(vetor_faixa1)):
            vetor_faixa1[i] = str(int(vetor_faixa1[i].replace('.', '')) + 1)
        vetor_faixa2 = response.xpath('//*[@id="colLeft"]/table[4]/tr[position() >= 3] / td[position() = 3] / text()').extract()
        vetor_faixa2[1] = vetor_faixa2[1].replace('-', '999.999.999')
        vetor_faixa = pbgas.agrupa_duas_faixa(vetor_faixa1, vetor_faixa2)
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[4]/tr[position() = 4] / td[position() = 4 or position() = 5] / text()').extract()
        vetor_parcelas = response.xpath('//*[@id="colLeft"]/table[4]/tr[position() = 3] / td[position() = 4 or position() = 5] / text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], '0', '0',vetor_parcelas[1], vetor_parcelas[0]))
        dados.append((2, vetor_faixa[1], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from self.envia_dados(dados, pbgas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")
        #RESIDENCIAL

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[5]/tr[position() >=3]/td[position() >= 3]/text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from self.envia_dados(dados, pbgas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #COMPRIMIDO
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[6]/tr[position() >= 3] / td[position() >= 3] / text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from self.envia_dados(dados, pbgas.nome, "COMPRIMIDO", "NAO POSSUI", "NAO POSSUI")
        #COMPRIMIDO

    def envia_copergas(self, response):
        copergas = Empresa("COPERGAS")
        faixa_auxiliar = ['0 a 999.999.999']

        #INDUSTRIAL GRANDE PORTE
        vetor_faixa = response.xpath('//*[@id="content"]/article/table[1]/tbody/ tr[position() >= 3] / td[1] / text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('acima de ', '').replace('Acima de ', '')
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+' a 999.999.999'
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[1]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        vetor_parcelas = response.xpath('//*[@id="content"]/article/table[1]/tbody / tr[position() >= 3] / td[position() = 3 or position() = 5] / text()').extract()
        dados = copergas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados,copergas.nome, "INDUSTRIAL", "GRANDE PORTE", "POSSUI")
        yield from self.envia_dados(dados, copergas.nome, "COMERCIAL", "GRANDE PORTE", "POSSUI")
        #INDUSTRIAL GRANDE PORTE

        #INDUSTRIAL PEQUENO PORTE
        vetor_faixa = response.xpath('//*[@id="content"]/article/table[5]/tbody / tr[position() >= 3] / td[1] / text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('acima de ', '').replace('Acima de ', '')
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[5]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        vetor_parcelas = response.xpath('//*[@id="content"]/article/table[5]/tbody / tr[position() >= 3] / td[position() = 3 or position() = 5] / text()').extract()
        dados = copergas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, copergas.nome, "INDUSTRIAL", "PEQUENO PORTE", "POSSUI")
        yield from self.envia_dados(dados, copergas.nome, "COMERCIAL", "PEQUENO PORTE", "POSSUI")
        #INDUSTRIAL PEQUENO PORTE

        #RESIDENCIAL
        vetor_faixa = response.xpath('//*[@id="content"]/article/table[7]/tbody / tr[position() >= 3] / td[1] / text()').extract()
        tam = len(vetor_faixa)
        #vetor_faixa[tam-1] = vetor_faixa[tam-1].replace('3.000', '3.001')
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[7]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        vetor_parcelas = response.xpath('//*[@id="content"]/article/table[7]/tbody / tr[position() >= 3] / td[position() = 3 or position() = 5] / text()').extract()
        dados = copergas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, copergas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")
        #RESIDENCIAL

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[9]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        dados = copergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from self.envia_dados(dados, copergas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
        #VEICULAR

        #COGERACAO
        vetor_faixa = response.xpath('//*[@id="content"]/article/table[17]/tbody / tr[position() >= 3] / td[1] / text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('acima de ', '').replace('Acima de ', '')
        vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'

        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[17]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        vetor_parcelas = response.xpath('//*[@id="content"]/article/table[17]/tbody / tr[position() >= 3] / td[position() = 3 or position() = 5] / text()').extract()
        dados = copergas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from self.envia_dados(dados, copergas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")
        #COGERACAO

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
        if segmento_ == "INDUSTRIAL":
            vetor_faixa = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 2] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa = algas_organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/ div[2] / table / tbody / tr[position() >= 2] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "INDUSTRIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COMERCIAL':
            vetor_faixa = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            print("TAMAAAAAAAAANHO: {}".format(tam))
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'RESIDENCIAL':
            vetor_faixa = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2]/table/tbody/tr[position() >= 3]/td[position() >= 2]/text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COGERACAO':
            vetor_faixa = response.xpath('//*[@id="content"]/div/table/tbody/tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="content"]/div/table/tbody/tr[position() >= 3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'VEICULAR':
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, algas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")

    #INCOMPLETO. VERIFICAR TAMBÉM QUE É SÓ MOSTRADO A TARIFA COM IMPOSTO
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
        if segmento_ == "RESIDENCIAL":
            #MEDICAO INDIVIDUAL
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr[position() >= 1] / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[4] / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('-', '0')
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasbrasiliano.nome, "RESIDENCIAL", "MEDICAO INDIVIDUAL", "POSSUI")
            #MEDICAO INDIVIDUAL

            #MEDICAO COLETIVA
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr[position() >= 1] / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[4] / text()').extract()
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasbrasiliano.nome, "RESIDENCIAL", "MEDICAO COLETIVA", "POSSUI")
            #MEDICAO COLETIVA

        elif segmento_ == "COMERCIAL":
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[4] / text()').extract()
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from self.envia_dados(dados, gasbrasiliano.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == "INDUSTRIAL":
            #INDUSTRIAL PEQUENO PORTE
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[2] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a '+vetor_faixa[0]
            vetor_faixa[0] = vetor_faixa[0] + ' a 999.999.999'
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            #INDUSTRIAL PEQUENO PORTE
            pass

    def envia_scgas(self, response, segmento_):
        faixa_auxiliar = ["0 a 999.999.999"]
        scgas = Empresa("SCGAS")
        if segmento_ == "RESIDENCIAL":
            icms = 17
            pis = 1.65
            confins = 7.60
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados,scgas.nome, segmento_, "MEDICAO COLETIVA", "NAO POSSUI")

        elif segmento_ == "COMERCIAL":
            icms = 17
            pis = 1.65
            confins = 7.60
            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/div[2] / table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a '+vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, segmento_, "NAO POSSUI", "NAO POSSUI")

        elif segmento_ == "VEICULAR":
            icms = 17
            pis = 1.65
            confins = 7.60
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, segmento_, "NAO POSSUI", "NAO POSSUI")

        elif segmento_ == "INDUSTRIAL TG1":
            icms = 12#reducao da base de calculo
            pis = 1.65
            confins = 7.60
            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG1", "POSSUI")

        elif segmento_ == "INDUSTRIAL TG2":
            icms = 12  # reducao da base de calculo
            pis = 1.65
            confins = 7.60
            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG2", "POSSUI")

        elif segmento_ == "INDUSTRIAL TG3":
            icms = 12  #reducao da base de calculo
            pis = 1.65
            confins = 7.60
            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr[position() <= 12] / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr[position() <= 12] / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, pis, confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from self.envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG3", "POSSUI")

    def envia_dados(self, dados, nome_empresa, segmento, subsegmento, reducao):
        data_atual = date.today()
        data_atual = data_atual.strftime('%d/%m/%Y')
        volume_acumulado = 0
        fat_acumulado = 0
        fxa_igual = "VERDADEIRO"
        fxa_uni = "NAO"

        #parcela_fxa = "NAO"

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

                if int(valor[0]) % 2 != 0:
                    valor[0] = int(valor[0])-1

                #Na última faixa o valor de "FXA_FIM" vai ser igual ao dobro de "FXA_INI"
                if (str(valor[0]) != "0" and "999999999" in str(valor[1]) or "9999999" in str(valor[1])):
                    valor[1] = str(int(valor[0])*2)

                if(str(valor[0]) == "0" and "999999999" in str(valor[1]) or "99999999" in str(valor[1]) or "9999999" in str(valor[1])):
                    valor[1] = "0"

                if(len(dados) == 1 and str(valor[0]) == "0" and str(valor[1]) == "0" ):
                    fxa_uni = "SIM"
                else:
                    fxa_uni = "NAO"

                valor[0] = int(valor[0])
                valor[1] = int(valor[1])

                ###VERIFICANDO SE O INICIO DA PRÓXIMA FAIXA É IGUAL AO FINAL DA FAIXA ANTERIOR
                if(i != 0):
                    fxa_anterior = dados[i - 1][1]  # dados na posicao anterior. Ex: '1 a 70'
                    if ('a' in fxa_anterior):
                        valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('a')[1])
                        if (valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"
                        else:
                            valor[0] = valor2
                            if (valor[0] == valor2):
                                fxa_igual = "VERDADEIRO"


                    elif ('à' in fxa_anterior):
                        valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('à')[1])
                        if (valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"
                        else:
                            valor[0] = valor2
                            if (valor[0] == valor2):
                                fxa_igual = "VERDADEIRO"
                    ###VERFIM

                volume = valor[1] - valor[0]
                tarifa = float(dados[i][2].replace(',', '.'))
                fat_fxo = str(round(volume*tarifa, 2)).replace('.', ',')


                if(i == 0):
                    volume_acumulado = volume
                    fat_acumulado = fat_fxo
                    if(volume_acumulado != 0):
                        tarifa_media = str(round(float(fat_acumulado.replace(',', '.'))/volume_acumulado, 4)).replace('.', ',')
                    else:
                        tarifa_media = str(round(tarifa, 4)).replace('.', ',')
                else:
                    volume_acumulado += volume#VOLUME ATUAL + VOLUME ANTERIOR
                    fat_acumulado = str(float(fat_acumulado.replace(',', '.'))+float(fat_fxo.replace(',', '.'))).replace('.', ',')
                    tarifa_media = str(round(float(fat_acumulado.replace(',', '.')) / volume_acumulado, 4)).replace('.', ',')



                yield{#Para cada valor envie as mesma informações.
                    "DTA_CST": data_atual,
                    "COD_CDL": nome_empresa,
                    "NME_SEG": segmento,
                    "NME_SBSEG": subsegmento,
                    "FXA_INI": valor[0],
                    "FXA_FIM": valor[1],
                    "FXA_UNI": fxa_uni,
                    "FXA_IGUAL": fxa_igual,
                    "TAR_SIM": dados[i][2],
                    "VOL_FXA": volume,
                    "VOL_ACU": volume_acumulado,
                    "FAT_FXA": fat_fxo,
                    "FAT_ACU": fat_acumulado,
                    "TAR_MED": tarifa_media
                }




    """FEITO O CÁLCULO DE TARIFA SEM IMPOSTO: 
    Residencial: SULGAS, Brasiliano, SCGAS. 
    COMERCIAL: Brasiliano, SCGAS. 
    VEICULAR: SCGAS. 
    INDUSTRIAL: SCGAS.
    
    CÁLCULO TARIFA SEM IMPOSTO
    VARIAVEIS = ICMS, PIS, CONFINS, TAR_CIMP
    impostos = ICMS+PIS+CONFINS
    tar_simp = tar_cimp - (tar_cimp*(impostos/100))
    """

    """FEITO CÁLCULO TARIFA COM IMPOSTO
    INDUSTRIAL: SULGAS.
    COMERCIAL: SULGAS.
    VEICULAR: SULGAS."""


    """"ANOTAÇÕES:
        CEGAS -> Os campos de tarifas que estão sendo capturados são tarifa_simp e tar_venda_prazo.
    """
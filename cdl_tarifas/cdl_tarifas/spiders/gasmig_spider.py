# -*- coding: utf-8 -*-
import scrapy
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess

class GasmigSpiderSpider(scrapy.Spider):
    name = 'gasmig_spider'
    allowed_domains = ['gasmig.com.br']
    start_urls = ['http://www.gasmig.com.br/']

    def parse(self, response):
        gasmig_links = [('RESIDENCIAL', 'http://www.gasmig.com.br/NossosServicos/Residencial/Paginas/Tarifas.aspx'),
                        ('COMERCIAL', 'http://www.gasmig.com.br/NossosServicos/Comercial/Paginas/Tarifas.aspx'),
                        ('VEICULAR', 'http://www.gasmig.com.br/NossosServicos/Veicular/Paginas/Tarifas.aspx'),
                        ('INDUSTRIAL', 'http://www.gasmig.com.br/NossosServicos/Industrial/Paginas/Tarifas.aspx'),
                        ('COGERACAO', 'http://www.gasmig.com.br/NossosServicos/Cogeracao/Paginas/Tarifas.aspx'),
                        ('COMPRIMIDO', 'http://www.gasmig.com.br/NossosServicos/GNCeGNL/Paginas/Tarifas.aspx')]
        for link in gasmig_links:
            callback = lambda response, l=link[0]: self.envia_gasmig(response, l)
            yield scrapy.Request(url=link[1], callback=callback)  # FUNCIONANDO <- MELHORAR

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
            yield from envia_dados(dados, gasmig.nome, segmento_, "MEDICAO INDIVIDUAL", "POSSUI")
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
            yield from envia_dados(dados, gasmig.nome, segmento_, "MEDICAO COLETIVA", "POSSUI")
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
            yield from envia_dados(dados, gasmig.nome, segmento_, "PEQUENO PORTE", "POSSUI")
            #PEQUENO CLIENTE NÃO RESIDENCIAL

            #NAO POSSUI
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_ea4022ca_30af_4811_83f9_4b3aff99dff4"]/div/table/tbody/tr/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'

            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_ea4022ca_30af_4811_83f9_4b3aff99dff4"]/div/table/tbody/tr/td[position() = 3 or position() = 5] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")
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
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_bc88c2cf_fffb_47bc_bd06_01685cb485de"]/div/table/tbody/tr[position() >= 1 and position() <= 9]/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_bc88c2cf_fffb_47bc_bd06_01685cb485de"]/div/table/tbody/tr[position() >= 1 and position() <= 9] / td[position() >= 2] / text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")
            #INDUSTRIAL

            #NAO POSSUI
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_c02bb240_fa4c_4d34_a9ef_71d285ef2f11"]/div/table/tbody/tr/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_c02bb240_fa4c_4d34_a9ef_71d285ef2f11"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasmig.nome, segmento_, "CI - 01", "POSSUI")
            #NAO POSSUI

        elif segmento_ == 'COGERACAO':
            vetor_faixa = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr[position() >= 1]/td[1]/text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr/td[position() = 3 or position() = 5]/text()').extract()
            vetor_parcelas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_a4c4a739_e889_4340_95f0_5b372388fa14"]/div/table/tbody/tr/td[position() = 2 or position() = 4]/text()').extract()
            dados = gasmig.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COMPRIMIDO':
            vetor_faixa = [faixa_auxiliar]
            vetor_tarifas = response.xpath('//*[@id="cbqwpctl00_ctl58_g_334aeb65_c0ce_4a74_a128_881c365a535a"]/table/tbody/tr/td/text()').extract()
            dados = gasmig.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasmig.nome, segmento_, "NAO POSSUI", "POSSUI")


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(GasmigSpiderSpider)
    process.start()
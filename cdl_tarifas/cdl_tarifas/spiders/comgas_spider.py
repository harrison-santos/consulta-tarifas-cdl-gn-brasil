# -*- coding: utf-8 -*-
import scrapy
from empresa import Empresa
from envia import envia_dados
from scrapy.crawler import CrawlerProcess

class ComgasSpiderSpider(scrapy.Spider):
    name = 'comgas_spider'
    allowed_domains = ['comgas.com.br']
    start_urls = ['http://www.comgas.com.br/']

    def parse(self, response):
        comgas_links = [("RESIDENCIAL", "https://www.comgas.com.br/tarifas/residencial"),
                        ("COMERCIAL", "https://www.comgas.com.br/tarifas/comercial/"),
                        ("INDUSTRIAL", "https://www.comgas.com.br/tarifas/industrial/"),
                        ("VEICULAR", "https://www.comgas.com.br/tarifas/gas-natural-veicular-gnv/"),
                        ("COMPRIMIDO", "https://www.comgas.com.br/tarifas/gas-natural-comprimido-gnc/")]
        for link in comgas_links:
            callback = lambda response, l=link[0]: self.envia_comgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)

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
            yield from envia_dados(dados, comgas.nome, segmento_, "MEDICAO INDIVIDUAL", "POSSUI")
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
            yield from envia_dados(dados, comgas.nome, segmento_, "MEDICAO COLETIVA", "POSSUI")
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
            yield from envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")

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
            yield from envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")

        elif segmento_ == "VEICULAR":
            sub_segmentos = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td / strong / text()').extract()
            vetor_faixa = []
            for i in range(0, 3):
                vetor_faixa.append(faixa_auxiliar[0])
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/ tbody / tr[position() > 2] / td[position() >= 2] / text()').extract()
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            for i in range(0, len(sub_segmentos)):
                yield from envia_dados([dados[i]], comgas.nome, segmento_, sub_segmentos[i], "POSSUI")

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
            yield from envia_dados(dados, comgas.nome, segmento_, "CNSUMO_PROPRIO/CNSMIDOR_FNAL", "POSSUI")
            #COGERACAO DE ENERGIA ELETRICA PARA CONSUMO PROPRIO/VENDA CONSUMIDOR FINAL

            #COGERACAO DE ENERGIA ELETRICA PARA REVENDA A DISTRIBUIDOR
            vetor_tarifas = response.xpath('//table/tbody/tr/td//table/tbody/tr[position() > 2] / td[position() = 4 or position() = 6] / text()').extract()
            vetor_tarifas[8] = vetor_tarifas[8].replace('\xa0', '')
            dados = comgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, comgas.nome, segmento_, "REVENDA DISTRIBUIDOR", "POSSUI")
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
            yield from envia_dados(dados, comgas.nome, segmento_, "NAO POSSUI", "POSSUI")

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(ComgasSpiderSpider)
    process.start()
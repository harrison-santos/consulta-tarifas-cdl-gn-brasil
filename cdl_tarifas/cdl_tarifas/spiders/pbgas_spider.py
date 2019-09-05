# -*- coding: utf-8 -*-
import scrapy
from empresa import Empresa
from envia import envia_dados
from scrapy.crawler import CrawlerProcess

class PbgasSpiderSpider(scrapy.Spider):
    name = 'pbgas_spider'
    allowed_domains = ['pbgas.com.br']
    start_urls = ['http://www.pbgas.com.br/']

    def parse(self, response):
        yield scrapy.Request(url='http://www.pbgas.com.br/?page_id=1477',
                             callback=self.envia_pbgas)

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
        yield from envia_dados(dados, pbgas.nome, "INDUSTRIAL", "NAO POSSUI", "POSSUI")
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
        yield from envia_dados(dados, pbgas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")
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
        yield from envia_dados(dados, pbgas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")
        #RESIDENCIAL

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[5]/tr[position() >=3]/td[position() >= 3]/text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from envia_dados(dados, pbgas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #COMPRIMIDO
        vetor_tarifas = response.xpath('//*[@id="colLeft"]/table[6]/tr[position() >= 3] / td[position() >= 3] / text()').extract()
        dados = []
        dados.append((1, vetor_faixa[0], vetor_tarifas[1], vetor_tarifas[0], '0', '0'))
        yield from envia_dados(dados, pbgas.nome, "COMPRIMIDO", "NAO POSSUI", "NAO POSSUI")
        #COMPRIMIDO

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(PbgasSpiderSpider)
    process.start()
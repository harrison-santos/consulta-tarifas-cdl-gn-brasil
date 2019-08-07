# -*- coding: utf-8 -*-
import scrapy
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess

class PotigasSpiderSpider(scrapy.Spider):
    name = 'potigas_spider'
    allowed_domains = ['potigas.com.br']
    start_urls = ['https://www.potigas.com.br/']

    def parse(self, response):
        yield scrapy.Request(url='https://www.potigas.com.br/sistema-tarifario',
                             callback=self.envia_potigas)

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
        yield from envia_dados(dados, potigas.nome,"INDUSTRIAL","NAO POSSUI", "NAO POSSUI")
        #INDUSTRIAL

        #COMPRIMIDO
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[3]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, potigas.nome, "COMPRIMIDO", "NAO POSSUI", "NAO POSSUI")
        #COMPRIMIDO

        #VEICULAR
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[4]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, potigas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        #VEICULAR

        #RESIDENCIAL E COMERCIAL
        vetor_tarifas = response.xpath('//*[@id="internas"]/table[5]/tbody/tr[position() > 1] / td / text()').extract()
        dados = potigas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, potigas.nome, "RESIDENCIAL", "NAO POSSUI", "NAO POSSUI")
        yield from envia_dados(dados, potigas.nome, "COMERCIAL", "NAO POSSUI", "NAO POSSUI")


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(PotigasSpiderSpider)
    process.start()
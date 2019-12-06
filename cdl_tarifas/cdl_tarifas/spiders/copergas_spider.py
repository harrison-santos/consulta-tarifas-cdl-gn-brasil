# -*- coding: utf-8 -*-
import scrapy
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess

class CopergasSpiderSpider(scrapy.Spider):
    name = 'copergas_spider'
    allowed_domains = ['copergas.com.br']
    start_urls = ['http://www.copergas.com.br/']

    def parse(self, response):
        yield scrapy.Request(url='https://www.copergas.com.br/atendimento-ao-cliente/tarifas',
                             callback=self.envia_copergas)


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
        yield from envia_dados(dados,copergas.nome, "INDUSTRIAL", "GRANDE PORTE", "POSSUI")
        yield from envia_dados(dados, copergas.nome, "COMERCIAL", "GRANDE PORTE", "POSSUI")
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
        yield from envia_dados(dados, copergas.nome, "INDUSTRIAL", "PEQUENO PORTE", "POSSUI")
        yield from envia_dados(dados, copergas.nome, "COMERCIAL", "PEQUENO PORTE", "POSSUI")
        #INDUSTRIAL PEQUENO PORTE

        #RESIDENCIAL
        vetor_faixa = response.xpath('//*[@id="content"]/article/table[17]/tbody/tr[position()>= 3]/td[1]/text()').extract()
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[17]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        vetor_parcelas = response.xpath('//*[@id="content"]/article/table[17]/tbody / tr[position() >= 3] / td[position() = 3 or position() = 5] / text()').extract()
        dados = copergas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from envia_dados(dados, copergas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")
        #RESIDENCIAL

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//*[@id="content"]/article/table[9]/tbody / tr[position() >= 3] / td[position() = 2 or position() = 4] / text()').extract()
        for i in range(0, len(vetor_tarifas)):
            vetor_tarifas[i] = vetor_tarifas[i].replace('.', ',')
        dados = copergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, copergas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
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
        yield from envia_dados(dados, copergas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")
        #COGERACAO


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(CopergasSpiderSpider)
    process.start()
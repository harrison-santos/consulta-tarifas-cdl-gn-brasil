# -*- coding: utf-8 -*-
from lxml import html
import scrapy
import bs4
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess


class CegasSpiderSpider(scrapy.Spider):
    name = 'cegas_spider'
    allowed_domains = ['cegas.com.br']
    start_urls = ['http://www.cegas.com.br/']

    def parse(self, response):
        yield scrapy.Request(url='http://cegas.com.br/tabela-de-tarifas-atual/',
                             callback=self.envia_cegas)

    def envia_cegas(self, response):
        cegas = Empresa('CEGAS')
        faixa_auxiliar = ["0 a 999.999.999"]

        #INDUSTRIAL
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[1]/tbody/tr[position() >= 2]/td[2]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam-1] = cegas.remove_string_acima(vetor_faixa[tam-1])
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[1]/tbody/tr[position() >= 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, cegas.nome, 'INDUSTRIAL', 'NAO POSSUI', 'NAO POSSUI')
        #INDUSTRIAL

        #COGERAÇÃO
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[2]/tbody/tr[position() >= 2]/td[2]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[2]/tbody/tr[position() >= 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, cegas.nome, 'COGERACAO', 'NAO POSSUI', 'NAO POSSUI')
        #COGERAÇÃO

        #VEICULAR
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[3]/tbody/tr[position() = 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, cegas.nome, 'VEICULAR', 'NAO POSSUI', 'NAO POSSUI')
        #VEICULAR

        #COMPRIMIDO FINS INDUSTRIAIS
        vetor_faixa = faixa_auxiliar
        vetor_tarifas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[5]/tbody/tr[position() = 2]/td[position() > 2]/text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, cegas.nome, 'COMPRIMIDO', 'NAO POSSUI', 'NAO POSSUI')
        #COMPRIMIDO FINS INDUSTRIAIS


        #COMERCIAL
        vetor_faixa = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody/tr[position() >= 3]/td[2]/text()').extract()
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])

        vetor_tarifas = ['0', '0']
        vetor_tarifas.extend(response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody/tr[position() >= 3]/td[position() = 3 or position() = 5]/text()').extract())
        vetor_parcelas = response.xpath('//article[contains(@id, "post-327")]/div[2]/table[6]/tbody / tr[position() >= 4] / td[position() = 3 or position() = 5] / text()').extract()
        dados = cegas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, cegas.nome, 'COMERCIAL', 'NAO POSSUI', 'NAO POSSUI')
        #COMERCIAL

        #RESIDENCIAL

        soup = bs4.BeautifulSoup(response.text, "html.parser")  # raw text para html
        soup = str(soup.findAll('table')[6])
        tree = html.fromstring(soup)
        vetor_faixa = tree.xpath('//tr[position() >= 3]/td[2]/text()')
        tam = len(vetor_faixa)
        vetor_faixa[tam - 1] = cegas.remove_string_acima(vetor_faixa[tam - 1])
        qtd_tarifas = len(tree.xpath('//tr[position() >= 3]/td[position() = 3 or position() = 5]/text()'))
        if(len(vetor_faixa)*2 == qtd_tarifas):
            vetor_tarifas = tree.xpath('//tr[position() >= 3]/td[position() = 3 or position() = 5]/text()')
        else:
            vetor_tarifas = ['0', '0']
            vetor_tarifas.extend(tree.xpath('//tr[position() >= 3]/td[position() = 3 or position() = 5]/text()'))

        print(vetor_faixa)
        print(vetor_tarifas)
        #dados = cegas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        #yield from envia_dados(dados, cegas.nome, 'RESIDENCIAL', 'NAO POSSUI', 'NAO POSSUI')
        #RESIDENCIAL

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(CegasSpiderSpider)
    process.start()
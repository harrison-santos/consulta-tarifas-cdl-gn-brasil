# -*- coding: utf-8 -*-
import scrapy
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess

class AlgasSpiderSpider(scrapy.Spider):
    name = 'algas_spider'
    allowed_domains = ['algas.com.br']
    start_urls = ['http://www.algas.com.br/']

    def parse(self, response):
        algas_links = [('INDUSTRIAL', 'http://algas.com.br/gas-natural/gas-industrial'),
                       ('COMERCIAL', 'http://algas.com.br/gas-natural/gas-comercial'),
                       ('RESIDENCIAL', 'http://algas.com.br/gas-natural/gas-residencial/'),
                       ('COGERACAO', 'http://algas.com.br/gas-natural/geracao-e-cogeracao-de-energia'),
                       ('VEICULAR', 'http://algas.com.br/gas-natural/gnv')]
        for link in algas_links:
            callback = lambda response, l=link[0]: self.envia_algas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)

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
            yield from envia_dados(dados, algas.nome, "INDUSTRIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COMERCIAL':
            vetor_faixa = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            print("TAMAAAAAAAAANHO: {}".format(tam))
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, algas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'RESIDENCIAL':
            vetor_faixa = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2]/table/tbody/tr[position() >= 3]/td[position() >= 2]/text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, algas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'COGERACAO':
            vetor_faixa = response.xpath('//*[@id="content"]/div/table/tbody/tr[position() >= 3] / td[1] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('+', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('//*[@id="content"]/div/table/tbody/tr[position() >= 3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, algas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")

        elif segmento_ == 'VEICULAR':
            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="acontent"]/section[2]/div/div/div[2] / table / tbody / tr[3] / td[position() >= 2] / text()').extract()
            dados = algas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, algas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'

        })
    process.crawl(AlgasSpiderSpider)
    process.start()
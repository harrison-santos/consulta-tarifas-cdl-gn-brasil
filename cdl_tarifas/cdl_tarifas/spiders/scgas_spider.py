# -*- coding: utf-8 -*-
import scrapy
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess


class ScgasSpiderSpider(scrapy.Spider):
    name = 'scgas_spider'
    allowed_domains = ['www.scgas.com.br']
    start_urls = ['http://www.scgas.com.br/']

    def parse(self, response):
        scgas_links = [('RESIDENCIAL', 'http://www.scgas.com.br/conteudos/tarifar'),
                       ('COMERCIAL', 'http://www.scgas.com.br/conteudos/tarifac'),
                       ('VEICULAR', 'http://www.scgas.com.br/conteudos/tarifav'),
                       ('INDUSTRIAL TG1', 'http://www.scgas.com.br/site/industrial/conteudos/tg1'),
                       ('INDUSTRIAL TG2', 'http://www.scgas.com.br/site/industrial/conteudos/tg2'),
                       ('INDUSTRIAL TG3', 'http://www.scgas.com.br/site/industrial/conteudos/tg3')
                       ]
        for link in scgas_links:
            callback = lambda response, l=link[0]: self.envia_scgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)


    def envia_scgas(self, response, segmento_):
        self.pis = 1.65
        self.confins = 7.60
        faixa_auxiliar = ["0 a 999.999.999"]
        scgas = Empresa("SCGAS")
        if segmento_ == "RESIDENCIAL":
            icms = 17

            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados,scgas.nome, segmento_, "MEDICAO COLETIVA", "NAO POSSUI")

        elif segmento_ == "COMERCIAL":
            icms = 17

            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/div[2] / table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a '+vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, scgas.nome, segmento_, "NAO POSSUI", "NAO POSSUI")

        elif segmento_ == "VEICULAR":
            icms = 17

            vetor_faixa = faixa_auxiliar
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ div[2] / table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, scgas.nome, segmento_, "NAO POSSUI", "NAO POSSUI")

        elif segmento_ == "INDUSTRIAL TG1":
            icms = 12#reducao da base de calculo

            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG1", "POSSUI")

        elif segmento_ == "INDUSTRIAL TG2":
            icms = 12  # reducao da base de calculo

            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG2", "POSSUI")

        elif segmento_ == "INDUSTRIAL TG3":
            icms = 12  #reducao da base de calculo

            vetor_faixa = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/table / tbody / tr[position() <= 12] / td[1] / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '1 a ' + vetor_faixa[0]
            vetor_tarifas = response.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ table / tbody / tr[position() <= 12] / td[2] / text()').extract()
            vetor_tarifas = scgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            dados = scgas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, scgas.nome, "INDUSTRIAL", "TG3", "POSSUI")

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(ScgasSpiderSpider)
    process.start()
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'C:\consulta-tarifas-cdl-gn-brasil\cdl_tarifas\cdl_tarifas\spiders\interfaces')
from envia import envia_dados
from scrapy.crawler import CrawlerProcess
import scrapy
sys.path.insert(1, r'C:\consulta-tarifas-cdl-gn-brasil\cdl_tarifas\cdl_tarifas\spiders')
from empresa import Empresa


class SergasSpider(scrapy.Spider):
    name = 'sergas_spider'
    allowed_domains = ['sergipegas.com.br']
    start_urls = ['https://www.sergipegas.com.br/cms/tarifas']

    def parse(self, response):
        yield scrapy.Request(url='https://www.sergipegas.com.br/cms/tarifas/',
                             callback=self.envia_sergas, priority=1)

    def envia_sergas(self, response):
        sergas = Empresa('SERGAS')
        faixa_auxiliar = '0 a 999.999.999'

        # INDUSTRIAL
        vetor_faixa = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr[position() <= 11]/td[1]/span/text()").extract()
        # Existe um valor de tarifa que está dentro de um tag span, diferente de todos os outros que estão somente dentro de uma tag td,
        valor_span_cimp = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr[8]/td[3]/span/text()").extract()[0]
        valor_span_simp = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr[8]/td[2]/text()").extract()[0]
        vetor_tarifas = response.xpath("//div[contains(@id, 'tab1')]/table/tbody/tr[position() <= 12]/td[position() >= 2]/text()").extract()
        vetor_tarifas.insert(vetor_tarifas.index(valor_span_simp) + 1, valor_span_cimp)  # Tarifa 'valor_span' não foi capturado no response acima mas agora foi adicionado com relacao ao seu anterior.
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "INDUSTRIAL", "NAO POSSUI", "NAO POSSUI")
        # INDUSTRIAL

        # COGERACAO
        vetor_faixa = response.xpath('//*[@id="tab2"]/table/tbody/tr[position() <= 14]/td[1]/text()').extract()
        vetor_tarifas = response.xpath('//*[@id="tab2"]/table/tbody/tr[position() <= 14]/td[position() > 1]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "COGERACAO", "NAO POSSUI", "NAO POSSUI")
        #COGERACAO

        # VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 1]/text()').extract()
        vetor_tarifas.extend(response.xpath('//*[@id="tab3"]/table/tbody/tr/td[position() = 2]/p/text()').extract())
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "VEICULAR", "NAO POSSUI", "NAO POSSUI")
        # VEICULAR

        # RESIDENCIAL
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab4"]/table/tbody/tr/td/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "RESIDENCIAL", "NAO POSSUI", "NAO POSSUI")
        # RESIDENCIAL

        # COMERCIAL
        vetor_faixa = response.xpath('//*[@id="tab5"]/table[1]/tbody/tr/td[1]/span/text()').extract()
        vetor_tarifas = response.xpath('//*[@id="tab5"]/table[1]/tbody/tr/td[position() >= 2]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "COMERCIAL", "NAO POSSUI", "NAO POSSUI")
        # COMERCIAL

        # COMPRIMIDO
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//*[@id="tab6"]/table/tbody/tr/td[position() < 3]/text()').extract()
        dados = sergas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, sergas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
        # COMPRIMIDO

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(SergasSpider)
    process.start()
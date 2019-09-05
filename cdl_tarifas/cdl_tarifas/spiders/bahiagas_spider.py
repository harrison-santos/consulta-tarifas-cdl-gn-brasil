# -*- coding: utf-8 -*-
from envia import envia_dados
import scrapy
from scrapy.crawler import CrawlerProcess
from empresa import Empresa

class BahiagasSpiderSpider(scrapy.Spider):
    name = 'bahiagas_spider'
    allowed_domains = ['bahiagas.com.br']
    start_urls = ['http://www.bahiagas.com.br/']

    def parse(self, response):
        yield scrapy.Request(url='http://clienteonline.bahiagas.com.br/portal/tabela_tarifaria.jsp',
                             callback=self.envia_bahiagas)
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
        #print(dados)
        yield from envia_dados(dados, bahiagas.nome, "INDUSTRIAL", "NAO POSSUI 2", "POSSUI")
        #INDUSTRIAL

        #VEICULAR
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('/html/body/table[2]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, bahiagas.nome, "VEICULAR", "NAO POSSUI", "POSSUI")
        #VEICULAR


        #COMERCIAL
        vetor_faixa = response.xpath('/html/body/table[3]/tr[position() >= 3 and position()<= 15]/td[position() <=2]/div/font/span/text()').extract()
        vetor_faixa[len(vetor_faixa) - 1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('/html/body/table[3]/tr[position() >= 3 and position() <= 15] / td[position() >= 3] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, bahiagas.nome, "COMERCIAL", "NAO POSSUI", "POSSUI")
        #COMERCIAL



        #Geração, Cogeração e Climatização Comercial
        vetor_faixa = response.xpath('//html/body/table[4]/tr[position() >= 3 and position() <= 15]/td[position() <= 2]/div/font/span/text()').extract()
        vetor_faixa[len(vetor_faixa)-1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('//html/body/table[4]/tr[position() >= 3 and position() <= 15]/td[position() >= 3]/div/text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, bahiagas.nome, "COGERACAO", "NAO POSSUI", "POSSUI")
        #Geração, Cogeração e Climatização Comercial


        #COMPRIMIDO
        vetor_faixa = [faixa_auxiliar]
        vetor_tarifas = response.xpath('//html/body/table[6]/tr[3]/td[position() >= 2] / div / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
        yield from envia_dados(dados, bahiagas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
        #COMPRIMIDO

        #RESIDENCIAL
        vetor_faixa = response.xpath('/html/body/table[7]/tr[position() >= 3]/td[position() <= 2] / div / font / span / text()').extract()
        vetor_faixa[len(vetor_faixa) - 1] = faixa_auxiliar_max
        vetor_faixa = bahiagas.organiza_faixa(vetor_faixa)
        vetor_tarifas = response.xpath('/html/body/table[7]/tr[position() >= 3] / td[position() = 4 or position() = 6] / div / text()').extract()
        vetor_parcelas = response.xpath('/html/body/table[7]/tr[position() >=3] / td[position() = 3 or position() = 5] / div / font / span / text()').extract()
        dados = bahiagas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
        yield from envia_dados(dados, bahiagas.nome, "RESIDENCIAL", "NAO POSSUI", "POSSUI")


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(BahiagasSpiderSpider)
    process.start()
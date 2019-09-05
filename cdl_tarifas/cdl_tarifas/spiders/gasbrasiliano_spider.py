# -*- coding: utf-8 -*-
import scrapy
from empresa import Empresa
from envia import envia_dados
from scrapy.crawler import CrawlerProcess

class GasbrasilianoSpiderSpider(scrapy.Spider):
    name = 'gasbrasiliano_spider'
    allowed_domains = ['www.gasbrasiliano.com.br']
    start_urls = ['http://www.gasbrasiliano.com.br/']

    def parse(self, response):
        gasbra_links = [('RESIDENCIAL', 'http://www.gasbrasiliano.com.br/residencial/tarifas/'),
                        ('COMERCIAL', 'http://www.gasbrasiliano.com.br/comercial/tarifas/'),
                        ('VEICULAR', 'http://www.gasbrasiliano.com.br/automotivo/tarifas/'),
                        ('INDUSTRIAL', 'http://www.gasbrasiliano.com.br/industrial/tarifas/')]
        for link in gasbra_links:
            callback = lambda response, l=link[0]: self.envia_gasbrasiliano(response, l)
            yield scrapy.Request(url=link[1], callback=callback)

    def envia_gasbrasiliano(self, response, segmento_):
        self.icms = 15
        self.pis = 1.65
        self.confins = 7.60
        gasbrasiliano = Empresa("GASBRASILIANO")
        def organiza_faixa(vetor_faixa):
            vetor_aux = []
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '')
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
                vetor_faixa[i] = vetor_faixa[i].replace(',', '.')
                aux = vetor_faixa[i].split('a')
                vetor_aux.append(str(int(round(float(aux[0]), 0) + 1)) + ' a ' + aux[1])

            return vetor_faixa
        if segmento_ == "RESIDENCIAL":
            #MEDICAO INDIVIDUAL
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr[position() >= 1] / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1]+' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[4] / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('-', '0')
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, gasbrasiliano.nome, "RESIDENCIAL", "MEDICAO INDIVIDUAL", "POSSUI")
            #MEDICAO INDIVIDUAL

            #MEDICAO COLETIVA
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr[position() >= 1] / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[4] / text()').extract()
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, gasbrasiliano.nome, "RESIDENCIAL", "MEDICAO COLETIVA", "POSSUI")
            #MEDICAO COLETIVA

        elif segmento_ == "COMERCIAL":
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[2] / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('>', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_faixa = organiza_faixa(vetor_faixa)
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[4] / text()').extract()
            vetor_tarifas = gasbrasiliano.calcula_s_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table / tbody / tr / td[3] / text()').extract()
            vetor_parcelas = gasbrasiliano.calcula_s_imposto_parcela(self.icms, self.pis, self.confins, vetor_parcelas)
            dados = gasbrasiliano.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, gasbrasiliano.nome, 'COMERCIAL', 'NAO POSSUI', 'POSSUI')

        elif segmento_ == "INDUSTRIAL":
            #INDUSTRIAL PEQUENO PORTE
            vetor_faixa = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[2] / text()').extract()
            for i in range(len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '').rstrip()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '0 a '+vetor_faixa[0]
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('> ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[1] / tbody / tr / td[4] / text()').extract()
            #removendo imposto pis e confins
            for i in range(0, len(vetor_tarifas)):
                valor_s_impostos = round(float(vetor_tarifas[i].replace(',', '.'))
                                         * ((100 - (self.pis + self.confins)) / 100), 3)
                vetor_tarifas[i] = str(valor_s_impostos).replace('.', ',')

            vetor_tarifas = gasbrasiliano.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            dados = gasbrasiliano.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasbrasiliano.nome, 'INDUSTRIAL', 'PEQUENO PORTE', 'POSSUI')
            #INDUSTRIAL PEQUENO PORTE

            #INDUSTRIAL GRANDE PORTE
            vetor_faixa = response.xpath('//html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[2] / text()').extract()
            for i in range(len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('m³', '').rstrip()
            vetor_faixa[0] = vetor_faixa[0].replace('Até ', '')
            vetor_faixa[0] = '0 a ' + vetor_faixa[0]
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('> ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[1]/section/div[3]/div/div[3] / div / table[2] / tbody / tr / td[4] / text()').extract()
            #removendo imposto pis e confins
            for i in range(0, len(vetor_tarifas)):
                valor_s_impostos = round(float(vetor_tarifas[i].replace(',', '.'))*((100 - (self.pis + self.confins)) / 100), 3)
                vetor_tarifas[i] = str(valor_s_impostos).replace('.', ',')
            vetor_tarifas = gasbrasiliano.calcula_imposto_tarifa(self.icms, self.pis, self.confins, vetor_tarifas)
            dados = gasbrasiliano.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            yield from envia_dados(dados, gasbrasiliano.nome, 'INDUSTRIAL', 'GRANDE PORTE', 'POSSUI')
            #INDUSTRIAL GRANDE PORTE


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(GasbrasilianoSpiderSpider)
    process.start()
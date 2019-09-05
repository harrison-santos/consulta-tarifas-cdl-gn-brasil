# -*- coding: utf-8 -*-
import scrapy
from empresa import Empresa
from envia import envia_dados
from scrapy.crawler import CrawlerProcess

class SulgasSpiderSpider(scrapy.Spider):
    name = 'sulgas_spider'
    allowed_domains = ['www.sulgas.rs.gov.br']
    start_urls = ['http://www.sulgas.rs.gov.br/']

    def parse(self, response):
        sulgas_links = [('INDUSTRIAL', 'http://www.sulgas.rs.gov.br/sulgas/industrial/tabela-de-precos'),
                        ('COMERCIAL', 'http://www.sulgas.rs.gov.br/sulgas/comercial/tabela-de-precos'),
                        ('RESIDENCIAL', 'http://www.sulgas.rs.gov.br/sulgas/residencial/tabela-precos'),
                        ('VEICULAR', 'http://www.sulgas.rs.gov.br/sulgas/veicular/tabela-de-precos')]
        for link in sulgas_links:
            callback = lambda response, l=link[0]: self.envia_sulgas(response, l)
            yield scrapy.Request(url=link[1], callback=callback)

    def envia_sulgas(self, response, segmento_):#
        faixa_auxiliar = ["0 a 999.999.999"]
        sulgas = Empresa("SULGAS")

        self.pis = 1.65
        self.confins = 7.6

        if(segmento_ == "INDUSTRIAL"):
            icms = 12.0 #VERIFICAR VALOR PARA ESSE SEGMENTO
            #INDUSTRIAL FIRME
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa), ):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
                vetor_faixa[i] = vetor_faixa[i].replace('  ', '')

            tarifa_s_impsto = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1 and position() <= 5] / td[2] / p / text()').extract()
            tarifa_s_impsto.extend(response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 5] / td[2] / text()').extract())

            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, tarifa_s_impsto)
            vetor_parcelas = response.xpath('//article/div[2]/table[1]/tbody/tr[position() > 1] / td[3] / p / text()').extract()
            vetor_parcelas.extend(response.xpath('//article/div[2]/table[1]/tbody/tr[position() > 5] / td[3] / text()').extract())
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "FIRME", "POSSUI")
            #INDUSTRIAL FIRME

            #INDUSTRIAL DE PEQUENO PORTE
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[3]/ tbody / tr[2] / td / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[1] / p / text()').extract()
            vetor_faixa[0] = vetor_faixa[0].replace('\xa0', ' ')

            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[2] / p / text()').extract()
            vetor_tarifas[0] = vetor_tarifas[0].replace('\xa0', '')
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[3] / tbody / tr[2] / td[3] / p / text()').extract()
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "PEQUENO PORTE", "POSSUI")
            #INDUSTRIAL DE PEQUENO PORTE

            #INDUSTRIAL INTERRUPTIVEL
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[5]/ tbody / tr / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 1 and position() <= 5] / td[2] / p / text()').extract()
            vetor_tarifas.extend(response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 5] / td[2] / text()').extract())
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[5] / tbody / tr[position() > 1 and position() <= 3] / td[3] / p / text()').extract()
            vetor_parcelas.extend(response.xpath('/html/body/div[3]/article/div[2]/ table[5] / tbody / tr[position() >= 4] / td[3] / text()').extract())
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "INTERRUPTIVEL", "POSSUI")
            #INDUSTRIAL INTERRUPTIVEL

            #COGERAÇÃO PPT
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[1] / p / text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')
            if vetor_faixa[len(vetor_faixa) - 1] == ' ':
                vetor_faixa.pop()

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[7] / tbody / tr[position() > 1] / td[3] / text()').extract()
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, "COGERACAO", "PPT", "POSSUI")
            #COGERAÇÃO PPT

            # COGERAÇÃO, CLIMATIZACAO E GERAÇÃO HORARIO PONTA
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[1] / p / span / text()').extract()
            vetor_faixa.extend(response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[1] / p / text()').extract())
            vetor_faixa[0] = vetor_faixa[0].replace('\xa0', ' ')
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)

            #ABAIXO ESTÁ SENDO FEITO A SOMA DE MMBTU E PARCELA FIXA DEFINIDA PARA O VALOR DE PARCELA FIXA
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            vetor_parcelas[2] = vetor_parcelas[2].replace(',00', '')
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms,self.pis,self.confins,vetor_parcelas)
            tam = len(vetor_parcelas)
            vetor_parcelas[tam-1] = vetor_parcelas[tam-1].replace(',', '')#C IMPOSTO
            vetor_parcelas[tam - 2] = vetor_parcelas[tam - 2].replace(',', '')#S IMPOSTO
            vetor_mmbtu = response.xpath('/html/body/div[3]/article/div[2]/table[9] / tbody / tr[position() > 1] / td[4] / p / text()').extract()
            vetor_mmbtu.insert(1, response.xpath('/html/body/div[3]/article/div[2]/ table[9] / tbody / tr[3] / td[4] / text()').extract()[0])
            vetor_mmbtu = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_mmbtu)
            vetor_parcelas = sulgas.soma_listas(vetor_parcelas, vetor_mmbtu)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            #CAPTURA ABAIXO yield from self.envia_dados(dados, sulgas.nome, segmento_, "COGERACAO, CLIMATIZACAO E GERAÇAO HORARIO PONTA", "POSSUI")
            yield from envia_dados(dados, sulgas.nome, "COGERACAO", "HORARIO PONTA", "POSSUI")#MESMOS VALORES PARA COMERCIAl
            #COGERAÇÃO, CLIMATIZACAO E GERAÇÃO HORARIO PONTA

            #INDUSTRIAL COMPRIMIDO
            vetor_faixa = faixa_auxiliar
            consulta = response.xpath('/html/body/div[3]/article/div[2]/table[11]/tbody/tr[2]/td[position() > 1]/p/text()').extract()#posicao1 tarifa, posicao2 mmbtu
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, [consulta[0]])
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, [consulta[1]])
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, "COMPRIMIDO", "NAO POSSUI", "POSSUI")
            #INDUSTRIAL COMPRIMIDO

        elif segmento_ == "COMERCIAL":
            icms = 12.0
            #COMERCIAL
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1]/tbody / tr[position() > 1] / td[1] / p / text()').extract()
            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')

            vetor_parcelas = sulgas.calcula_s_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")
            #COMERCIAL

        elif(segmento_ == "RESIDENCIAL"):
            icms = 12.0
            vetor_faixa = response.xpath('/html/body/div[3]/article/div[2]/table[1]/tbody/tr[position() > 1]/td[1]/p/text()').extract()
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('\xa0', ' ')

            tam = len(vetor_faixa)
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1].replace('Acima de ', '').replace('acima de ', '')
            vetor_faixa[tam - 1] = vetor_faixa[tam - 1] + ' a 999.999.999'
            vetor_tarifas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[3] / p / text()').extract()
            vetor_tarifas.append(response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[8] / td[3] / text()').extract()[0])
            vetor_tarifas = sulgas.calcula_s_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[position() > 1] / td[2] / p / text()').extract()
            for i in range(0, len(vetor_parcelas)):
                vetor_parcelas[i] = vetor_parcelas[i].replace('.', '')
            vetor_parcelas = sulgas.calcula_s_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)

            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")

        elif(segmento_ == "VEICULAR"):
            icms = 12.0#VERIFICAR VALOR ICMS
            #VEICULAR
            vetor_faixa = faixa_auxiliar
            vetor_auxiliar = response.xpath('/html/body/div[3]/article/div[2]/table[1] / tbody / tr[2] / td[position() > 1] / text()').extract()
            vetor_tarifas = [vetor_auxiliar[0].replace('\xa0', ' ')]
            vetor_tarifas = sulgas.calcula_imposto_tarifa(icms, self.pis, self.confins, vetor_tarifas)
            vetor_parcelas = [vetor_auxiliar[1].replace('\xa0', ' ')]
            vetor_parcelas = sulgas.calcula_imposto_parcela(icms, self.pis, self.confins, vetor_parcelas)
            dados = sulgas.organiza_faixa_tarifas_parcelas(vetor_faixa, vetor_tarifas, vetor_parcelas)
            yield from envia_dados(dados, sulgas.nome, segmento_, "NAO POSSUI", "POSSUI")
            #VEICULAR




if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(SulgasSpiderSpider)
    process.start()

# -*- coding: utf-8 -*-
import scrapy
import bs4
import urllib
from modulos.empresa import Empresa
from modulos.envia import envia_dados
from scrapy.crawler import CrawlerProcess

class CompagasSpiderSpider(scrapy.Spider):
    name = 'compagas_spider'
    allowed_domains = ['compagas.com.br']
    start_urls = ['http://www.compagas.com.br/']

    def parse(self, response):
        yield from self.envia_compagas()

    def envia_compagas(self):
        faixa_auxiliar = "0 a 999.999.999"
        compagas = Empresa("COMPAGAS")
        links = [
            ("COMERCIAL", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=2"),
            ("INDUSTRIAL", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=1"),
            ("RESIDENCIAL", "MEDICAO COLETIVA",
             "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=17"),
            ("RESIDENCIAL", "MEDICAO INDIVIDUAL",
             "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=4"),
            ("VEICULAR", "NAO POSSUI", "http://agv.compagas.com.br/index.php?action=uiprecos.index&segmento=3")
            ]
        for link in links:
            segmento = link[0]
            subsegmento = link[1]
            url = link[2]


            s = urllib.request.urlopen(url)#COMANDO CHAVE
            soup = s.read().decode('ISO-8859-1')
            soup = soup.replace("</fo<td>", "</td>")
            #print(soup)
            soup = bs4.BeautifulSoup(soup, "html.parser") #raw text para html
            #print(soup)
            table = soup.find('table', attrs={'class': 'data'})
            #print(table)
            total = len(table.findAll("tr"))
            #print(total)
            row_count = 0
            vetor_faixa = []
            vetor_tarifas = []
            for row in table.findAll("tr"):
                td_count = 0
                if (row_count >= 2) and (row_count <= (total - 2)):
                    dados = ' '
                    for cell in row("td"):
                        valor = cell.get_text().strip()
                        if td_count <= 1:  # 0 1 2 3 = 4
                            vetor_faixa.append(valor)

                        elif td_count == 2 or td_count == 3:
                            vetor_tarifas.append(valor)

                        td_count += 1
                    #linha = str(dados)
                    #print(linha)
                row_count += 1
            for i in range(0, len(vetor_faixa)):
                vetor_faixa[i] = vetor_faixa[i].replace('.', '')
                if (i != 0) and (i % 2 == 0):
                    vetor_faixa[i] = str(int(vetor_faixa[i]) + 1)

            for i in range(0, len(vetor_faixa) - 1):
                vetor_faixa[i] = str(vetor_faixa[i])

            vetor_faixa = compagas.organiza_faixa(vetor_faixa)
            dados = compagas.organiza_faixa_tarifas(vetor_faixa, vetor_tarifas)
            #print("FX: {}".format(vetor_faixa))
            #print("TRFA: {} Tamanho: {}".format(vetor_tarifas, len(vetor_tarifas)))
            yield from envia_dados(dados, compagas.nome, segmento, subsegmento, "NAO POSSUI")


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(CompagasSpiderSpider)
    process.start()
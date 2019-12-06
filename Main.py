import algas_spider
import bahiagas_spider
import cegas_spider
import comgas_spider
import compagas_spider
import copergas_spider
import gasbrasiliano_spider
import gasmig_spider
import pbgas_spider
import potigas_spider
import scgas_spider
import sergas_spider
import sulgas_spider
import csv

from scrapy.crawler import CrawlerProcess
from cdl_screenshots import cdls_screenshots

if __name__ == "__main__":

    fieldnames = ["DTA_CST", "COD_CDL", "NME_SEG", "NME_SBSEG", "FXA_INI", "FXA_FIM", "FXA_UNI",
                  "FXA_IGUAL",
                  "TAR_SIM", "VOL_FXA", "VOL_ACU", "FAT_FXA", "FAT_ACU", "TAR_MED"]

    with open('C:\consulta-tarifas-cdl-gn-brasil\dados_teste.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fieldnames)

    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

    """
    print("Informe quais dados deseja capturar::")
    opcao = input(" 1-Algas \n 2-Bahiagas \n 3-Cegas \n 4-Comgas \n 5-Compagas \n 6-Copergas \n 7-Copergas \n 8-Gasbrasilliano \n 9-Gasmig \n 10-Pbgas "
          "\n 11-Potigas \n 12 -Scgas \n 13-Sergas \n 14-Sulgas \n 0-Todos")"""

   # print(type(opcao))
    """
    process.crawl(algas_spider.AlgasSpiderSpider)
    
    process.crawl(cegas_spider.CegasSpiderSpider)

    process.crawl(comgas_spider.ComgasSpiderSpider)
    process.crawl(compagas_spider.CompagasSpiderSpider)
    process.crawl(copergas_spider.CopergasSpiderSpider)
    process.crawl(gasbrasiliano_spider.GasbrasilianoSpiderSpider)
    process.crawl(gasmig_spider.GasmigSpiderSpider)
    process.crawl(pbgas_spider.PbgasSpiderSpider)
    process.crawl(potigas_spider.PotigasSpiderSpider)
    process.crawl(scgas_spider.ScgasSpiderSpider)
    process.crawl(sergas_spider.SergasSpider)
    process.crawl(sulgas_spider.SulgasSpiderSpider)

    process.crawl(bahiagas_spider.BahiagasSpiderSpider)
    process.start()"""
    cdls_screenshots.captura()
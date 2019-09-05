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

from scrapy.crawler import CrawlerProcess
#from cdl_screenshots import cdls_screenshots

if __name__ == "__main__":
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
    process.crawl(algas_spider.AlgasSpiderSpider)
    #process.crawl(bahiagas_spider.BahiagasSpiderSpider)
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
    process.start()
    #cdls_screenshots.captura()
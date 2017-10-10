# encoding: utf-8

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ConsCscrap.items import listCCitem

class CCspider(CrawlSpider):
    name = 'CC_main'
    handle_httpstatus_list = [404, 301]
    
    # Page du Cons. Constit. qui renvoie, pour chaque année, à toutes les décisions prises
    start_urls = ['http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/les-decisions-par-date.4614.html']
    
    rules = (Rule(LxmlLinkExtractor(allow=(), restrict_xpaths="//div[@id='articlesArchives']"),
                  callback="parse_annee", follow=True),)
    
    def parse_annee(self, response):
        decisions = response.selector.xpath("//li[@class='ld']")
        for el in decisions:
            item = listCCitem()
            item['dd'] = el.xpath('./a/text()').extract()[0].split()[0]
            item['mm'] = el.xpath('./a/text()').extract()[0].split()[1]
            item['yy'] = el.xpath('./a/text()').extract()[0].split()[2]
            item['num_dc'] = el.xpath('./a/text()').extract()[0].split()[6]
            item['type_dc'] = el.xpath('./a/text()').extract()[0].split()[7]
            item['sol_dc'] = ''.join(re.findall('[^\[].*(?<!\])', el.xpath("./em/small/text()").extract()[0]))
            item['objet_dc'] = el.xpath("./em/text()").extract()[0].rstrip()
            item['publi_dc'] = el.xpath("./em/em/text()").extract()[0]
            item['link_dc'] = "http://www.conseil-constitutionnel.fr"+el.xpath('./a/@href').extract()[0]

            yield Request(item['link_dc'], meta={'item':item}, callback=self.parse_decision)

    def parse_decision(self, response):
        decision = response.selector.xpath("//div[@id='mainContent']")
        for el in decision:
            item = response.request.meta['item']
            item['ecli_dc'] = el.xpath("./div[@id='ecli']/text()").extract()[0].rstrip().replace(' ', '')
            pres_dc = el.xpath("./a[@id='information_seance']/following-sibling::p/text()").extract()[0].rstrip()
            # Pour recenser les membres qui ont pris une décision on utilise le regex : 
            reg = "(Georges VEDEL|Louis JOXE|Robert LECOURT|Francis MOLLET-VI\xc9VILLE|L\xe9on JOZEAU-MARIGN\xc9|Daniel MAYER|Robert FABRE|Robert BADINTER|Jacques LATSCHA|Maurice FAURE|Jean CABANNES|Noelle Lenoir|Jacques ROBERT|Georges ABADIE|Marcel RUDLOFF|No\xeblle LENOIR|Roland DUMAS|Val\xe9ry GISCARD d'ESTAING|Etienne Dailly|Michel AMELLER|Alain LANCELOT|Yves GU\xc9NA|Pierre MAZEAUD|Simone VEIL|Jean-Claude COLLIARD|Monique PELLETIER|Olivier DUTHEILLET de LAMOTHE|Dominique SCHNAPPER|Pierre JOXE|Jean-Louis PEZANT|Jacqueline de GUILLENCHMIDT|Pierre STEINMETZ|Jacques BARROT|Hubert HAENEL|Jean-Louis DEBR\xc9|Guy CANIVET|Renaud DENOIX de SAINT MARC|Jacques CHIRAC|Michel CHARASSE|Claire BAZY MALAURIE|Nicolas SARKOZY|Nicole MAESTRACCI|Nicole BELLOUBET|Lionel JOSPIN|Jean-Jacques HYEST|Laurent FABIUS|Corinne LUQUIENS|Michel PINAULT)"
            item['membres'] = re.findall(str(reg), pres_dc)

yield item

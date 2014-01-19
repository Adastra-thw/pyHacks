#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Adastra

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

class Torrent(Item):
    url = Field()
    tipo = Field()
    torrentLink = Field()
    size = Field()
    description = Field()

class PirateBaySpider(CrawlSpider):

    name = 'thepiratebay.sx'
    allowed_domains = ['thepiratebay.sx']
    start_urls = ['http://thepiratebay.sx/browse']
    rules = [Rule(SgmlLinkExtractor(allow=['/\d+']), 'parse_torrent')]

    def parse_torrent(self, response):
        x = HtmlXPathSelector(response)
        torrent = Torrent()
        torrent['url'] = response.url
        torrent['tipo'] = x.select('//*[@id="searchResult"]/tr[1]/td[1]/center/a[2]//text()').extract()
	torrent['torrentLink'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/a[2]/@href').extract()
        torrent['description'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/div/a/@title').extract()
        torrent['size'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/font/text()[2]').extract()
        return torrent

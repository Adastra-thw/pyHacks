#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Adastra

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

class HackerWayItem(Item):
	title = Field()
	author =  Field()
	tag = Field()
	date = Field()


class BloggerSpider(CrawlSpider):
	name="TheHackerWay"
	start_urls=['http://thehackerway.com']
	# urls desde las cuales el spider comenzará el proceso de crawling
    	rules = [Rule(SgmlLinkExtractor(allow=[r'/\d{4}']), follow=True, callback='parse_blog'), 
    		# r'/\d+' : expression regular para http://thehackerway.com/X URLs
	    	Rule(SgmlLinkExtractor(allow=[r'\d{4}/\d{2}\d{2}/\w+']), callback='parse_blog')]
    		# http://thehackerway.com/YYYY/MM/DD/titulo URLs

	def parse_blog(self, response):
		print 'link parseado %s' %response.url
		hxs = HtmlXPathSelector(response)
		item = HackerWayItem()
		item['title'] = hxs.select('//title/text()').extract() # Selector XPath para el titulo
		item['author'] = hxs.select("//span[@class='author']/a/text()").extract() # Selector XPath para el author
		item['tag'] = hxs.select("//meta[@property='og:title']/text()").extract() # Selector XPath para el tag
		item['date'] = hxs.select("//span[@class='date']/text()").extract() # Selector XPath para la fecha
		return item # Retornando el Item.

def main():
	"""Rutina principal para la ejecución del Spider"""
	# set up signal to catch items scraped
	from scrapy import signals
	from scrapy.xlib.pydispatch import dispatcher

	def catch_item(sender, item, **kwargs):
		print "Item Extraido:", item
	dispatcher.connect(catch_item, signal=signals.item_passed)

	from scrapy.conf import settings
	settings.overrides['LOG_ENABLED'] = False

	# setup crawler
	from scrapy.crawler import CrawlerProcess

	crawler = CrawlerProcess(settings)
	crawler.install()
	crawler.configure()

	# definir el spider para el crawler
	crawler.crawl(BloggerSpider())

	# iniciar scrapy
	print "STARTING ENGINE"
	crawler.start()
	print "ENGINE STOPPED"

if __name__ == '__main__':
	main()

# -*- coding: utf-8 -*-
import scrapy


class VivaSpider(scrapy.Spider):
    name = 'viva'
    allowed_domains = ['www.vivareal.com.br/']
    start_urls = ['https://www.vivareal.com.br/aluguel/parana/curitiba/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['pe.olx.com.br']
    start_urls = [
        'https://pe.olx.com.br/imoveis/aluguel'
    ]

    def parse(self, response):
        # r.db('scrapy_olx').table('items').delete();
        items = response.xpath(
            '//div[contains(@class,"section_OLXad-list")]//li[contains'
            '(@class,"item")]'
        )
        for item in items:
            url = item.xpath(
                ".//a[contains(@class,'OLXad-list-link')]/@href"
            ).extract_first()
            if url:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()
        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

#sc-bZQynM sc-45jt43-0 bJcANz
    def parse_detail(self, response):
        # self.log(u'Imóvel URL: {0}'.format(response.url))
        item = dict()
        item['photos'] = response.xpath(
            '//div[contains(@data-testid,"slides-wrapper")]//img/@src'
        ).extract()
        item['url'] = response.url
        item['address'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-location")]'
            '//.)'
        ).extract_first()
        item['title'] = response.xpath(
            'normalize-space(//h2[contains(@class,"OLXad-list-title")]//.)'
        ).extract_first()
        item['price'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-price")]'
            '//span[contains(@class,"actual-price")]//.)'
        ).extract_first()
        item['details'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-description")]'
            '//.)'
        ).extract_first()
        item['source_id'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-id")]//strong//.)'
        ).extract_first()
        date = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-date")]//.)'
        ).re("Inserido em: (.*).")
        item['date'] = (date and date[0]) or ''
        yield item

import scrapy
from scrapy.http import HtmlResponse
from ads_parser.items import AdsParserItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['https://leroymerlin.ru/search/?q=обои&family=7f8ab360-4691-11ea-b7ce-8d83641e7e8e&suggest=true']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}/']




    def parse(self, response:HtmlResponse):
        links = response.xpath("//div[@data-cy='l-card']/a")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse(self, response):
        next_page_path = 'a[aria-label*="Следующая страница"]::attr(href)'
        next_page_link = response.css(next_page_path).extract_first()
        next_page_full_link = f'https://leroymerlin.ru{next_page_link}'

        yield response.follow(next_page_full_link, callback=self.parse)


        product_links_path = '//*/div[@class="phytpj4_plp largeCard"]/a/@href'
        product_links = response.xpath(product_links_path).extract()
        for product_link in product_links:
            product_full_link = f'https://leroymerlin.ru{product_link}'
            yield response.follow(product_full_link, callback=self.parse_product)

    def parse_product(self, response):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_value('link', response.url)
        loader.add_css('name', 'h1[slot=title]::text')
        loader.add_xpath('parameter_name', "//dt/text()")
        loader.add_xpath('parameter_value', "//dd/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_xpath('images', '//source[contains(@media, "only screen and (min-width: 768px)")]/@srcset')
        yield loader.load_item()

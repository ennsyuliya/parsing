import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,' f-test-link-Dalshe')]/@href").get()
        job_links = response.xpath("//a[contains(@class, '_1IHWd f-test-link)]/@href").getall()
        for link in job_links:
            link = link.split('?')[0]
            yield response.follow(link, callback=self.vacansy_parce)

        yield response.follow(next_page, callback=self.parse)


    def vacansy_parce(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='2eYAG _3xCPT rygxv _17lam _3GtUQ']/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, link=link, url=url)

import scrapy

def kamien(response):
    if response == None:
        return "Nie dotyczy"
    return response.split('\n')[2].strip()

def proba(response):
    if response == None:
        return "Nie dotyczy"
    return response.split('\n')[2].strip()
        



class ApartSpider(scrapy.Spider):
    name = 'apart'
    start_urls = ['https://www.apart.pl/bizuteria/chokery']

    def parse(self, response):
        for url in response.css('.product-name a::attr(href)').getall():
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        yield {
        "Nazwa": response.css('.section.title > h1::text').get(),
        "Nr wzoru": response.css('.section.title > span::text').get().split(':')[1].strip(),
        "Cena (PLN)": response.css('span.price > span.value::text').get(),
        "Marka": response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Marka:')]/a/text()").get(),
        "Kolekcja": response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Kolekcja:')]/a/text()").get(),
        "Kamień": kamien(response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Kamień:')]/text()").get()),
        "Surowiec": response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Surowiec:')]/text()").get().split(':')[1].strip(),
        "Próba": proba(response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Próba:')]/text()").get()),
        # "Materiał dodatkowy": response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Materiał dodatkowy:')]/text()").get().split(':')[1].strip(),
        # "Szerokość": response.xpath("//div[@class='col-xs-24']/p[contains(text(), 'Szerokość:')]/text()").get().split(':')[1].strip()
        }

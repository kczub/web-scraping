import scrapy


class Giants2Spider(scrapy.Spider):
    name = 'giants2'
    start_urls = ['https://wearelittlegiants.com/home/shop/']

    def parse(self, response):
        for url in response.css('div.category_grid_box a::attr(href)').getall():
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        for url in response.css('h2.woocommerce-loop-product__title > a::attr(href)').getall():
            yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_category)

    def parse_item(self, response):
        yield {
            "category": response.css(".product_meta a[rel='tag']::text").get(),
            "name": response.css('h1.product_title.entry-title::text').get(),
            "price": response.css('p.price bdi::text').get(),
            "sku": response.css('.product_meta span.sku::text').get(),
            "description": response.css('#tab-description p::text').getall(),
            "additional info": response.css('#tab-additional_information td::text').getall()
        }

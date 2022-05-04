import scrapy


class ProductsSpider(scrapy.Spider):
    name = "notebook_spider"

    def start_requests(self):
        url = "https://ordi.eu/sulearvutid?___store=en&___from_store=et"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get list of products from <li> tags
        for product in response.css('li.item'):
            yield {
                # Name of product in <h2><a> tags
                'Product name': product.css('h2.product-name a::text').get(),
                # Price of product in <span> tags
                'Product price': product.css('span.price::text').get(),
                # Product image ref from <img> tags
                'Product image': product.css('a.product-image img::attr(src)').get(),
            }
        # Get next page button 
        next_page = response.css('div.pages ol li a.next::attr(href)').get()
        # If the next button exists
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
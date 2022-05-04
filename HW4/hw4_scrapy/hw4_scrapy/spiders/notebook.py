import scrapy

# Run command:
# scrapy crawl products -o [output-file]


class ProductsSpider(scrapy.Spider):
    # Name of the spider
    name = "test"

    # Request are made to the url with this function
    # Code partially taken from official documentation of Scrapy.
    def start_requests(self):
        url = "https://ordi.eu/lauaarvutid#"
        yield scrapy.Request(url=url, callback=self.parse)

    # Determines how the information will be parsed and in which section
    def parse(self, response):
        for product in response.css('li.item'):
            # Creates a dictionary with the related information
            yield {
                'Product name': product.css('h2.product-name a::text').get(),
                'Product price': product.css('span.price::text').get(),
                'Product image': product.css('a.product-image img::attr(src)').get(),
            }
        # Follow next page links
        next_page = response.css('div.pages ol li a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
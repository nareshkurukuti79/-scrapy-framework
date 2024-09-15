# /* chocolatespider.py file created manually */


from urllib.parse import urlencode
import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader

# https://scrapeops.io/app/login
API_KEY = '021f52e4-c875-4349-a468-57feccd34b8c'

def get_proxy_url(url):
    payload = { 'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?'+urlencode(payload)
    return proxy_url

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk", "proxy.scrapeops.io"]
    # start_urls = ["https://chocolate.co.uk"]
    # start_urls = ["https://www.chocolate.co.uk/collections/all"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'chocolatescraper.pipelines.PriceToUSDPipeline': 100,
            'chocolatescraper.pipelines.DuplicatesPipeLilne': 200,
            'chocolatescraper.pipelines.SavingToMysqlPipeline': 300,
            'chocolatescraper.pipelines.SavingToPostgresPipeline': 400,
        },
        'ROBOTSTXT_OBEY': True,  # Ignore robots.txt rules
    }

    def start_requests(self):
        start_urls = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(url=get_proxy_url(start_urls), callback=self.parse)

    def parse(self, response):

        products = response.css('product-item')

        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            chocolate.add_css('price','span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            
            yield chocolate.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page

            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)
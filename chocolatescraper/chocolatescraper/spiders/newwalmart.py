import json
import math
import scrapy
import logging
from urllib.parse import urlencode

API_KEY = '021f52e4-c875-4349-a468-57feccd34b8c'

def get_proxy_url(url):
    payload = { 'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?'+urlencode(payload)
    # print('proxy_url')
    # print(proxy_url)
    return proxy_url

class WalmartSpider(scrapy.Spider):
    name = "newwalmart"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}},
        'ROBOTSTXT_OBEY': False,  # Ignore robots.txt rules
    }

    def start_requests(self):
        sitemap_url = 'https://www.walmart.com/sitemap_category.xml'
        self.log(f"Starting to scrape sitemap: {sitemap_url}", level=logging.INFO)
        yield scrapy.Request(url=get_proxy_url(sitemap_url), callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        self.log(f"Parsing sitemap: {response.url}", level=logging.INFO)
        # category_urls = response.xpath('//url/loc/text()').getall()
        # Define the namespace
        namespaces = {
            'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        }
        
        # Use the namespace in the XPath expression
        # category_urls = response.xpath('//ns:url/ns:loc/text()', namespaces=namespaces).getall()
        # category_urls = response.xpath('//ns:url/ns:loc/text()', namespaces=namespaces).get()
        category_urls = ['https://www.walmart.com/cp/additional-garage-equipment/4066622']

        self.log(f"Found {len(category_urls)} categories in sitemap", level=logging.INFO)
        for url in category_urls:
            self.log(f"Scraping category page: {url}", level=logging.DEBUG)
            yield scrapy.Request(url=get_proxy_url(url), callback=self.parse_category_page, meta={'category_url': url, 'page': 1})

    def parse_category_page(self, response):
        category_url = response.meta['category_url']
        page = response.meta['page']
        self.log(f"Scraping category: {category_url}, page: {page}", level=logging.INFO)
        
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        if script_tag is not None:
            json_blob = json.loads(script_tag)
            self.log(f"Extracted JSON data from category page: {category_url}, page: {page}", level=logging.DEBUG)

            ## Request Product Page
            product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
            self.log(f"Found {len(product_list)} products on category page: {category_url}, page: {page}", level=logging.INFO)
            for idx, product in enumerate(product_list):
                walmart_product_url = 'https://www.walmart.com' + product.get('canonicalUrl', '').split('?')[0]
                self.log(f"Scraping product: {walmart_product_url}", level=logging.DEBUG)
                yield scrapy.Request(url=get_proxy_url(walmart_product_url), callback=self.parse_product_data, meta={'category_url': category_url, 'page': page, 'position': idx + 1})

            ## Request Next Page
            if page == 1:
                total_product_count = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["count"]
                max_pages = math.ceil(total_product_count / 40)
                self.log(f"Total products: {total_product_count}, calculated max pages: {max_pages} for category: {category_url}", level=logging.INFO)
                if max_pages > 5:
                    max_pages = 5
                    self.log(f"Limiting max pages to 5 for category: {category_url}", level=logging.INFO)
                for p in range(2, max_pages + 1):
                    category_page_url = f"{category_url}?page={p}"
                    self.log(f"Scraping category page: {category_page_url}", level=logging.DEBUG)
                    yield scrapy.Request(url=get_proxy_url(category_page_url), callback=self.parse_category_page, meta={'category_url': category_url, 'page': p})

    def parse_product_data(self, response):
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)
            raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
            self.log(f"Extracted product data: {raw_product_data.get('id')} from {response.url}", level=logging.DEBUG)
            yield {
                'category_url': response.meta['category_url'],
                'page': response.meta['page'],
                'position': response.meta['position'],
                'id': raw_product_data.get('id'),
                'type': raw_product_data.get('type'),
                'name': raw_product_data.get('name'),
                'brand': raw_product_data.get('brand'),
                'averageRating': raw_product_data.get('averageRating'),
                'manufacturerName': raw_product_data.get('manufacturerName'),
                'shortDescription': raw_product_data.get('shortDescription'),
                'thumbnailUrl': raw_product_data['imageInfo'].get('thumbnailUrl'),
                'price': raw_product_data['priceInfo']['currentPrice'].get('price'),
                'currencyUnit': raw_product_data['priceInfo']['currentPrice'].get('currencyUnit'),
            }

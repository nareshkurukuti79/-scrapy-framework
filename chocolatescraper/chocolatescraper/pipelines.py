# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import psycopg2

# useful for handling different item types with a single interface
from sqlite3 import adapters
from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.exceptions import DropItem

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        if adapter.get('price'):

            floatPrice = float(adapter['price'])

            adapter['price'] = floatPrice*self.gbpToUsdRate
            
            return item
        else: 
            raise DropItem(f"Missing price in {item}")
        

class DuplicatesPipeLilne:

    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.name_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.name_seen.add(adapter['name'])
            return item
        

class SavingToMysqlPipeline(object):

    def __init__(self):
        self.create_connection()

    
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'chocolate_scraping',
            port = '3306',
        )

        self.curr = self.connection.cursor()
        self.curr.execute("TRUNCATE TABLE chocolate_products")
        self.connection.commit()
    
    def process_item(self, item, spider):
        self.store_db(item)

        return item
    
    def store_db(self, item):        
        self.curr.execute("""
            INSERT INTO chocolate_products (name, price, url) 
            VALUES (%s, %s, %s)
        """, (
            item['name'],
            item['price'],
            item['url']
        ))
        self.connection.commit()


class SavingToPostgresPipeline(object):

    def __init__(self):
        self.create_connection()

    
    def create_connection(self):
        self.connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = 'postgres',
            database = 'chocolate_scraping',
        )

        self.curr = self.connection.cursor()
        self.curr.execute("TRUNCATE TABLE chocolate_products")
        self.connection.commit()
    
    def process_item(self, item, spider):
        self.store_db(item)

        return item
    
    def store_db(self, item): 

        try:
            self.curr.execute("""
                        INSERT INTO chocolate_products (name, price, url) 
                        VALUES (%s, %s, %s)
                    """, (
                        item['name'],
                        item['price'],
                        item['url']
                    ))
        except BaseException as e:
            print(e)
        
        self.connection.commit()
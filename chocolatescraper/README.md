Part - 1 Python Scrapy Begginer Series
-------------------------------------
pipenv install scrapy

pipenv shell

scrapy startproject chocolatescraper

cd .\chocolatescraper\

scrapy genspider chocolatespider chocolate.co.uk

scrapy list

/*To run scrapy shell to check crawling output*/
scrapy shell

/*It will fetch the all html content*/
fetch('https://www.chocolate.co.uk/collections/all')

/*It will fetch the all products*/
response.css('product-item')

/*It will fetch the first product item*/
response.css('product-item').get()

/*Assigning all products items to the products variable*/
products = response.css('product-item')

/*Assinging 1st product item to single variable*/
product = products[0]

/*To get product title*/
product.css('a.product-item-meta__title::text').get()

/*To get Product price*/
product.css('span.price').get()

product.css('span.price').get().replace('<span class="price"><span class="visually-hidden">Sale price','')

product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price',''). replace('</span>','')

/*To get product href link*/
product.css('div.product-item-meta a').get()

product.css('div.product-item-meta a::attr(href)').get()

/*To run the 'chocolatespider' code and crawling the content and store in the json file*/
scrapy crawl chocolatespider -O mydata.json
- here small letter o append the data in the mydata.json file
- here capital letter O append the data in the mydata.json file

/*To run the 'chocolatespider' code and crawling the contetn and store in the csv file*/
scrapy crawl chocolatespider -O mydata.csv
- here small letter o append the data in the mydata.csv file
- here capital letter O append the data in the mydata.csv file


Part-2: Scrapy Beginner Series Fixing Dirty Data & Edge Cases
--------------------------------------------------------------
1. Strategies to Deal with Edge Cases
2. Organizing Our Data With Scrapy Items
3. Pre Processing Data with Scrapy Item Loaders
4. Processing Our Data with Scrapy Item Pipelines

Part-3: Python Scrapy - Beginner Series
----------------------------------------
1. Using The Scrapy Feed Exporters
2. Saving Data to Amazon S3 Storage
3. Saving Data to MySQL and PostgresSQL Databases

pipenv install botocore 

scrapy crawl chocolatespider -O s3://aws_key:aws_secret@mybucket/path/to/myscrapedata.csv:csv

pipenv install mysql

pipenv install mysql-connector-python

pipenv install psycopg2

scrapy crawl chocolatespider 

Part-4: Scrapy Beginner Series - Bypassing Restrictions
------------------------------------------------------
1. Getting Blocked & Banner when web scraping
2. Using User Agent when scraping
3. Using Proxies to Bypass Anti-bots and CAPTCHA's
4. Difference Between Feed & Paid Proxies

pipenv install scrapy-user-agents

scrapy crawl chocolatespider 

[scrapeops.io/proxy-providers/comparsion/](https://scrapeops.io/proxy-providers/comparison/
Need to Login:
username: naresh@altnsoulutions.co.uk
password: DIP

How to Schedule Scrapy Spiders with Scrapyd & ScrapeOps
---------------------------------------------------------
https://github.com/ScrapeOps/Scrapeops-scrapy-demo

We have to create server in the digital ocean

pipenv install scrapy

pipenv install scrapyd

Deploy & Run Your Scrapy Spiders On AWS Server Using ScrapeOps
-----------------------------------------------------------------

Schedule & Run Scrapy Spiders On Digital Ocean Droplet With ScrapeOps
-----------------------------------------------------------------------



This is for learning:
---------------------
https://scrapeops.io/python-scrapy-playbook/


Python Scrapy - How to scrape walmart:
---------------------------------------
1. Basics of scraping data on walmart
2. Setting up our proxy
3. Crawling for a specific search term
4. Parsing the search results
5. Parsing the product data

Basic-scrapy-project:
https://github.com/python-scrapy-playbook/basic-scrapy-project

walmart-python-scrapy-scraper
https://github.com/python-scrapy-playbook/walmart-python-scrapy-scraper
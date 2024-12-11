#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

import random
import re


# In[3]:


# pipelines 
# The way pipelines works: 
# a yield dict from spider come here, if_else condition checks the desired key,
# and apply the cleaning functionn on it

class DataCleansingPipeline:
    def process_item(self, item, spider):
        if 'num_page' in item:
            item['num_page'] = self.clean_num_pages(''.join(item['num_page']))
        return item

    def clean_num_pages(self, text):
        match  = re.search('\d+\sPages', text)
        if match:
            cleaned_text =  match.group()
        else:
            cleaned_text = 'not mentioned'
        return cleaned_text


# In[4]:


# This spider using the CrawlSpider class, do the scrapping of all pages of a popular category 
# and it extract the links of all books and parse it into parse_item for extraction
# another Rule is defined for pagnition

class PDFdriveCrawler(CrawlSpider):
    name='books-data-crawler'
    allowed_domains = ['pdfdrive.to']
    start_urls = ['https://pdfdrive.to/categories/popular']
    
    rule_books_link = Rule(LinkExtractor(restrict_css='a.title-link'), callback = 'parse_item', follow = False)
    rule_pagnition = Rule(LinkExtractor(restrict_xpaths="//span[@class='jsx-d375c0faf73020ef arrow-right']/.."), follow=True)
    rules = (rule_books_link, rule_pagnition, )
    

    def parse_item(self, response):
        yield{
        'book_name' : response.css('div h1::text').get(),
        'author_name' : response.xpath('//a[starts-with(@href, "/author/")]/text()').get(),
        'num_page' : response.css("div[class='jsx-7d4e960818f559df file-info'] span::text").getall(),
        'download_url' : response.url,
        'book_image' : response.css("div.container img[title='ebook img']::attr(src)").get(),
        }


# In[ ]:


process = CrawlerProcess({
    
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    'FEED_FORMAT' : 'csv',
    'FEED_URI' : 'pdfdrive.csv',
    # 'DOWNLOAD_DELAY' : random.uniform(3.0, 5.0),
    'ITEM_PIPELINES': {'__main__.DataCleansingPipeline': 1}, # define for pipeline configuration
    'AUTOTHROTTLE_ENABLED' : True, #  This enable Auto Throttle extesnion, and it is pretty awesome.
    'AUTOTHROTTLE_START_DELAY' : 5.0,
    'AUTOTHROTTLE_MAX_DELAY' : 60.0,
    'AUTOTHROTTLE_TARGET_CONCURRENCY' :2.0
    
})

process.crawl(PDFdriveCrawler)
process.start()


# In[ ]:





# In[ ]:





# In[11]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import random
from tqdm import tqdm  # Import tqdm


class DataCrawler(scrapy.Spider):
    name = 'emotions-vocab-data'

    def start_requests(self):
        url = 'https://onestopforwriters.com/emotions'
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # Select all <a> elements with href attributes starting with "/emotions" inside <p> elements
        all_url = response.css("p a[href^='/emotions']::attr(href)").extract()
        urls = ['https://onestopforwriters.com' + i for i in all_url]


        # Initialize tqdm with the total number of URLs to track progress

        for single_url in urls:
            yield Request(url=single_url, callback=self.extract_info)
            
    def extract_info(self, response):
        emotion_data = response.css("div.panel-body div[class='thesaurus-field context-menu-selectable']::text").extract()
        yield {
            'Emotion_word' : response.css('h2::text').extract()[0].strip(),
            'Emotion_means' : emotion_data[0],
            'Behaviours' : ','.join(emotion_data[1:])
        }
        
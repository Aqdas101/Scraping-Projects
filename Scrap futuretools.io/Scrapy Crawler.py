import scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

class AIToolsCrawler(CrawlSpider):
    name = 'future-tools-crawler'
    allowed_domains = ['futuretools.io']
    start_urls = ['https://www.futuretools.io/?d34f6f6e_page=1'] 

    max_page = 2

    tool_links_rule = Rule(LinkExtractor(restrict_css='div > a[href^="/tool"]', unique=True), callback='parse_items', follow=False) # get all links
    rule_pagnition = Rule(LinkExtractor(allow=('d34f6f6e_page=\d+'), unique=True), callback='page_checker', follow=True)
                          
    rules = (tool_links_rule, rule_pagnition, )

    def page_checker(self, response):
        self.page_number = int(response.url.split('=')[-1])
        if self.page_number == self.max_page:
             raise scrapy.exceptions.CloseSpider('Reached page limit')
         
    def parse_items(self,response):
        yield {
            'heading' : response.css('h1.heading-3::text').get(),
            'description' : response.css('div.rich-text-block > p::text').get(),
            'upvote' : response.css('div.not-upvoted > a div::text').get(),
            'tag' : response.css('div.tags-block a > div::text').get(),
            'price_model' : response.css('div.div-block-17 div.text-block-2::text').get(),
            'link_web' : response.css("div.cell-2 > a::attr(href)").get() if response.css("div.cell-2 > a::attr(href)").get() else response.url
        }

process = CrawlerProcess({
    
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    'FEED_FORMAT' : 'json',
    'FEED_URI' : 'AItools.json',
    # 'DOWNLOAD_DELAY' : random.uniform(3.0, 5.0),
    # 'ITEM_PIPELINES': {'__main__.DataCleansingPipeline': 1}, # define for pipeline configuration
    'AUTOTHROTTLE_ENABLED' : True, #  This enable Auto Throttle extesnion, and it is pretty awesome.
    'AUTOTHROTTLE_START_DELAY' : 5.0,
    'AUTOTHROTTLE_MAX_DELAY' : 60.0,
    'AUTOTHROTTLE_TARGET_CONCURRENCY' :2.0
    
})

process.crawl(AIToolsCrawler)
process.start()

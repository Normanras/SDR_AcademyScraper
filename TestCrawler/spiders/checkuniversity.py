import scrapy
from scrapy import Request
from TestCrawler.items import TutorialcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class AcademyCrawlerSpider(scrapy.Spider):
    name = 'checkuniversity'
    '''
    url = input("Please enter the URL of the company:  ")
    allowed_domains = [f"https://{url}"]
    start_urls = [f"www.{url}"]
    base_url = start_urls
    rules = [Rule(LinkExtractor(allow=['university/','resources/','knowledge/','academy/','training/']), callback='parse_stuff', follow=True)]
    #file = f'Crawl_{url}.csv'
    '''
    myBaseUrl = ''
    start_urls = []
    def __init__(self, category='', **kwargs): 
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    custom_settings = {
        'FEED_URI' : 'crawl1.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8',
    }

    def parse(self, response):
        universitylink = response.xpath('//a[contains(@href,"university")]/@href').get()
        if universitylink is not None:
            universitylink = response.urljoin(universitylink)
            yield scrapy.Request(universitylink, callback=self.parse_page)

        resourcelink = response.xpath('//a[contains(@href,"resources")]/@href').get()
        if resourcelink is not None:
            resourcelink = response.urljoin(resourcelink)
            yield scrapy.Request(resourcelink, callback=self.parse_page)

        traininglink = response.xpath('//a[contains(@href,"training")]/@href').get()
        if traininglink is not None:
            traininglink = response.urljoin(traininglink)
            yield scrapy.Request(traininglink, callback=self.parse_page)
            
        knowledgelink = response.xpath('//a[contains(@href,"knowledge")]/@href').get()
        if knowledgelink is not None:
            knowledgelink = response.urljoin(knowledgelink)
            yield scrapy.Request(knowledgelink, callback=self.parse_page)

        academylink = response.xpath('//a[contains(@href,"academy")]/@href').get()
        if academylink is not None:
            academylink = response.urljoin(academylink)
            yield scrapy.Request(academylink, callback=self.parse_page)

    def parse_page(self, response):
        title = response.xpath('//title/text()').extract()
        title2 = response.xpath('//head/title/text()').extract()
        university = response.xpath('//a[contains(@href,"university")]/@href').extract()
        academy = response.xpath('//a[contains(@href,"academy")]/@href').extract()
        training = response.xpath('//a[contains(@href,"training")]/@href').extract()
        resources = response.xpath('//a[contains(@href,"resources")]/@href').extract()
        
        yield {
            f'{title}'
            'Title' : title,
            'Title 2' : title2,
            'University' : university,
            'Academy' : academy,
            'Training' : training,
            'Resources' : resources,
        }

        item = TutorialcrawlItem()

        item['title'] = title
        item['title2'] = title2
        item['academy'] = academy
        item['university'] = university
        item['resources'] = resources
        item['training'] = training

        for (title, titles2, university2, academy2, training2, resources2) in zip(title, title2, university, academy, training, resources):
            yield TutorialcrawlItem(titles=title, title2=titles2, university=university2, academy=academy2, training=training2, resources=resources2)

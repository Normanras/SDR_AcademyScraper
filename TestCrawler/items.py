# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AcademyItem(scrapy.Item):
    title = scrapy.Field()
    title2 = scrapy.Field()
    names = scrapy.Field()
    university = scrapy.Field()
    academy = scrapy.Field()
    resources = scrapy.Field()
    knowledge = scrapy.Field()
    training = scrapy.Field()
    learning = scrapy.Field()
    
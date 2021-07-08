import scrapy
from TestCrawler.items import TutorialcrawlItem
import crochet
crochet.setup()

from flask import Flask, render_template, jsonify, request, redirect, url_for
from scrapy import signals, spiders
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
import os

# Importing our Scraping Function from the amazon_scraping file

from TestCrawler.spiders.checkuniversity import AcademyCrawlerSpider

app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['url']
        global baseURL
        baseURL = s

        if os.path.exists("/Projects/TestCrawler/crawl1.json"):
                os.remove("/Projects/TestCrawler/crawl1.json")
        
        return redirect(url_for('scrape'))

@app.route("/scrape")
def scrape():
    scrape_with_crochet(baseURL=baseURL)
    time.sleep(20)
    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(AcademyCrawlerSpider, category='baseURL')
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

if __name__=="__main__":
    app.run(debug=True)
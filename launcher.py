import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from linkedin.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals
import boto3
spider = LinkedInPeopleProfileSpider
process = CrawlerProcess(get_project_settings())

def lambda_handler(event, context):
    http_method = event["httpMethod"]
    if http_method == "POST":
        body = json.loads(event["body"])
        profile = body.get("profile", "jackwillie") 
        results = []
        def collect_items(item, response, spider):
            results.append(dict(item))

        dispatcher.connect(collect_items, signal=signals.item_scraped)
        process.crawl(spider, input='inputargument', profile=profile) ## <-------------- (1)
        process.start(stop_after_crawl=True)
        process.join()
        dispatcher.disconnect(collect_items, signal=signals.item_scraped)


        response = {
            "statusCode": 200,
            "body": json.dumps(results),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        return response
import scrapy
import json
from ..items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'

    def start_requests(self):
        file_list = ['/home/kerem/deCanaria/scrapping-pipeline/data/s01.json', '/home/kerem/deCanaria/scrapping-pipeline/data/s02.json']
        for file_path in file_list:
            # Not: file:/// kullanilabilir
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            yield scrapy.Request(
                url='file://' + file_path,
                cb_kwargs={'data': data},
                callback=self.parse_page
            )

    def parse_page(self, response, data):
        jobs = data.get('jobs', [])
        for job_dict in jobs:
            job_data = job_dict.get('data', {})
            item = JobItem()
            item['slug'] = job_data.get('slug')
            item['title'] = job_data.get('title')
            item['description'] = job_data.get('description')
            # Not: Diğer alanlar da aynı şekilde eklenmeli
            yield item

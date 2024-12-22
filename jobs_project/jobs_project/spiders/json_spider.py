import scrapy
import json
from ..items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'

    def start_requests(self):
        file_list = ['/app/data/s01.json', '/app/data/s02.json']
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
            item['language'] = job_data.get('language')
            item['languages'] = job_data.get('languages')
            item['req_id'] = job_data.get('req_id')
            item['title'] = job_data.get('title')
            item['description'] = job_data.get('description')
            item['street_address'] = job_data.get('street_address')
            item['city'] = job_data.get('city')
            item['state'] = job_data.get('state')
            item['country_code'] = job_data.get('country_code')
            item['postal_code'] = job_data.get('postal_code')
            item['location_type'] = job_data.get('location_type')
            item['latitude'] = job_data.get('latitude')
            item['longitude'] = job_data.get('longitude')
            item['categories'] = job_data.get('categories')
            item['tags'] = job_data.get('tags')
            item['tags5'] = job_data.get('tags5')
            item['tags6'] = job_data.get('tags6')
            item['brand'] = job_data.get('brand')
            item['promotion_value'] = job_data.get('promotion_value')
            item['salary_currency'] = job_data.get('salary_currency')
            item['salary_value'] = job_data.get('salary_value')
            item['salary_min_value'] = job_data.get('salary_min_value')
            item['salary_max_value'] = job_data.get('salary_max_value')
            item['benefits'] = job_data.get('benefits')
            item['employment_type'] = job_data.get('employment_type')
            item['hiring_organization'] = job_data.get('hiring_organization')
            item['source'] = job_data.get('source')
            item['apply_url'] = job_data.get('apply_url')
            item['internal'] = job_data.get('internal')
            item['searchable'] = job_data.get('searchable')
            item['applyable'] = job_data.get('applyable')
            item['li_easy_applyable'] = job_data.get('li_easy_applyable')
            item['ats_code'] = job_data.get('ats_code')
            item['meta_data'] = job_data.get('meta_data')
            item['update_date'] = job_data.get('update_date')
            item['create_date'] = job_data.get('create_date')
            item['category'] = job_data.get('category')
            item['full_location'] = job_data.get('full_location')
            item['short_location'] = job_data.get('short_location')

            yield item

import scrapy

from scrapy.loader import ItemLoader

from ..items import SaibsaItem
from itemloaders.processors import TakeFirst


class SaibsaSpider(scrapy.Spider):
	name = 'saibsa'
	start_urls = ['https://www.saib.com.sa/en/content/press-releases?year=all']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "block-views-block-news-list-block-1")]//span/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="block-core block-basic-page-title"]/h1//text()[normalize-space()]').get()
		description = response.xpath('//div[@class="press_release__body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="press_release__press-release-date"]/text()').get()

		item = ItemLoader(item=SaibsaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

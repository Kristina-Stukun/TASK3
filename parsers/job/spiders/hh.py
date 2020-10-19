import scrapy
from job.items import JobItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = [
           'https://tyumen.hh.ru/search/vacancy?clusters=true&enable_snippets=true&specialization=1&L_save_area=true&area=1384&from=cluster_area&showClusters=true'
    ]
    

    def parse(self, response):
        for href in response.xpath(
                '//a[@data-qa="vacancy-serp__vacancy-title"]/@href'):
            url = response.urljoin(href.extract().split('?')[0])
            yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.xpath(
            '//a[@data-qa="pager-next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        item = JobItem()

        content = response.xpath(
            '(//div[@class="main-content"]//div[contains(@class, "bloko-column_container")])[1]')
        vacancy_section = content.xpath(
            '(//div[@class="vacancy-description"]/div[@class="vacancy-section"])[1]/div[1]')

        item['name'] = content.xpath(
            './/div[contains(@class, "vacancy-title")]/h1//text()').get()

        if len(content.xpath('.//p[@class="vacancy-salary"]//*/text()').getall())>1:
            item['salaryMIN'] = int((content.xpath('.//p[@class="vacancy-salary"]//*/text()').getall()[1]).replace('\xa0',''))
            if len(content.xpath('.//p[@class="vacancy-salary"]//*/text()').getall())>2:
                if content.xpath('.//p[@class="vacancy-salary"]//*/text()').getall()[2] == ' до ':
                    item['salaryMAX'] = int((content.xpath('.//p[@class="vacancy-salary"]//*/text()').getall()[3]).replace('\xa0',''))
                    
                    
        xpath_t = './p/strong[contains(text(), "{}")]/ancestor::p/following::ul[1]/li/text()'
        item['duty'] = vacancy_section.xpath(xpath_t.format(
            'Обязанности')).getall()
        item['requirements'] = vacancy_section.xpath(xpath_t.format(
            'Требования')).getall()
        item['conditions'] = vacancy_section.xpath(xpath_t.format(
            'Условия')).getall()
        
        item['company'] = content.xpath(
            './/a[@data-qa="vacancy-company-name"]//*/text()').getall()[-1]
        item['address'] = content.xpath(
            './/p[@data-qa="vacancy-view-location"]//text()').extract_first()
        item['experience'] = content.xpath(
            './/*[@data-qa="vacancy-experience"]//text()').getall()
        item['type_of_employment'] = content.xpath(
            './/*[@data-qa="vacancy-view-employment-mode"]//text()'
            ).getall()[0]
        item['schedule'] = content.xpath(
            './/*[@data-qa="vacancy-view-employment-mode"]//text()'
            ).getall()[-1]
        item['date'] = content.xpath(
            './/*[@class="vacancy-creation-time"]//text()'
            ).getall()[1]
        item['skills'] = content.xpath(
            './/*[contains(@data-qa, "skills-element")]/span/text()'
            ).getall()
        item['description'] = vacancy_section.get() or ''
        item['url'] = response.request.url

        yield item

import scrapy

from scrapy.item import Field

class JobItem(scrapy.Item):
    name = Field()
    address = Field()
    salaryMIN = Field()
    salaryMAX = Field()
    company = Field()
    date = Field()
    experience = Field()
    type_of_employment = Field()
    description = Field()
    duty = Field()
    requirements = Field()
    skills = Field()
    conditions = Field()
    schedule = Field()
    url = Field()
    pass

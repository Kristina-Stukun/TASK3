import re

from lxml.html.clean import Cleaner


class JobPipeline(object):
    
    def __init__(self):
        self.cleaner = Cleaner(style=True, links=True,
            add_nofollow=True, page_structure=False, safe_attrs=[],
            remove_tags=['svg', 'img'])

    def clean_html(self, html):
        html = self.cleaner.clean_html(html)
        result = re.sub(r'<div>', ' ', html)
        result = re.sub(r'</div>', ' ', result)
        result = re.sub(r'<strong>', ' ', result)
        result = re.sub(r'</strong>', ' ', result)
        result = re.sub(r'<p>', ' ', result)
        result = re.sub(r'</p>', ' ', result)
        result = re.sub(r'<br>', ' ', result)
        result = re.sub(r'</br>', ' ', result)
        result = re.sub(r'<li>', ' ', result)
        result = re.sub(r'</li>', ' ', result)
        result = re.sub(r'<ul>', ' ', result)
        result = re.sub(r'</ul>', ' ', result)
        result = re.sub(r'<em>', ' ', result)
        result = re.sub(r'</em>', ' ', result)
        return re.sub(r'\s+', ' ', result)

    def process_item(self, item, spider):
        item['description'] = self.clean_html(item['description'])
        return item
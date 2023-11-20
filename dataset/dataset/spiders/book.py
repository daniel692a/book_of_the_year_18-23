from pathlib import Path
import scrapy
import pandas as pd
from dataset.items import DatasetItem

df = pd.DataFrame()

class BookSpider(scrapy.Spider):
    name = 'book2023'
    allowed_domains = ['barnesandnoble.com']

    def start_requests(self):
        urls = [
            'https://www.barnesandnoble.com/w/the-heaven-earth-grocery-store-james-mcbride/1142821692?ean=9780593422960',
            'https://www.barnesandnoble.com/w/the-puppets-of-spelhorst-kate-dicamillo/1142940870?ean=9781536234251',
            'https://www.barnesandnoble.com/w/the-wager-david-grann/1141813906?ean=9780385534277',
            'https://www.barnesandnoble.com/w/the-story-of-art-without-men-katy-hessel/1141471389?ean=9780393881875',
            'https://www.barnesandnoble.com/w/yellowface-r-f-kuang/1142006137?ean=9780063250840',
            'https://www.barnesandnoble.com/w/zilot-other-important-rhymes-bob-odenkirk/1143031704?ean=9780316567251',
            'https://www.barnesandnoble.com/w/chili-crisp-james-park/1143036116?ean=9781797223391',
            'https://www.barnesandnoble.com/w/the-berry-pickers-amanda-peters/1143013349?ean=9781646221967',
            'https://www.barnesandnoble.com/w/divine-rivals-rebecca-ross/1141344106?ean=9781250857446',
            'https://www.barnesandnoble.com/w/the-creative-act-rick-rubin/1141404747?ean=9780593653425',
            'https://www.barnesandnoble.com/w/let-us-descend-jesmyn-ward/1142986349?ean=9781982104511',
            'https://www.barnesandnoble.com/w/fourth-wing-rebecca-yarros/1142297916?ean=9781649374080'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data_book = {}
        title = response.css('h1.pdp-header-title::text').get()

        authors = []
        span = response.css('span.contributors')

        for i in range(len(span)):
            authors.append(span.css('a::text')[i].get())

        authors = ", ".join(authors)

        related = []
        span_sub = response.css('span.related-sub-text')

        for i in range(len(span_sub)):
            related.append(span_sub.css('a::text')[i].get())
        related = ", ".join(related)

        ebook_price = response.css('span.price::text').get()

        publisher = ''
        isbn = ''
        publication_date = ''
        sales_rank = ''
        pages = 0
        tr = response.css('tr')

        for t in tr:
            th = t.css('th::text').get()
            td = t.css('td')
            if td.css('a'):
                td = td.css('a')
                td = td.css('span::text').get()
            else:
                td = t.css('td::text').get()

            if th == 'Publisher:':
                publisher = td
            elif th == 'ISBN-13:':
                isbn = td
            elif th == 'Publication date:':
                publication_date = td
            elif th == 'Sales rank:':
                sales_rank = td
            elif th == 'Pages:':
                pages = td

        """ data_book = {
            isbn,
            title,
            authors,
            publisher,
            publication_date,
            sales_rank,
            pages,
            ebook_price,
            related
        } """

        item = DatasetItem()

        item['isbn'] = isbn
        item['title'] = title
        item['authors'] = authors
        item['publisher'] = publisher
        item['publication_date'] = publication_date
        item['sales_rank'] = sales_rank
        item['pages'] = pages
        item['ebook_price'] = ebook_price
        item['related'] = related
        yield item

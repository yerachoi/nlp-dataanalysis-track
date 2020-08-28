import scrapy


class QuotesSpider(scrapy.Spider):
    name = "bok"

    def start_requests(self):
        urls = [
            'https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761&sdate=2005-05-01&edate=2017-12-31',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        total_page_xpath = "//div[@class='schTotal']/span[2]/text()"
        total_page = int(response.xpath(total_page_xpath).extract()[1].split()[0].replace('/', ''))

        urls = ('https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761&sdate=2005-05-01&edate=2017-12-31&pageIndex={}'.format(i) for i in range(1,total_page))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        table_xpath = "//div[@class='fileGoupBox']/ul/li/a[contains(., 'pdf')]/@href"
        pdf_paths = response.xpath(table_xpath).extract()
        filename = 'bok_pdf_paths_test.txt'
        with open(filename, 'a') as f:
            for pdf_path in pdf_paths:
                f.write('https://www.bok.or.kr/' + pdf_path + '\n')

        self.log('Saved pdf paths to %s' % filename)
        
    #   for sel in response.xpath('//ul/li'):
    #      title = sel.xpath('a/text()').extract()
    #      link = sel.xpath('a/@href').extract()
    #      desc = sel.xpath('text()').extract()
    #      print title, link, desc
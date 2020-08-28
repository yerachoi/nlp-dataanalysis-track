import scrapy


class QuotesSpider(scrapy.Spider):
    name = "bok"

    def start_requests(self):
        # base url for BOK minutes
        urls = [
            'https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761&sdate=2005-05-01&edate=2017-12-31',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get the total number of pages (for the result of search)
        total_page_xpath = "//div[@class='schTotal']/span[2]/text()"
        total_page = int(response.xpath(total_page_xpath).extract()[1].split()[0].replace('/', ''))

        # get page urls for of the search between 2005-05-01 and 2017-12-31
        urls = ('https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761&sdate=2005-05-01&edate=2017-12-31&pageIndex={}'.format(i) for i in range(1,total_page))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # get minute names
        pdf_names_xpath = "//span[@class='titlesub']/text()"
        pdf_names = response.xpath(pdf_names_xpath).extract()

        # get file link urls with the string '.pdf'
        pdf_urls_xpath = "//div[@class='fileGoupBox']/ul/li/a[contains(., 'pdf')]/@href"
        pdf_urls = response.xpath(pdf_urls_xpath).extract()
        
        filename = 'bok_pdf_urls.tsv'
        with open(filename, 'a') as f: # if file exists, append
            for pdf_name, pdf_url in zip(pdf_names, pdf_urls):
                f.write(pdf_name + '\t' + 'https://www.bok.or.kr/' + pdf_url + '\n')

        self.log('Saved pdf paths to %s' % filename)
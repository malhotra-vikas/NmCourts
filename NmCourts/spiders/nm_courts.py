import csv
import scrapy
from scrapy import signals
from scrapy.utils.response import open_in_browser
from twocaptcha import TwoCaptcha


class NmCourtsSpider(scrapy.Spider):
    name = "nm_courts"
    url = 'https://caselookup.nmcourts.gov/caselookup/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'JSESSIONID=298985ADD50D9DD5B4BEC3E26D23E5B5',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output_03.csv'
    }

    def __init__(self):
        super().__init__()
        self.inputs = list(csv.DictReader(open('input_01.csv')))

    def start_requests(self):
        if self.inputs:
            yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        url = 'https://caselookup.nmcourts.gov/caselookup/app'
        data = {
            'formids': 'Submit,If',
            'component': 'disclaimerForm',
            'page': 'Home',
            'service': 'direct',
            'session': 'T',
            'submitmode': '',
            'submitname': '',
            'If': 'F',
            'Submit': 'I Accept',
        }

        yield scrapy.FormRequest(url=url, headers=self.headers, method='POST', formdata=data,
                                 callback=self.parse_accept,
                                 dont_filter=True)

    def parse_accept(self, response):
        data_sitekey = response.xpath('//div[@class="g-recaptcha"]/@data-sitekey').get('')
        captcha_response = self.captcha_solver(data_sitekey, self.url)
        print(captcha_response)

        url = 'https://caselookup.nmcourts.gov/caselookup/app'
        data = {
            'formids': 'csrfToken,Submit',
            'component': 'noticeForm',
            'page': 'Notice',
            'service': 'direct',
            'session': 'T',
            'submitmode': '',
            'submitname': '',
            'csrfToken': 'Sjid-5392787059674339833',
            'g-recaptcha-response': captcha_response,
            'Submit': 'Continue to Case Lookup',
        }
        yield scrapy.FormRequest(url=url, headers=self.headers, formdata=data, callback=self.parse_case_lookup,
                                 dont_filter=True)

    def parse_case_lookup(self, response):
        csrf_token = response.xpath('//input[@id="csrfToken"]/@value').get('')
        current_input = self.inputs.pop()
        if current_input.get('name'):
            data = {
                'formids': 'csrfToken,If_2,If_3,partyName,driversLicense,dlState,If_4,dob,yearOnlyDob,caseNumberPartialSearch,courtTypeSelection,dol,caseCategory,dateSearch,dateType,monthFromSelection,dol2,yearFrom,monthToSelection,dol3,yearTo,results,Submit',
                'component': 'nameSearchForm',
                'page': 'NameSearch',
                'service': 'direct',
                'session': 'T',
                'submitmode': '',
                'submitname': '',
                'csrfToken': csrf_token,
                'If_2': 'F',
                'If_3': 'F',
                'If_4': 'F',
                'partyName': current_input.get('name'),
                'driversLicense': '',
                'dlState': '0',
                'dob': '',
                'yearOnlyDob': '',
                'caseNumberPartialSearch': 'on',
                'courtTypeSelection': 'D',
                'dol': '0',
                'caseCategory': '',
                'results': '0',
                'Submit': 'Name Search',
            }

        elif current_input.get('court_type'):
            data = {
                'formids': 'csrfToken,If_2,If_3,partyName,driversLicense,dlState,If_4,dob,yearOnlyDob,caseNumberPartialSearch,courtTypeSelection,dol,caseCategory,dateSearch,dateType,monthFromSelection,dol2,yearFrom,monthToSelection,dol3,yearTo,results,Submit',
                'component': 'nameSearchForm',
                'page': 'NameSearch',
                'service': 'direct',
                'session': 'T',
                'submitmode': '',
                'submitname': '',
                'csrfToken': csrf_token,
                'If_2': 'F',
                'If_3': 'F',
                'If_4': 'F',
                'partyName': current_input.get('name'),
                'driversLicense': '',
                'dlState': '0',
                'dob': '',
                'yearOnlyDob': '',
                'caseNumberPartialSearch': 'on',
                'courtTypeSelection': current_input.get('court_type'),
                'dol': current_input.get('court_location'),
                'caseCategory': '',
                'results': '0',
                'Submit': 'Name Search',
            }

        elif current_input.get('filing_start_date'):
            start_date_split = current_input.get('filing_start_date').split('/')
            start_date = start_date_split[0]
            start_month = start_date_split[1]
            start_year = start_date_split[2]

            end_date_split = current_input.get('filing_end_date').split('/')
            end_date = end_date_split[0]
            end_month = end_date_split[1]
            end_year = end_date_split[2]
            data = {
                'formids': 'csrfToken,If_2,If_3,partyName,driversLicense,dlState,If_4,dob,yearOnlyDob,caseNumberPartialSearch,courtTypeSelection,dol,caseCategory,dateSearch,dateType,monthFromSelection,dol2,yearFrom,monthToSelection,dol3,yearTo,results,Submit',
                'component': 'nameSearchForm',
                'page': 'NameSearch',
                'service': 'direct',
                'session': 'T',
                'submitmode': '',
                'submitname': '',
                'csrfToken': csrf_token,
                'If_2': 'F',
                'If_3': 'F',
                'If_4': 'F',
                'partyName': current_input.get('name'),
                'driversLicense': '',
                'dlState': '0',
                'dob': '',
                'yearOnlyDob': '',
                'caseNumberPartialSearch': 'on',
                'courtTypeSelection': current_input.get('court_type'),
                'dol': current_input.get('court_location'),
                'caseCategory': '',
                'dateSearch': 'on',
                'dateType': '0',
                'monthFromSelection': start_month,
                'dol2': start_date,
                'yearFrom': start_year,
                'monthToSelection': end_month,
                'dol3': end_date,
                'yearTo': end_year,
                'results': '0',
                'Submit': 'Name Search',
            }

        url = 'https://caselookup.nmcourts.gov/caselookup/app'

        yield scrapy.FormRequest(url=url, headers=self.headers, formdata=data, callback=self.parse_search)

    def parse_search(self, response):
        for row in response.xpath('//tr[contains(@id,"informal")]'):
            item = dict()
            item['case_number'] = ''.join(
                [text.strip() for text in row.xpath('./td[@class="fullCaseNumberColumnValue"]//text()').getall() if
                 text])
            item['party_name'] = row.xpath('./td[@class="nameColumnValue"]/text()').get('').strip()
            item['dob'] = row.xpath('.//td[@class="dobColumnValue"]/text()').get("").strip()
            item['party_type'] = row.xpath('./td[@class="partyTypeColumnValue"]/text()').get('').strip()
            item['party #'] = row.xpath('./td[@class="partyNumberColumnValue"]/text()').get('').strip()
            item['case_title'] = row.xpath('./td[@class="caseTitleColumnValue"]/text()').get('').strip()
            item['case_judge'] = row.xpath('./td[@class="caseJudgeColumnValue"]/text()').get('').strip()
            item['court'] = row.xpath('./td[@class="courtDescriptionColumnValue"]/text()').get('').strip()
            item['filing_date'] = ''.join(
                [text.strip() for text in row.xpath('./td[@class="filingDateColumnValue"]//text()').getall() if text])
            pass
            yield item

        next_page = response.xpath('//a[@id="linkFwd_0"]/@href').get('')
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.parse_search, dont_filter=True)

    def captcha_solver(self, site_key, page_url):
        """
        takes site_key and page_url and solve the captcha using 2captcha service
        returns the captcha key
        """
        # creating the colver obj
        solver = TwoCaptcha("fbb180dff2f4cf9541f6e0c3a1adc497")
        result = solver.recaptcha(site_key, page_url)
        print('returning solved captcha')
        return result.get('code')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NmCourtsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)

        return spider

    def spider_idle(self, spider):

        if self.inputs:
            self.crawler.engine.crawl(
                scrapy.Request(
                    url=self.url, headers=self.headers, dont_filter=True),
            )

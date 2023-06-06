import scrapy
from scrapy import Request

class ExhibitorScraperSpider(scrapy.Spider):
    name = 'exhibitor_scraper'
    allowed_domains = ['bio.org']
    start_urls = ['https://www.bio.org/events/bio-international-convention/exhibitor-directory']
    # start_urls = ['https://www.bio.org/events/bio-international-convention/exhibitor-directory?c3=24%2025%2022%2021%2023#filters']

    def parse(self, response):
        results = response.xpath("//div[@class='mc-flipCompany__titleLink']/a/@href").extract()

        for link in results:
            yield Request("https://www.bio.org" + link, callback=self.parse_details)


        absolute_next_url = response.xpath("//li[@class='pager__item--next']/a/@href").get()
        if absolute_next_url:
            yield Request("https://www.bio.org/events/bio-international-convention/exhibitor-directory" + absolute_next_url, callback=self.parse)


    def parse_details(self, response):
        company_name = response.xpath("normalize-space(//h1[@class='oc-articleDetail__title']/div/text())").get()
        booth = response.xpath("normalize-space(//div[@class='oc-articleDetail__infoItem text']/div/text())").get()
        location = response.xpath("normalize-space(//div[@class='oc-articleDetail__location']/div/text())").get()

        twitter = ""
        linkedin = ""
        facebook = ""
        website = ""


        links = response.xpath("//div[@class='oc-articleDetail__channelIcon']/a/@href").extract()

        for link in links:
            if  "twitter" in link:
                twitter = link

            elif "facebook" in link:
                facebook = link

            elif "linkedin" in link:
                linkedin = link

            else:
                website = link

        description = response.xpath("normalize-space(//div[@class='oc-articleDetail__body']/div/text())").get()
        focus_areas = ', '.join(response.xpath("//div[@class='ac-tagLink__link']/a/text()").extract())

        yield{
            "Company name": company_name,
            "Booth number": booth,
            "Company location": location,
            "Twitter": twitter,
            "Linkedin": linkedin,
            "Facebook": facebook,
            "Website": website,
            "Description": description,
            "Focus areas": focus_areas,
        }
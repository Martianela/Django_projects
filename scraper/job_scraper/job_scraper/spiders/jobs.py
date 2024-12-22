import scrapy
from scrapy.utils.project import get_project_settings
class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ['dice.com']
    start_urls = [
        'https://www.dice.com/jobs?q=Software&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.workplaceTypes=Remote&filters.employmentType=CONTRACTS&currencyCode=USD&language=en'
    ]

    def start_requests(self):
        settings = get_project_settings()
        user_agent = settings.get('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
        
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={
                    'User-Agent': user_agent,
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://www.dice.com/',
                },
                meta={
                    "playwright": True,
                    "playwright_context": "default",
                },
            )

    async def parse(self, response):
        # Extract job IDs from dynamically rendered content
        job_ids = response.css('a[data-cy="card-title-link"]::attr(id)').extract()
        self.logger.info(f"Found Job IDs: {job_ids}")

        # Construct job detail URLs and yield requests
        base_url = "https://www.dice.com/job-detail/"
        for job_id in job_ids:
            job_url = f"{base_url}{job_id}"
            self.logger.info(f"Fetching Job URL: {job_url}")
            yield scrapy.Request(
                job_url,
                callback=self.parse_job_details,
                headers={
                    'User-Agent': response.request.headers.get('User-Agent'),
                },
                meta={"playwright": True},
            )

    async def parse(self, response):
        # Extract job IDs from dynamically rendered content
        job_ids = response.css('a[data-cy="card-title-link"]::attr(id)').extract()
        self.logger.info(f"Found Job IDs: {job_ids}")

        # Construct job detail URLs and yield requests
        base_url = "https://www.dice.com/job-detail/"
        for job_id in job_ids:
            job_url = f"{base_url}{job_id}"
            self.logger.info(f"Fetching Job URL: {job_url}")
            yield scrapy.Request(
                job_url,
                callback=self.parse_job_details,
                meta={"playwright": True},
            )

        # Handle pagination
        # next_page = response.css('a.pagination-next::attr(href)').get()
        # if next_page:
        #     self.logger.info(f"Following next page: {next_page}")
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback=self.parse,
        #         meta={"playwright": True},
        #     )

    async def parse_job_details(self, response):
        try:
            # Extract job details from dynamically rendered content
            job_title = response.css('h1[data-cy="jobTitle"]::text').get()
            company_name = response.css('a[data-cy="companyNameLink"]::text').get()
            company_url = response.css('a[data-cy="companyNameLink"]::attr(href)').get()
            posted_date = response.css('span#timeAgo::text').get()
            location = response.css('span#location::text').get()
            pay_details = response.css('span#payChip::text').get()
            employment_details = response.css('span[id^="employmentDetailChip"]::text').getall()
            skills = response.css('span[id^="skillChip"]::text').getall()
            job_description = response.css('div#jobDescriptionHtml p::text').getall()

            # Create a dictionary to store the data
            job_data = {
                'jobTitle': job_title.strip() if job_title else None,
                'company': {
                    'name': company_name.strip() if company_name else None,
                    'companyProfileUrl': company_url,
                },
                'postedDate': posted_date.strip() if posted_date else None,
                'location': location.strip() if location else None,
                'payDetails': pay_details.strip() if pay_details else None,
                'employmentDetails': employment_details,
                'skills': skills,
                'jobDescription': " ".join(job_description).strip(),
            }
            self.logger.info(f"Scraped Job Data: {job_data}")
            yield job_data
        except Exception as e:
            self.logger.error(f"Error while parsing job details: {e}")

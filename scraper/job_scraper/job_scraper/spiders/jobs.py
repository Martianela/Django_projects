import scrapy
import requests

class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ['dice.com']
    start_urls = [
        'https://www.dice.com/jobs?q=Software&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.workplaceTypes=Remote&filters.employmentType=CONTRACTS&currencyCode=USD&language=en'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,  # Enable Playwright for this request
                    "playwright_context": "default",  # Use the default Playwright context
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # Add any other custom headers you need here
                    'Accept-Language': 'en-US,en;q=0.9',
                }
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
                    meta={"playwright": True,
                          "playwright_include_page":True,
                        #   "playwright_page": response.meta["playwright_page"],
                        },
                     headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # Add any other custom headers you need here
                    'Accept-Language': 'en-US,en;q=0.9',
                    }
                )

        # Handle pagination
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            self.logger.info(f"Following next page: {next_page}")
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={"playwright": True,"playwright_include_page":True, "playwright_page": response.meta['playwright_page']},
            )

    async def parse_job_details(self, response):
        try:
            # Extract job details from dynamically rendered content
            page = response.meta["playwright_page"]
            await page.wait_for_selector('h1[data-cy="jobTitle"]', timeout=60000) 
            
            job_title = response.css('h1[data-cy="jobTitle"]::text').get()
            company_name = response.css('a[data-cy="companyNameLink"]::text').get()
            company_url = response.css('a[data-cy="companyNameLink"]::attr(href)').get()
            posted_date = response.css('span#timeAgo::text').get()
            location = response.css('div[data-cy="locationDetails"] span::text').get()  # Updated location extraction
            pay_details = response.css('div[data-cy="payDetails"] span::text').get()  # Updated pay details extraction
            employment_details = response.css('div[data-cy="employmentDetails"] span::text').getall()  # Updated employment details extraction
            
            # Extract all skills
            
            # await page.wait_for_selector('div[data-cy="skillsList"] .chip_chip__cYJs6 span')
            skills = response.css('div[data-cy="skillsList"] .chip_chip__cYJs6 span::text').getall()

            # self.logger.info('skills',response.css('div[data-cy="skillsList"]').getall())
            # Extract full job description
            # Extracting the job description text from the HTML
            job_description = response.css('div#jobDescriptionHtml *::text').getall()
            # self.logger.info('job details',job_description)
            # Cleaning and formatting the extracted text
            job_details_section = response.css('div[data-testid="jobDescriptionHtml"]')

            if job_details_section:
                # Extract all text while handling tags like <p>, <li>
                job_description_parts = job_details_section.css('p::text, li::text').getall()
                # Clean and join the extracted parts
                job_description = " ".join([text.strip() for text in job_description_parts if text.strip()])
            else:
                job_description = "Job details section not found."

            # Output or log the job description
            # self.logger.info(job_description)

            if not job_title or not company_name:
               self.logger.warning("Incomplete data. Skipping job entry.")
               return  # Skip posting if essential data is missing
            

            # Create a dictionary to store the data
            job_data = {
                "title": job_title.strip(),
                "company_name": company_name.strip(),
                "company_profile_url": company_url,
                "location": location.strip() if location else None,
                "posted_date": posted_date.strip() if posted_date else None,
                "pay_details": pay_details.strip() if pay_details else None,
                "employment_details": ", ".join(employment_details),
                "skills": ", ".join(skills) if skills else None,
                "job_description": job_description
            }

            yield job_data

            self.logger.info(f"Scraped Job Data: {job_data}")

            self.logger.info(f"Posting Job Data: {job_data}")
            response = requests.post(
                "http://127.0.0.1:8000/api/jobs/",
                json=job_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 201:
                self.logger.info("Job successfully posted to the API.")
            else:
                self.logger.error(f"Failed to post data: {response.status_code}, {response.text}")

        except Exception as e:
            self.logger.error(f"Error while parsing job details: {e}")

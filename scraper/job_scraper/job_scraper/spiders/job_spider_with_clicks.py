import scrapy


class JobsSpiderWithClicks(scrapy.Spider):
    name = "jobs_with_clicks"
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
            )

    async def parse(self, response):
        # Extract job card elements to simulate clicks
        job_cards = response.css('a[data-cy="card-title-link"]')
        self.logger.info(f"Found {len(job_cards)} job cards.")

        for job_card in job_cards:
            # Click on each job card and extract details
            yield scrapy.Request(
                response.url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,  # Include page object to perform actions
                    "job_element": job_card,  # Pass job element for clicking
                },
                callback=self.parse_job_with_click,
            )

        # Handle pagination
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            self.logger.info(f"Following next page: {next_page}")
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={"playwright": True},
            )

    async def parse_job_with_click(self, response):
        page = response.meta["playwright_page"]
        job_element = response.meta["job_element"]

        try:
            # Click on the job element to open the job details page
            await job_element.click()
            await page.wait_for_selector("#jobDescriptionHtml")  # Wait for job details to load

            # Extract job details from the rendered page
            job_title = page.locator('h1[data-cy="jobTitle"]').text_content()
            company_name = page.locator('a[data-cy="companyNameLink"]').text_content()
            company_url = page.locator('a[data-cy="companyNameLink"]').get_attribute("href")
            posted_date = page.locator('span#timeAgo').text_content()
            location = page.locator('span#location').text_content()
            pay_details = page.locator('span#payChip').text_content()
            employment_details = page.locator('span[id^="employmentDetailChip"]').all_text_contents()
            skills = page.locator('span[id^="skillChip"]').all_text_contents()
            job_description = page.locator('div#jobDescriptionHtml p').all_text_contents()

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

        finally:
            await page.close()

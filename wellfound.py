import scrapy


class WellfoundSpider(scrapy.Spider):
    name = "wellfound"
    allowed_domains = ["wellfound.com"]
    start_urls = ["https://wellfound.com/jobs"]

    def start_requests(self):
        """Initializes requests with Playwright enabled."""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                },
            )

    def parse(self, response):
        """Parses the job listings from the current page."""
        # Update the CSS selector based on the actual structure of the website
        job_cards = response.css("div.job-card")  # Replace 'job-card' with the correct class
        if not job_cards:
            self.logger.warning("No job listings found. Check your selectors.")

        for job in job_cards:
            title = job.css("h2::text").get()
            company = job.css(".company-name::text").get(default="").strip()
            location = job.css(".location::text").get(default="").strip()
            job_link = job.css("a::attr(href)").get()

            yield {
                "title": title.strip() if title else "N/A",
                "company": company,
                "location": location,
                "link": response.urljoin(job_link) if job_link else "N/A",
            }

        # Handle pagination
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            self.logger.info(f"Navigating to the next page: {next_page}")
            yield response.follow(
                next_page,
                callback=self.parse,
                meta={"playwright": True},
            )
        else:
            self.logger.info("No more pages to scrape.")


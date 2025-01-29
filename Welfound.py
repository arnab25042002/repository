import os
import pandas as pd
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the paths
INPUT_HTML_PATH = r"C:\Users\ARNAB BANDYOPADHYAY\Downloads\Welfound.html"
OUTPUT_CSV_PATH = r"C:\Users\ARNAB BANDYOPADHYAY\Downloads\job_listings.csv"

# Function to extract job data and delete processed parts
def extract_and_delete(html_path):
    """Extract job data from an HTML file and delete processed parts."""
    try:
        # Read the HTML file
        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        logging.error(f"File not found at {html_path}")
        return [], None
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return [], None

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "lxml")
    job_data = []

    # Find all job postings
    job_posts = soup.find_all("div", class_="min-h-[50px] items-end justify-between rounded-2xl px-2 py-2 sm:flex")
    if not job_posts:
        logging.warning("No job postings found.")
        return [], soup

    for idx, job in enumerate(job_posts, start=1):
        try:
            # Extract job details
            job_title_tag = job.find("a", class_="mr-2 text-sm font-semibold text-brand-burgandy hover:underline")
            job_title = job_title_tag.text.strip() if job_title_tag else "N/A"

            employment_type_tag = job.find("span", class_="whitespace-nowrap rounded-lg bg-accent-yellow-100 px-2 py-1 text-[10px] font-semibold text-neutral-800")
            employment_type = employment_type_tag.text.strip() if employment_type_tag else "N/A"

            company_tag = soup.find("a", class_="text-neutral-1000 hover:underline focus:no-underline")
            company_name = company_tag.text.strip() if company_tag else "N/A"

            location_div = job.find_all("div", class_="flex items-center text-neutral-500")
            location = location_div[0].find("span", class_="pl-1 text-xs").text.strip() if location_div else "N/A"

            experience = "N/A"
            if len(location_div) > 1:
                experience_tag = location_div[1].find("span", class_="pl-1 text-xs")
                experience = experience_tag.text.strip() if experience_tag else "N/A"

            Year = "N/A"
            if len(location_div) > 2:
                Year_tag = location_div[2].find("span", class_="pl-1 text-xs")
                Year = Year_tag.text.strip() if Year_tag else "N/A"

            posted_time_tag = job.find("span", class_="text-xs lowercase text-dark-a md:hidden")
            posted_time = posted_time_tag.text.strip() if posted_time_tag else "N/A"

            # Append job data
            job_data.append({
                "Job Title": job_title,
                "Company Name": company_name,
                "Employment Type": employment_type,
                "Salary": location,
                "Location" : experience,
                "Experience" : Year,
                "Posted Time": posted_time,
                
            })

            # Remove the processed job posting
            job.decompose()

        except Exception as e:
            logging.warning(f"Error processing job posting {idx}: {e}")
            continue

    # Remove the specific section between the two divs
    try:
        start_div = soup.find("div", class_="mb-6 w-full rounded border border-gray-400 bg-white")
        end_div = soup.find("div", class_="w-full sm:w-min")
        if start_div and end_div:
            while start_div != end_div:
                next_sibling = start_div.find_next_sibling()
                if next_sibling:
                    next_sibling.decompose()
                start_div.decompose()

            # Finally, remove the Apply button div
            end_div.decompose()
    except Exception as e:
        logging.warning(f"Error removing specific section: {e}")

    return job_data, soup

def save_html(soup, html_path):
    """Save the modified HTML content back to the file."""
    try:
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(str(soup))
        logging.info(f"HTML file updated at {html_path}")
    except Exception as e:
        logging.error(f"Error saving HTML file: {e}")

def save_to_csv(data, output_path):
    """Save extracted data to a CSV file."""
    if not data:
        logging.info("No data to save.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    try:
        if os.path.exists(output_path):
            # Append to the existing CSV
            df_existing = pd.read_csv(output_path)
            df_new = pd.DataFrame(data)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(output_path, index=False, encoding="utf-8")
        else:
            # Save as a new CSV
            pd.DataFrame(data).to_csv(output_path, index=False, encoding="utf-8")
        logging.info(f"Data successfully saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving CSV file: {e}")

if __name__ == "__main__":
    # Extract job data and update the HTML
    jobs, updated_soup = extract_and_delete(INPUT_HTML_PATH)

    if jobs:
        # Save the data to CSV
        save_to_csv(jobs, OUTPUT_CSV_PATH)

        # Save the updated HTML
        if updated_soup:
            save_html(updated_soup, INPUT_HTML_PATH)
    else:
        logging.info("No data extracted.")

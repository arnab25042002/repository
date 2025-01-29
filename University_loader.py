from bs4 import BeautifulSoup
import csv

# Filepath to your HTML file
html_file_path = "C:\\Users\\ARNAB BANDYOPADHYAY\\Downloads\\university.html"

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract university data
universities = []

# Find all university sections
university_sections = soup.find_all('section', class_='DetailCardGlobalUniversities__CardContainer-sc-1v60hm5-0')
for section in university_sections:
    university_name = section.find('h2', class_='Heading-sc-1w5xk2o-0').get_text(strip=True)
    location_info = section.find('p', class_='Paragraph-sc-1iyax29-0').get_text(strip=True)
    country, city = location_info.split('|')
    country = country.strip()
    city = city.strip()

    # Extract scores and ranks
    scores = section.find_all('dd', class_='QuickStatHug__Description-hb1bl8-1')
    global_score = scores[0].get_text(strip=True) if len(scores) > 0 else None
    subject_score = scores[1].get_text(strip=True) if len(scores) > 1 else None

    scores_and_ranks = section.find_all('li', class_='RankList__ListItem-sc-2xewen-1')
    global_rank = subject_rank = None

    for rank in scores_and_ranks:
        rank_text = rank.find('div', class_='RankList__Rank-sc-2xewen-2').get_text(strip=True)
        if 'Best Global Universities' in rank.get_text():
            global_rank = rank_text.replace('#', '').strip()
        elif 'Best Universities for' in rank.get_text():
            subject_rank = rank_text.replace('#', '').strip()

    # Store the university data
    university_data = {
        "University Name": university_name,
        "Country": country,
        "City": city,
        "Global Score": global_score,
        "Subject Score": subject_score,
        "Global Rank": global_rank,
        "Subject Rank": subject_rank,
    }
    universities.append(university_data)

# Write data to a CSV file
output_file = r"C:\Users\ARNAB BANDYOPADHYAY\Downloads\universities_data.csv"
with open(output_file, 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[
        "University Name", "Country", "City", "Global Score", "Subject Score", "Global Rank", "Subject Rank"
    ])
    writer.writeheader()
    writer.writerows(universities)

print(f"Extracted data saved to {output_file}")

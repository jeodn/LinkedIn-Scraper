import time
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from random import randrange

# --- List of LinkedIn profile URLs to scrape ---
pages = pd.read_csv('linkedin_connection_profiles.csv')['Profile URL'].dropna().tolist()

# --- Scrape profiles ---
data = []

for p in pages:
    driver.get(url)
    time.sleep(randrange(3,5))  # Wait for page to load fully

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    name = soup.find('h1').text.strip() if soup.find('h1') else "N/A"
    
    # Find the education section
    education_section = soup.find('section', {'id': 'education-section'})
    
    schools = []
    if education_section:
        for school in education_section.find_all('li'):
            school_name = school.find('h3')
            if school_name:
                schools.append(school_name.text.strip())
    
    # Alternate method (because LinkedIn changes layout often)
    if not schools:
        for span in soup.find_all('span'):
            if 'Education' in span.text:
                next_section = span.find_parent('section')
                if next_section:
                    for li in next_section.find_all('li'):
                        school = li.find('h3')
                        if school:
                            schools.append(school.text.strip())
    
    data.append({
        'Name': name,
        'Profile URL': url,
        'Schools': ', '.join(schools) if schools else "N/A"
    })
    print(f"Scraped {name}")
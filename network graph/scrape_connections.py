import time
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import random

# --- Setup Chrome driver ---
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

# --- Login manually first ---
driver.get('https://www.linkedin.com/login')
print("Please log in manually within 60 seconds...")
time.sleep(60)

# --- Load connection profile URLs ---
profile_urls = pd.read_csv('linkedin_connection_profiles_TEST.csv')['Profile URL'].dropna().tolist()

edges = []  # Person -> Mutual connections

def extract_names(driver, person_name) -> list[str]:
    """Return list of all mutual connection names by navigating pagination."""
    rejected_names = ['Status is reachable', '• 1st', '1st degree connection', 'Status is offline']
    collected_names = []

    while True:
        # Reparse the page every time after clicking
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        container = soup.find('div', class_='search-results-container')

        if not container:
            print("No mutuals container found!")
            break

        # --- Extract names from current page ---
        for span in container.find_all('span'):
            text = span.get_text(strip=True)
            if text and (2 <= len(text.split()) <= 3) and not text.lower().startswith('see all') and text not in collected_names and text not in rejected_names:
                collected_names.append(text)

        # --- Try to find the Next button ---
        next_button = container.find('button', attrs={"aria-label": "Next"})
        if next_button:
            # Check if disabled
            if next_button.has_attr('disabled'):
                print("Reached last page of mutuals.")
                break
            else:
                # Click the Next button using Selenium
                try:
                    # Find and click the button in the real DOM (not just HTML)
                    next_button_real = driver.find_element('xpath', '//button[@aria-label="Next" and not(@disabled)]')
                    next_button_real.click()
                    print("Clicked Next. Loading more mutuals...")
                    time.sleep(random.uniform(3, 5))  # Wait for new page to load
                except Exception as e:
                    print(f"Error clicking Next button: {e}")
                    break
        else:
            print("No Next button found.")
            break

    return collected_names

# --- Loop over each connection profile ---
for idx, profile_url in enumerate(profile_urls):
    driver.get(profile_url)
    time.sleep(random.uniform(4,6)) # WAIT TO LOAD.

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # --- Get the main connection's name ---
    name_tag = soup.find('h1')
    person_name = name_tag.text.strip() if name_tag else f"Person_{idx}"

    # --- Find link to mutual connections page ---
    mutuals_link = None
    for a_tag in soup.find_all('a', href=True):
        if 'connections' in a_tag.text.lower() and 'mutual' in a_tag.text.lower():
            mutuals_link = a_tag['href']
            break

    if mutuals_link:
        if mutuals_link.startswith('/'):
            mutuals_link = 'https://www.linkedin.com' + mutuals_link
        
        driver.get(mutuals_link)
        time.sleep(random.uniform(4,6))

        # --- Extract all mutuals (with pagination) ---
        mutual_names = extract_names(driver, person_name)

        # --- Save edges ---
        for mutual_name in mutual_names:
            edges.append((person_name, mutual_name))

        print(mutual_names)
        print(f"Scraped {len(mutual_names)} mutuals for {person_name}")

    else:
        print(f"No mutuals link found for {person_name}")

    time.sleep(random.uniform(4,6))

# --- Save edges ---
edges_df = pd.DataFrame(edges, columns=['Person', 'MutualConnection'])
edges_df.to_csv('linkedin_mutual_connections_full.csv', index=False)

print("Scraping complete! Saved mutual connections.")
driver.quit()

import time
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import random
import os

# --- Settings ---
BATCH_SIZE = 10   # Number of profiles per batch
#SHORT_SLEEP = random.uniform(4, 6)  # Seconds between profiles
#LONG_SLEEP = random.uniform(19, 24) # Seconds between batches
SAVE_FILE = 'linkedin_education_data_batched.csv'

# --- Set up browser ---
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

# --- Log in manually ---
driver.get('https://www.linkedin.com/login')
print("Please log in manually within the next 60 seconds...")
time.sleep(60)

# --- Load all profile URLs ---
profile_urls = pd.read_csv('linkedin_connection_profiles.csv')['Profile URL'].dropna().tolist()

# --- Helper to split list into batches ---
def batchify(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i+batch_size]

# --- Initialize output CSV ---
if not os.path.exists(SAVE_FILE):
    # Create CSV with headers if it doesn't exist
    pd.DataFrame(columns=['Name', 'Profile URL', 'Schools']).to_csv(SAVE_FILE, index=False)

# --- Scrape profiles batch by batch ---
for batch_num, batch in enumerate(batchify(profile_urls, BATCH_SIZE), 1):
    print(f"\nProcessing batch {batch_num} with {len(batch)} profiles...")

    batch_data = []

    for url in batch:
        driver.get(url)
        SHORT_SLEEP = random.uniform(4, 6)
        time.sleep(SHORT_SLEEP)  # Short sleep between profiles

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else "N/A"

        schools = []
        for span in soup.find_all('span'):
            if span.text:
                text = span.text.strip()
                if ("University" in text or "College" in text or "Institute" in text) and (len(text.split()) <= 4):
                    schools.append(text)

        batch_data.append({
            'Name': name,
            'Profile URL': url,
            #'Schools': ', '.join(set(schools)) if schools else "N/A"
            'Schools': schools[0] if schools else "N/A"
        })
        print(f"  Scraped {name}: Student at {schools}")

    # --- Save after each batch ---
    df_batch = pd.DataFrame(batch_data)
    df_batch.to_csv(SAVE_FILE, mode='a', header=False, index=False)

    # Sleep longer after each batch
    LONG_SLEEP = random.uniform(14, 24)
    print(f"Batch {batch_num} saved. Sleeping for {LONG_SLEEP} seconds...")
    time.sleep(LONG_SLEEP)

# --- Close browser ---
print("ALL PROCESSED")
driver.quit()

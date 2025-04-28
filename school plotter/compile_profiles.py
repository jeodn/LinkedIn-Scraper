import time
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# --- Set up the browser ---
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

# --- Open LinkedIn and wait for manual login ---
driver.get('https://www.linkedin.com/login')
print("Please log in manually within the next 60 seconds...")
time.sleep(60)

# --- Navigate to connections page ---
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
time.sleep(5)

# --- Scroll to load all connections ---
SCROLL_PAUSE_TIME = 3

last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(10):  # You can increase the range if you have many connections
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    
# --- Parse the page ---
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all connection profile links
profile_links = []

for link in soup.find_all('a', href=True):
    href = link['href']
    if href.startswith('/in/'):  # LinkedIn profiles usually start with '/in/'
        full_link = 'https://www.linkedin.com' + href.split('?')[0]  # Remove tracking params
        if full_link not in profile_links:
            profile_links.append(full_link)

# --- Save to CSV ---
df = pd.DataFrame(profile_links, columns=['Profile URL'])
df.to_csv('linkedin_connection_profiles.csv', index=False)

print(f"Scraped {len(profile_links)} connection profile URLs!")
print("Saved to linkedin_connection_profiles.csv")

# --- Close browser ---
driver.quit()
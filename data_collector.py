import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
import time
import os

from sqlalchemy import create_engine

# --- 1. Web Scraping Function ---
def scrape_breach_portal():
    """
    Scrapes a hypothetical data breach notification portal.
    You need to find real URLs for state attorney general websites.
    """
    # Example URL from California Attorney General's office
    url = "https://oag.ca.gov/privacy/databreach/list"
    incidents = []
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # NOTE: This part is highly specific to the website's HTML structure.
        # You will need to inspect the HTML of your target sites to find the right tags.
        breach_entries = soup.find_all('div', class_='breach-entry') # This is a placeholder class
        
        for entry in breach_entries:
            date = entry.find('span', class_='date-class').text
            company = entry.find('a', class_='company-class').text
            incidents.append({'date': date, 'company': company, 'region': 'US', 'source': url})

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        
    print(f"Scraped {len(incidents)} incidents from {url}")
    return incidents

# --- 2. API Querying Function ---
def query_nvd_api():
    """
    Queries the NIST NVD API for vulnerabilities related to 'AI'.
    This is an example of getting structured data.
    """
    # NVD API endpoint for CVEs
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {'keywordSearch': 'artificial intelligence', 'resultsPerPage': 50}
    incidents = []
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        for cve_item in data.get('vulnerabilities', []):
            cve_id = cve_item['cve']['id']
            published_date = cve_item['cve']['published']
            description = cve_item['cve']['descriptions'][0]['value']
            
            # Simple check to assign region based on description content
            region = 'EU' if 'GDPR' in description else 'US' if 'CCPA' in description else 'Global'
            
            incidents.append({'date': published_date, 'company': cve_id, 'region': region, 'source': 'NVD API'})
        
    except requests.exceptions.RequestException as e:
        print(f"Error querying NVD API: {e}")
        
    print(f"Queried {len(incidents)} incidents from NVD API")
    return incidents
    
# --- 3. RSS Feed Parsing Function ---
def parse_security_rss_feed():
    """
    Parses an RSS feed from a cybersecurity news website.
    """
    # Example RSS feed URL (The Hacker News)
    url = "https://feeds.feedburner.com/TheHackersNews"
    incidents = []
    
    feed = feedparser.parse(url)
    
    for entry in feed.entries:
        title = entry.title
        published_date = entry.published
        link = entry.link
        
        # Simple logic to find keywords
        if 'breach' in title.lower() or 'attack' in title.lower():
            # A more advanced version would use NLP to determine region
            region = 'EU' if 'europe' in title.lower() else 'US' if 'u.s.' in title.lower() else 'Unknown'
            incidents.append({'date': published_date, 'company': title, 'region': region, 'source': 'The Hacker News RSS', 'link': link})

    print(f"Parsed {len(incidents)} incidents from RSS feed")      
    return incidents



# --- Main Execution ---
if __name__ == "__main__":
    print("Starting data collection...")
    
    # Run all collection functions
    scraped_incidents = scrape_breach_portal()
    time.sleep(1) # Be respectful and pause between requests
    api_incidents = query_nvd_api()
    time.sleep(1)
    rss_incidents = parse_security_rss_feed()
    
    # Combine all results
    all_incidents = scraped_incidents + api_incidents + rss_incidents
    
    # Convert to a pandas DataFrame for easy handling
    df = pd.DataFrame(all_incidents)
    
    # Save to a CSV file
    output_path = 'data/incidents_database.csv'
    df.to_csv(output_path, index=False)

    print(f"\nCollection complete. Found {len(df)} potential incidents.")
    print(f"Data saved to {output_path}")

    #SAVE TO EXCEL
    path = 'data'
    excel_path = os.path.join(path, 'incidents_database.xlsx')
    print(f"Attempting to save data to {excel_path}...")
    try:
        # engine='openpyxl' es necesario para archivos .xlsx
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print("Data saved successfully as an Excel file!")
    except PermissionError:
        print(f"Permission denied: Unable to save to {excel_path}. Please close the file if it's open and try again.")
    except Exception as e:
        print(f"An error occurred while saving to Excel: {e}")

    #SAVE AS JSON
    json_path = os.path.join(path, 'incidents_database.json')
    print(f"Attempting to save data to {json_path}...")
    try:
        df.to_json(json_path, index=False)
        print("Data saved successfully as a JSON file!")
    except PermissionError:
        print(f"Permission denied: Unable to save to {json_path}. Please close the file if it's open and try again.")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

    #SAVE IN SQLITE
    db_path = os.path.join(path, 'incidents_database.sqlite')
    print(f"Attempting to save data to {db_path}...")
    try:
        # Crea una "conexión" a la base de datos en el archivo
        engine = create_engine(f'sqlite:///{db_path}')
        # Guarda el DataFrame en una tabla llamada 'incidents'
        # if_exists='replace' borrará la tabla anterior cada vez que ejecutes el script
        df.to_sql('incidents', engine, if_exists='replace', index=False)
        print("Data saved successfully to SQLite database!")
    except Exception as e: # Capturamos un error más genérico para bases de datos
        print(f"\n--- ERROR ---")
        print(f"Could not write to the database: {e}")
        print("----------------")



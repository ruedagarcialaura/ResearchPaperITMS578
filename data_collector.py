import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import PyPDF2
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# --- 1. Keyword Definitions (Unchanged) ---
AI_KEYWORDS = [
    'deepfake', 'adversarial attack', 'model poisoning', 
    'data poisoning', 'machine learning', 'generative ai'
]
INCIDENT_KEYWORDS = [
    'attack', 'breach', 'vulnerability', 'threat actor', 'malware', 
    'exploit', 'incident', 'campaign', 'phishing'
]

# --- 2. Deep Analysis Function (for PDFs) ---
def analyze_alert_pdf_content(alert_url, driver):
    """
    Performs the SLOW, deep analysis on a single, promising candidate.
    """
    try:
        driver.get(alert_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.c-field--name-body')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        pdf_link_tag = soup.select_one('a[href$=".pdf"]')
        if not pdf_link_tag:
            # If no PDF, analyze the body text as a fallback
            print("      -> No PDF found, analyzing body text...")
            content_element = soup.select_one('div.c-field--name-body')
            if not content_element: return False
            page_text = content_element.get_text().lower()
        else:
            pdf_url = urljoin(alert_url, pdf_link_tag['href'])
            print(f"      -> Found PDF: {pdf_url.split('/')[-1]}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            pdf_response = requests.get(pdf_url, headers=headers)
            pdf_response.raise_for_status()
            pdf_file = BytesIO(pdf_response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_text = ""
            for page in pdf_reader.pages:
                page_text += page.extract_text() or ""
            page_text = page_text.lower()

        found_ai_keys = [key for key in AI_KEYWORDS if key in page_text]
        found_incident_keys = [key for key in INCIDENT_KEYWORDS if key in page_text]
        is_relevant = bool(found_ai_keys) and bool(found_incident_keys)
        
        if is_relevant:
            print(f"      -> SUCCESS: AI Keys Found: {found_ai_keys}, Incident Keys Found: {found_incident_keys}")
        
        return is_relevant
    except Exception as e:
        print(f"      -> Error during deep analysis: {e}")
        return False

# --- 3. Fast Triage Scraper (NEW LOGIC) ---
def triage_cisa_alerts_list(driver, max_pages):
    """
    Performs a FAST triage by scanning only the summaries on the list pages.
    Returns a short list of promising candidates for deep analysis.
    """
    base_url = "https://www.cisa.gov/news-events/cybersecurity-advisories"
    print(f"--- Phase 1: Fast Triage of CISA advisories (up to {max_pages} pages) ---")
    driver.get(base_url)
    promising_candidates = []
    page_num = 1

    while page_num <= max_pages:
        print(f"  -> Scraping page {page_num} for summaries...")
        try:
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.c-view__row')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            alert_rows = soup.select('div.c-view__row')
            if not alert_rows: break

            for row in alert_rows:
                summary_tag = row.select_one('div.c-teaser__summary')
                title_tag = row.select_one('h3.c-teaser__title a')
                if summary_tag and title_tag:
                    summary_text = summary_tag.get_text().lower()
                    # --- FAST TRIAGE: Check if any keyword exists in the summary ---
                    if any(key in summary_text for key in AI_KEYWORDS):
                        title = title_tag.text.strip()
                        link = urljoin(base_url, title_tag['href'])
                        print(f"    -> PROMISING CANDIDATE FOUND: {title}")
                        promising_candidates.append({'title': title, 'link': link})
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li.c-pager__item--next a')
                parent_li = next_button.find_element(By.XPATH, '..')
                if 'is-disabled' in parent_li.get_attribute('class'): break
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)
                page_num += 1
                time.sleep(3)
            except (NoSuchElementException, TimeoutException):
                break
        except Exception as e:
            print(f"  -> An error occurred during pagination: {e}")
            break
            
    return promising_candidates

# --- 4. Main Execution (Updated with 2-Phase Logic) ---
if __name__ == "__main__":
    print("--- Starting V18 Data Collection with Fast Triage ---")
    MAX_PAGES_TO_SCRAPE = 3 # Limit for the fast triage phase
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    
    driver = None
    confirmed_incidents = []
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # --- PHASE 1: Get promising candidates quickly ---
        candidates = triage_cisa_alerts_list(driver, MAX_PAGES_TO_SCRAPE)
        
        # --- PHASE 2: Perform deep analysis only on the best candidates ---
        if candidates:
            print(f"\n--- Phase 2: Performing Deep Analysis on {len(candidates)} promising candidates... ---")
            for i, alert in enumerate(candidates):
                print(f"  -> Deep Checking ({i+1}/{len(candidates)}): {alert['title']}")
                if analyze_alert_pdf_content(alert['link'], driver):
                    confirmed_incidents.append({
                        'title': alert['title'], 'region': 'US',
                        'source': 'CISA Advisory', 'link': alert['link']
                    })
                time.sleep(1)
            
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        if driver:
            driver.quit()

    if not confirmed_incidents:
        print("\n--- Collection Complete: No CISA advisories were confirmed after deep analysis. ---")
    else:
        df = pd.DataFrame(confirmed_incidents)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        output_path = os.path.join(data_dir, 'ai_incidents_database_v18.xlsx')
        print(f"\n--- Collection Complete: Found {len(df)} unique and confirmed relevant CISA advisories. ---")
        try:
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Data saved to {output_path}")
        except PermissionError:
            print(f"ERROR: PERMISSION DENIED. Is the file open in Excel?")


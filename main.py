# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# import pandas as pd
# import time
# import os

# def setup_driver():
#     """Setup headless Chrome driver with necessary options"""
#     try:
#         chrome_options = Options()
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('--window-size=1920,1080')
#         chrome_options.add_argument('--disable-extensions')
#         chrome_options.add_argument('--disable-popup-blocking')
#         chrome_options.add_argument('--disable-blink-features=AutomationControlled')

#         driver = webdriver.Chrome(options=chrome_options)
#         print("✅ Chrome driver setup successful")
#         return driver
#     except Exception as e:
#         print(f"❌ Failed to setup Chrome driver: {str(e)}")
#         raise

# def wait_for_table(driver, timeout=30):
#     """Wait for table to load and verify its contents"""
#     try:
#         print("⏳ Waiting for table to be present...")
#         table = WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "table"))
#         )
#         print("✅ Table found, waiting for rows...")
#         time.sleep(2)

#         max_retries = 3
#         for attempt in range(max_retries):
#             try:
#                 rows = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
#                 )
#                 if rows:
#                     print(f"✅ Found {len(rows)} rows in table")
#                     return table, rows
#             except StaleElementReferenceException:
#                 if attempt < max_retries - 1:
#                     print(f"🔄 Stale element, retrying... (attempt {attempt + 1})")
#                     time.sleep(2)
#                     continue
#                 else:
#                     raise Exception("❌ Max retries reached for finding table rows")

#         raise Exception("❌ No rows found in table")

#     except TimeoutException as e:
#         print(f"❌ Timeout while waiting for table: {str(e)}")
#         raise
#     except Exception as e:
#         print(f"❌ Error in wait_for_table: {str(e)}")
#         raise

# def extract_table_data(driver, table, rows):
#     """Extract data from table with retry mechanism"""
#     try:
#         headers = [
#             'Company Name', 'Status', 'Price', 'GMP', 'Est. Listing Price', 'Fire Rating',
#             'IPO Size', 'Lot Size', 'Open Date', 'Close Date', 'Allotment Date', 'Listing Date', 'Last Updated'
#         ]

#         data = []
#         for row in rows[1:]:
#             try:
#                 cols = row.find_elements(By.TAG_NAME, "td")
#                 if cols and len(cols) >= 5:
#                     row_data = [col.text.strip() if col.text.strip() and col.text.strip() != '--' else None for col in cols]
#                     while len(row_data) < len(headers):
#                         row_data.append(None)
#                     if any(row_data):
#                         data.append(row_data[:len(headers)])
#             except StaleElementReferenceException:
#                 print("⚠️ Skipping stale row")
#                 continue
#             except Exception as e:
#                 print(f"❌ Error processing row: {str(e)}")
#                 continue

#         if not data:
#             raise Exception("❌ No data rows were extracted")

#         return headers, data

#     except Exception as e:
#         print(f"❌ Error in extract_table_data: {str(e)}")
#         raise

# def save_to_excel(data, headers, filename="ipo_gmp_data.xlsx"):
#     """Save scraped data to Excel file"""
#     try:
#         df = pd.DataFrame(data, columns=headers)

#         # Clean numeric data
#         for col in ['Price', 'GMP', 'Est. Listing Price', 'IPO Size', 'Lot Size']:
#             if col in df.columns:
#                 df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
#                 df[col] = pd.to_numeric(df[col], errors='coerce')

#         df.to_excel(filename, index=False)
#         print(f"✅ Data saved successfully in {filename}")

#     except Exception as e:
#         print(f"❌ Error saving data to Excel: {str(e)}")

# def scrape_ipo_gmp():
#     """Scrape IPO GMP data and save to Excel"""
#     driver = None
#     try:
#         print("🚀 Starting web scraping process...")
#         driver = setup_driver()

#         print("🌍 Navigating to InvestorGain...")
#         driver.get("https://www.investorgain.com/report/live-ipo-gmp/331/all/")

#         table, rows = wait_for_table(driver)
#         headers, data = extract_table_data(driver, table, rows)

#         print(f"✅ Successfully extracted {len(data)} rows of data")
#         save_to_excel(data, headers)

#     except Exception as e:
#         print(f"❌ Error: {str(e)}")

#     finally:
#         if driver:
#             try:
#                 driver.quit()
#                 print("✅ Chrome driver closed successfully")
#             except Exception as e:
#                 print(f"❌ Error closing Chrome driver: {str(e)}")

# # Run the script
# scrape_ipo_gmp()

# New 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
# import pandas as pd
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import time

# # Google Sheets Config
# SHEET_NAME = "IPO_GMP_Data"  # Change to your Google Sheet name
# WORKSHEET_NAME = "Sheet1"  # Change to your sheet name

# def setup_google_sheets():
#     """Authenticate and return Google Sheets client."""
#     try:
#         scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#         client = gspread.authorize(creds)
#         sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
#         print("✅ Google Sheets connection established")
#         return sheet
#     except Exception as e:
#         print(f"❌ Google Sheets setup failed: {str(e)}")
#         raise

# def setup_driver():
#     """Setup headless Chrome driver"""
#     try:
#         chrome_options = Options()
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('--window-size=1920,1080')

#         driver = webdriver.Chrome(options=chrome_options)
#         print("✅ Chrome driver setup successful")
#         return driver
#     except Exception as e:
#         print(f"❌ Failed to setup Chrome driver: {str(e)}")
#         raise

# def wait_for_table(driver, timeout=30):
#     """Wait for table to load"""
#     try:
#         print("⏳ Waiting for table to load...")
#         table = WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "table"))
#         )
#         time.sleep(2)
#         rows = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
#         )
#         print(f"✅ Found {len(rows)} rows in table")
#         return table, rows
#     except TimeoutException as e:
#         print(f"❌ Timeout while waiting for table: {str(e)}")
#         raise

# def extract_table_data(driver, rows):
#     """Extract data from the table"""
#     headers = [
#         'Company Name', 'Status', 'Price', 'GMP', 'Est. Listing Price', 'Fire Rating',
#         'IPO Size', 'Lot Size', 'Open Date', 'Close Date', 'Allotment Date', 'Listing Date', 'Last Updated'
#     ]

#     data = []
#     for row in rows[1:]:
#         try:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             row_data = [col.text.strip() if col.text.strip() else None for col in cols]
#             while len(row_data) < len(headers):
#                 row_data.append(None)
#             data.append(row_data[:len(headers)])
#         except StaleElementReferenceException:
#             continue

#     return headers, data

# def update_google_sheet(sheet, data, headers):
#     """Upload data to Google Sheets"""
#     try:
#         sheet.clear()  # Clear existing data
#         sheet.append_row(headers)  # Add headers
#         sheet.append_rows(data)  # Add new data
#         print(f"✅ Data updated successfully in Google Sheet: {SHEET_NAME}")
#     except Exception as e:
#         print(f"❌ Error updating Google Sheet: {str(e)}")

# def scrape_ipo_gmp():
#     """Scrape IPO GMP data and update Google Sheets"""
#     driver = None
#     try:
#         print("🚀 Starting web scraping process...")
#         driver = setup_driver()
#         sheet = setup_google_sheets()

#         print("🌍 Navigating to InvestorGain...")
#         driver.get("https://www.investorgain.com/report/live-ipo-gmp/331/all/")

#         table, rows = wait_for_table(driver)
#         headers, data = extract_table_data(driver, rows)

#         print(f"✅ Successfully extracted {len(data)} rows of data")
#         update_google_sheet(sheet, data, headers)

#     except Exception as e:
#         print(f"❌ Error: {str(e)}")

#     finally:
#         if driver:
#             driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import json
import os

# Google Sheets Config
SHEET_NAME = "IPO_GMP_Data"  # Change to your Google Sheet name
WORKSHEET_NAME = "Sheet1"  # Change to your sheet name

def setup_google_sheets():
    """Authenticate using environment variable and return Google Sheets client."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # 🟢 Load credentials from environment variable instead of file
        creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
        print("✅ Google Sheets connection established")
        return sheet
    except Exception as e:
        print(f"❌ Google Sheets setup failed: {str(e)}")
        raise

def setup_driver():
    """Setup headless Chrome driver"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome driver setup successful")
        return driver
    except Exception as e:
        print(f"❌ Failed to setup Chrome driver: {str(e)}")
        raise

def wait_for_table(driver, timeout=30):
    """Wait for table to load"""
    try:
        print("⏳ Waiting for table to load...")
        table = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        time.sleep(2)
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        print(f"✅ Found {len(rows)} rows in table")
        return table, rows
    except TimeoutException as e:
        print(f"❌ Timeout while waiting for table: {str(e)}")
        raise

def extract_table_data(driver, rows):
    """Extract data from the table"""
    headers = [
        'Company Name', 'Status', 'Price', 'GMP', 'Est. Listing Price', 'Fire Rating',
        'IPO Size', 'Lot Size', 'Open Date', 'Close Date', 'Allotment Date', 'Listing Date', 'Last Updated'
    ]

    data = []
    for row in rows[1:]:
        try:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() if col.text.strip() else None for col in cols]
            while len(row_data) < len(headers):
                row_data.append(None)
            data.append(row_data[:len(headers)])
        except StaleElementReferenceException:
            continue

    return headers, data

def update_google_sheet(sheet, data, headers):
    """Upload data to Google Sheets"""
    try:
        sheet.clear()  # Clear existing data
        sheet.append_row(headers)  # Add headers
        sheet.append_rows(data)  # Add new data
        print(f"✅ Data updated successfully in Google Sheet: {SHEET_NAME}")
    except Exception as e:
        print(f"❌ Error updating Google Sheet: {str(e)}")

def scrape_ipo_gmp():
    """Scrape IPO GMP data and update Google Sheets"""
    driver = None
    try:
        print("🚀 Starting web scraping process...")
        driver = setup_driver()
        sheet = setup_google_sheets()

        print("🌍 Navigating to InvestorGain...")
        driver.get("https://www.investorgain.com/report/live-ipo-gmp/331/all/")

        table, rows = wait_for_table(driver)
        headers, data = extract_table_data(driver, rows)

        print(f"✅ Successfully extracted {len(data)} rows of data")
        update_google_sheet(sheet, data, headers)

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    finally:
        if driver:
            driver.quit()
            print("✅ Chrome driver closed successfully")

if __name__ == "__main__":
    scrape_ipo_gmp()

            print("✅ Chrome driver closed successfully")

# Run the script
scrape_ipo_gmp()

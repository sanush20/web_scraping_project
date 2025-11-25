from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# ---------------- Step 1: Create Driver ----------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Website URL
url = "https://quotes.toscrape.com/js"
driver.get(url)

# ---------------- Step 2: Prepare CSV ----------------
csv_file = open("quotes_data.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["Quote", "Author"])  # CSV Headers

# ---------------- Step 3: Pagination Loop ----------------
while True:
    try:
        # Wait until quotes appear
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "text")))

        # Extract quotes and authors
        quotes = driver.find_elements(By.CLASS_NAME, "text")
        authors = driver.find_elements(By.CLASS_NAME, "author")

        # Save to CSV
        for q, a in zip(quotes, authors):
            print(q.text, "-", a.text)
            writer.writerow([q.text, a.text])

        # Handle pagination
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            driver.execute_script("arguments[0].click();", next_button)  # safer click
            time.sleep(2)

        except:
            print("\n--- No more pages. Scraping finished. ---")
            break

    except Exception as e:
        print("Error:", e)
        break

# ---------------- Step 4: Cleanup ----------------
csv_file.close()
driver.quit()

print("\nData saved as: quotes_data.csv")

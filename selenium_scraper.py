from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def extract_claims_data():
    # Setup the browser driver (Chrome in this example)
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # This will open the local HTML file
    driver.get("file:///C:/Users/PRAKA/OneDrive/Desktop/healthcare_portal_automation/mock_portal/index.html")

    # This will simulate clicking the login button
    login_button = driver.find_element(By.TAG_NAME, 'button')
    login_button.click()

    # This Wait for the page to load claims data
    time.sleep(1)

    # This will extract table data
    claims_data = []
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        claim = {
            "Patient ID": columns[0].text,
            "Name": columns[1].text,
            "Service Date": columns[2].text,
            "Billing Code": columns[3].text
        }
        claims_data.append(claim)

    # This will close the browser
    driver.quit()

    # This will return the extracted data
    return claims_data


if __name__ == "__main__":
    data = extract_claims_data()
    for record in data:
        print(record)



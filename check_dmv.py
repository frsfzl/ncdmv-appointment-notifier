from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

def get_active_locations():
    print("Starting get_active_locations...")

    # Path to my local geckodriver executable for Firefox automation
    GECKO_PATH = r".\geckodriver.exe"

    # Set up Firefox options, maximizing window for better interaction
    options = Options()
    options.add_argument("--start-maximized")

    # Automatically allow geolocation requests without prompts
    options.set_preference("permissions.default.geo", 1)
    options.set_preference("geo.prompt.testing", True)
    options.set_preference("geo.prompt.testing.allow", True)

    # Initialize Firefox driver service with the given executable path
    service = Service(GECKO_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    active_locations = []  # List to hold available appointment locations

    try:
        # Open the NCDMV appointment page
        driver.get("https://skiptheline.ncdot.gov/Webapp/Appointment/Index/a7ade79b-996d-4971-8766-97feb75254de")

        wait = WebDriverWait(driver, 10)  # Wait object for element presence and interactions

        # Find and click the "Make an Appointment" button
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Make an Appointment')]")))
        print("Clicking 'Make an Appointment' button...")
        button.click()

        # Handle possible JS alert popup after clicking button
        try:
            alert = wait.until(EC.alert_is_present(), message="Waiting for alert timed out")
            print("Alert detected, accepting it now...")
            alert.accept()
        except Exception:
            print("No alert popup appeared.")

        # Click the "Teen Driver Level 3" appointment type option
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Teen Driver Level 3')]")))
        print("Selecting 'Teen Driver Level 3' option...")
        button.click()

        # Wait for active appointment locations to load, or timeout if none found
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.QflowObjectItem.Active-Unit")))
        except Exception:
            print("No active appointment locations detected on the page.")
            return []  # Return empty list if no locations available

        # Grab all the divs that mark active appointment spots
        active_location_divs = driver.find_elements(By.CSS_SELECTOR, "div.QflowObjectItem.Active-Unit")

        # Extract the location names from the divs
        for div in active_location_divs:
            try:
                # Location name is usually inside nested divs
                location_name = div.find_element(By.CSS_SELECTOR, "div > div:first-child").text.strip()
                active_locations.append(location_name)
            except Exception:
                # If structure changes, fallback to grabbing all text inside div
                active_locations.append(div.text.strip())

        if not active_locations:
            print("Looks like no available appointments right now.")
        else:
            print("Found these active locations with appointments:")
            for loc in active_locations:
                print(loc)

    except Exception as e:
        print(f"Oops, something went wrong: {e}")
        print(traceback.format_exc())
    finally:
        # Always close the browser no matter what happened
        driver.quit()

    return active_locations


if __name__ == "__main__":
    # Run the function and print out the results for debugging
    locations = get_active_locations()
    print("Final list of found locations:", locations)
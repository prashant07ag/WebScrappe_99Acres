from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

property_names = []
property_costs = []
property_types = []
property_areas = []
property_localities = []
average_property_costs = []

# Initialize the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

# Define the city and its corresponding 99acres URL
city_details = [
    ('Pune', 'pune-all', 19),
    ('Delhi', 'delhi-ncr-all', 1),
    ('Mumbai', 'mumbai-all', 12),
    ('Lucknow', 'lucknow', 205),
    ('Ahmedabad', 'ahmedabad-all', 45),
    ('Kolkata', 'kolkata-all', 25),
    ('Jaipur', 'jaipur', 177),
    ('Chennai', 'chennai-all', 32),
    ('Bengaluru', 'bangalore-all', 20),
]

# Loop through each city
for city_name, city, city_no in city_details:
    URL = f"https://www.99acres.com/search/property/buy/{city}?city={city_no}&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N"
    driver.get(URL)
    print(f"Scraping data for {city_name}")

    # Scroll down to load more listings
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extract property details
    property_listings = soup.find_all('div', {'class': ["projectTuple__tupleDetails", "projectTuple__premiumWrapper", "projectTuple__fsl"]})

    for property in property_listings:
        property_names.append(property.find('a', {'class': ["projectTuple__projectName", "projectTuple__pdWrap20", "ellipsis"]}).text)
        cost_range = property.find('div', {'class': "configurationCards__cardPriceHeadingWrapper"}).text
        property_costs.append(cost_range)
        property_types.append(property.find('div', {'class': ["configurationCards__cardConfigBand", "undefined"]}).text)
        
        area_element = property.find('span', {'class': ["configurationCards__cardAreaHeading", "ellipsis"]})
        if area_element:
            property_areas.append(area_element.text)
        else:
            property_areas.append("N/A")
        
        locality_element = property.find('div', {'class': "SliderTagsAndChips__sliderChipsStyle"})
        if locality_element:
            property_localities.append(locality_element.text)
        else:
            property_localities.append("N/A")



# Create a DataFrame
data = {
    'Property Name': property_names,
    'Property Cost': property_costs,
    'Property Type': property_types,
    'Property Area': property_areas,
    'Property Locality': property_localities,
}

df = pd.DataFrame(data)

# Convert columns to numeric, handling non-numeric values
print(df.head())

# Close the WebDriver
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

driver_service = webdriver.chrome.service.Service('chromedriver-mac-x64/chromedriver')

def scrape_availability():
    print('Started Webscraping Data')
    browser = webdriver.Chrome(service=driver_service)
    browser.get("https://disneyland.disney.go.com/passes/blockout-dates/")

    passes = ['inspire', 'believe', 'enchant', 'imagine', 'dream']

    # wait for entire page and js to load
    WebDriverWait(browser, 10).until(visibility_of_element_located((By.CSS_SELECTOR, ".sectionComponent")))

    for i in range(0, 5, 1):
        browser.execute_script(f'document.getElementsByClassName("sectionComponent")[0].shadowRoot.children[2].children[0].items[{i}].click()')
        with open(f'data/{passes[i]}.json', 'w') as outfile:
            print(f"Successfully recieved data on the {passes[i].capitalize()} pass")
            outfile.write(str(browser.execute_script('return document.getElementsByClassName("calendarContainer")[0].children[0].children[0].children[0].$.admissionCalendar.dates')))
            print(f"Wrote to file: {passes[i].capitalize()}.json")

    browser.close()
import asyncio
import json
from pyppeteer import launch
from pyppeteer_stealth import stealth


async def scrape_availability():
    print('Started Webscraping Data')
    browser = await launch(headless=True, args=['--disable-dev-shm-usage', '--no-sandbox'])
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.')
    await page.setViewport({'width': 1280, 'height': 800})
    await stealth(page) 
    await page.goto("https://disneyland.disney.go.com/passes/blockout-dates/")

    # Output browser to file
    content = await page.content()

    passes = ['inspire', 'believe', 'enchant', 'imagine', 'dream']

    # Wait for the entire page and JavaScript to load
    await asyncio.sleep(5)

    for i, pass_name in enumerate(passes):
        # Execute JavaScript on the page to simulate clicks
        await page.evaluate(f'''() => {{
            document.getElementsByClassName("sectionComponent")[0].shadowRoot.children[2].children[0].items[{i}].click()
        }}''')

        # Fetch data
        pass_data = await page.evaluate('''() => {
            return document.getElementsByClassName("calendarContainer")[0].children[0].children[0].children[0].$.admissionCalendar.dates;
        }''')

        # Write to JSON file
        with open(f'../data/{pass_name}.json', 'w') as outfile:
            print(f"Successfully received data on the {pass_name.capitalize()} pass")
            json.dump(pass_data, outfile)
            print(f"Wrote to file: {pass_name.capitalize()}.json")

    await browser.close()

# Call the function to perform scraping
asyncio.get_event_loop().run_until_complete(scrape_availability())

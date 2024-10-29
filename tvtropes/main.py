from playwright.sync_api import sync_playwright

def scrape_tvtropes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        page.goto("https://tvtropes.org/pmwiki/pmwiki.php/Main/TheEveryman")

        # Simulate clicking the "open/close all folders" button
        page.click('.folderlabel')  # Adjust selector as needed

        # Now scrape the contents after opening the folders
        content = page.content()  # Get the entire page content

        print(content)
        browser.close()

scrape_tvtropes()

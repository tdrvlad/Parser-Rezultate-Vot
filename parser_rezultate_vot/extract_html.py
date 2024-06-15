from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

HTML_ELEMENTS_TO_REMOVE = ["script", "style", "footer", "svg", "img", "iframe", "nav"]


def filter_html_content(html_content, elements_to_remove=HTML_ELEMENTS_TO_REMOVE):
    """
    Process the HTML content to remove style, script, and image elements.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in elements_to_remove:
        for script in soup.find_all(element):
            script.decompose()

    return str(soup)


def get_html_content(url: str) -> str:
    """
    Loads the HTML content of a URL using Selenium to handle JavaScript.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Allow some time for the JavaScript to execute
    time.sleep(5)

    html_content = driver.page_source
    driver.quit()
    return html_content

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pandas as pd




class BookDetailsScraper:
    def __init__(self, url, webdriver_path):
        self.url = url
        self.webdriver_path = webdriver_path
        self.ua = UserAgent()
        self.user_agent = self.ua.random
        self.headers = {'User-Agent': self.user_agent}
        self.options = Options()
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

    def scrape_details(self):
        self.driver.get(self.url)
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # Extracting Book Title
        title_element = soup.select_one('h1.MuiTypography-root.MuiTypography-h1.mui-style-1ngtbwk')
        book_title = title_element.text.strip() if title_element else "Title Not Found"

        # Extracting Author
        author_element = soup.select_one('span.MuiTypography-root.MuiTypography-body1.mui-style-1plnxgp')
        book_author = author_element.text.strip() if author_element else "Author Not Found"

        # Extracting Discounted Price
        discounted_price_element = soup.select_one('p.MuiTypography-root.MuiTypography-body1.BuyBox_sale-price__PWbkg.mui-style-tgrox')
        discounted_price = discounted_price_element.text.strip() if discounted_price_element else "Discounted Price Not Found"

        # Extracting Original Price (RRP)
        original_price_element = soup.select_one('p.MuiTypography-root.MuiTypography-body1.mui-style-vrqid8 > span.strike')
        original_price = original_price_element.text.strip() if original_price_element else "Original Price Not Found"

        # Clicking Details Button
        details_button = self.driver.find_element(By.ID, "pdp-tab-details")
        details_button.click()

        # Extracting Details
        details_container = soup.select_one('div.MuiBox-root.mui-style-h3npb')
        details = {}
        if details_container:
            for p_tag in details_container.find_all('p'):
                text_content = p_tag.text.strip()
                label, value = text_content.split(':', 1)
                details[label.strip()] = value.strip()

        exclude_labels = {'ISBN', 'Audience', 'Country of Publication', 'Language', 'Series', 'Dimensions (cm)',
                          'Weight (kg)'}  # Labels to exclude

        # Preparing data for CSV
        data = {
            "Title": [book_title],
            "Author": [book_author],
            "Discounted Price": [discounted_price],
            "Original Price (RRP)": [original_price]
        }
        if details:
            for label, value in details.items():
                if label not in exclude_labels:  # Check if the label should be printed
                    data[label] = [value]

        # Creating DataFrame
        df = pd.DataFrame(data)
        # save in Csv file
        df.to_csv('CSV_book_details_of_Single_ISBN.csv', mode='a', header=not os.path.exists('CSV_book_details_of_Single_ISBN.csv'), index=False)

    def close_driver(self):
        self.driver.quit()


url = "https://www.booktopia.com.au/what-happened-to-nina--dervla-mctiernan/book/9781460760147.html"
webdriver_path = r"C:\Users\mnaga\Downloads\chromedriver-win64\chromedriver.exe"
scraper = BookDetailsScraper(url, webdriver_path)
scraper.scrape_details()
scraper.close_driver()

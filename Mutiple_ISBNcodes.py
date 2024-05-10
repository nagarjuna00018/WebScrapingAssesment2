import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class BookDetailsScraper:
    def __init__(self, chromedriver_path, url_base, isbn_csv_path, user_agents_txt_path, output_csv_path):
        self.chromedriver_path = chromedriver_path
        self.url_base = url_base
        self.isbn_csv_path = isbn_csv_path
        self.user_agents_txt_path = user_agents_txt_path
        self.output_csv_path = output_csv_path

    def scrape_book_details(self):
        # Read ISBN list from CSV file
        isbn_df = pd.read_csv(self.isbn_csv_path)
        isbn_list = isbn_df["ISBN13"].tolist()

        # Read user agents from text file
        with open(self.user_agents_txt_path, "r") as file:
            user_agents = file.readlines()

        for isbn in isbn_list:
            for user_agent in user_agents:
                user_agent = user_agent.strip()
                self._scrape_book(isbn, user_agent)

    def _scrape_book(self, isbn, user_agent):
        options = Options()
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        data = {}  # Initialize data outside the try block

        try:
            url = f"{self.url_base}search.ep?keywords={isbn}"
            driver.get(url)

            # Explicit wait for the search bar element to be present
            search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-bar")))

            # Clear search bar, enter ISBN, and submit search
            search_bar.clear()
            search_bar.send_keys(isbn)
            search_bar.submit()

            # Wait for the book details to load
            time.sleep(3)  # Add delay to ensure page loads
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            # Check if the book is found
            not_found_element = soup.find('p', text='Sorry, no products were found for that search term')
            if not_found_element:
                print(f"Book with ISBN {isbn} not found.")
                return  # Skip to the next ISBN

            # Extracting Book Title
            title_element = soup.find('h1', class_='MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk')
            book_title = title_element.text.strip() if title_element else "Title Not Found"

            # Extracting Author
            author_element = soup.find('span', class_='MuiTypography-root MuiTypography-body1 mui-style-1plnxgp')
            book_author = author_element.text.strip() if author_element else "Author Not Found"

            # Extracting Discounted Price
            discounted_price_element = soup.find('p', class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox')
            discounted_price = discounted_price_element.text.strip() if discounted_price_element else "Discounted Price Not Found"

            # Extracting Original Price (RRP)
            original_price_element = soup.find('p', class_='MuiTypography-root MuiTypography-body1 mui-style-vrqid8').find('span', class_='strike')
            original_price = original_price_element.text.strip() if original_price_element else "Original Price Not Found"

            # Clicking Details Button
            details_button = driver.find_element(By.ID, "pdp-tab-details")
            details_button.click()

            # Extracting Details
            details_container = soup.select_one('div.MuiBox-root.mui-style-h3npb')
            details = {}
            if details_container:
                for p_tag in details_container.find_all('p'):
                    text_content = p_tag.text.strip()
                    label, value = text_content.split(':', 1)
                    details[label.strip()] = value.strip()
            else:
                print("Details Container Not Found")

            exclude_labels = {'ISBN', 'Audience', 'Country of Publication', 'Language', 'Series', 'Dimensions (cm)',
                              'Weight (kg)'}  # Labels to exclude
            # Prepare data for DataFrame
            data = {
                "Title": [book_title],
                "Author": [book_author],
                "Discounted Price": [discounted_price],
                "Original Price (RRP)": [original_price],
                "User Agent": [user_agent]
            }
            if details:
                for label, value in details.items():
                    if label not in exclude_labels:  # Check if the label should be printed
                        data[label] = [value]
            else:
                print("Details Not Found")
        except Exception as e:
            print(f"Error occurred while scraping details for ISBN {isbn} with user agent {user_agent}: {e}")
        finally:
            driver.quit()

        df = pd.DataFrame(data)
        # save in Csv file
        df.to_csv(self.output_csv_path, mode='a', header=not os.path.exists(self.output_csv_path), index=False)

# Example usage:
chromedriver_path = r"C:\Users\mnaga\Downloads\chromedriver-win64\chromedriver.exe"
url_base = "https://www.booktopia.com.au/"
isbn_csv_path = r"C:\Users\Arjun\Downloads\web-scrapingAssessment2-main\web-scrapingAssessment2-main\input_list.csv"
user_agents_txt_path = r"C:\Users\Arjun\Downloads\web-scrapingAssessment2-main\web-scrapingAssessment2-main\Chrome.txt"
output_csv_path = 'CSV_book_details_of_Multiple_ISBNCodes.csv'

scraper = BookDetailsScraper(chromedriver_path, url_base, isbn_csv_path, user_agents_txt_path, output_csv_path)
scraper.scrape_book_details()

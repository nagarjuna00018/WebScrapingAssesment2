
# Book Details Scraper

This Python script scrapes details of a single book from the Booktopia website and saves them to a CSV file.

## Introduction

This script utilizes Selenium and BeautifulSoup to extract details such as book title, author, discounted price, original price (RRP), and additional information from a single book page on the Booktopia website. The scraped data is then saved to a CSV file.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Chrome webdriver
- Required Python libraries:
  - selenium
  - BeautifulSoup
  - pandas
  - fake_useragent

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nagarjuna00018/book-details-scraper.git
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Download the Chrome webdriver and specify its path in the script.

## Usage

1. Specify the URL of the book page and the path to the Chrome webdriver in the script.
2. Run the script:

```bash
Single_ISBNcode.py
```

3. The scraped book details will be saved in a CSV file named `CSV_book_details_of_Single_ISBN.csv`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

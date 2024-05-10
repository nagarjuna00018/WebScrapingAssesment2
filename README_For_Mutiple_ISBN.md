# Book Details Scraper

This Python script scrapes details of multiple books from the Booktopia website using different user agents for each request and saves them to a CSV file.

## Introduction

This script utilizes Selenium and BeautifulSoup to extract details such as book title, author, discounted price, original price (RRP), and additional information from multiple book pages on the Booktopia website. It rotates through a list of user agents to mimic different web browsers and avoid detection.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Chrome webdriver
- Required Python libraries:
  - selenium
  - BeautifulSoup
  - pandas

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nagarjuna00018/WebScrapingAssesment2.git 
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Download the Chrome webdriver and specify its path in the script.

## Usage

1. Prepare a CSV file containing a list of ISBNs named `input_list.csv`.
2. Prepare a text file containing a list of user agents named `Chrome.txt`.
3. Run the script:

```bash
Mutiple_ISBNcodes.py
```

4. The scraped book details will be saved in a CSV file named `CSV_book_details_of_Multiple_ISBNCodes.csv`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

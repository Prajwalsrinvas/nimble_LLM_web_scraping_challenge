
<div >
<h1 align="center">
<a href="https://www.nimbleway.com/">Nimble</a> &amp;<a href="https://substack.thewebscraping.club?r=u72gk">The Web Scraping Club</a> AI <a href="https://github.com/Nimbleway/challenge">Challenge</a>
</h1>
<h3 align="center">🕷️ Web scraping using Nimble data extraction API and OpenAI LLM 🕷️</h3>
</div>

---


## 📍Overview

- This is a Python project that extracts specific elements by web scraping given URLs and collects product URLs.
- It supports pagination and provides options to write the collected data to an output file or print it as a formatted table.
- The project also includes functions for preprocessing HTML content, removing unwanted elements, and minimizing the modified HTML code.
- Overall, the project aims to streamline the process of web scraping and data extraction, saving time and effort for users.

---

## 🚀 Usage

1. Clone the repo

```
git clone https://github.com/Prajwalsrinvas/nimble_LLM_web_scraping_challenge
```

2. Create Virtual environment and install requirements
   
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. View CLI help

```
python main.py --help
```

The following is displayed:

```
usage: main.py [-h] (--start_url START_URL | --start_urls_file START_URLS_FILE) [--output_file_name OUTPUT_FILE_NAME] [--max_pages MAX_PAGES]
               [--store_html]

Process start URLs.

options:
  -h, --help            show this help message and exit
  --start_url START_URL
                        URL to be scraped. Scraped product urls will be displayed as a table.
  --start_urls_file START_URLS_FILE
                        Path to file containing list of URLs. JSON, CSV and TXT files are supported.
  --output_file_name OUTPUT_FILE_NAME
                        Path to file to store scraped product URLs. JSON, CSV and TXT files are supported. If not provided, it is stored in
                        '{Y_m_d_H_M_S}_output.{start_urls_file extension}' by defult
  --max_pages MAX_PAGES
                        Maximum number of pages to be scraped. This overrides default value set in config.toml.
  --store_html          Writes Raw and processed HTML to disk.
```

---


## 🤖 Examples

- Extract links from a single URL. Displays scraped data in the form of a table
```
python main.py --start_url https://books.toscrape.com
```

- Extract links from a single URL, from first 5 pages and store the scraped data in a JSON file.
- `--max_pages` overrides deault max_pages value in `config.toml`
```
python main.py --start_url https://www.gsmarena.com/samsung-phones-9.php --max_pages 5 --output_file_name books.json
```

- Extract multiple links, being read from a file. JSON, CSV and TXT file formats are supported.
- When `--start_urls_file` is used, it stores the scraped data to a file with same format of the input file.
```
python main.py --start_urls_file input/start_urls.csv
```

- Extract multiple links, being read from a file.
- When ``--output_file_name`` is used, it stores the scraped data to a file with the given format. JSON, CSV and TXT file formats are supported.
```
python main.py --start_urls_file input/start_urls.txt --output_file_name books.json
```

- When `--store_html` is passed, the Scraped HTML and the Processed HTML is stored to disk.
```
python main.py --start_urls_file input/start_urls.txt --output_file_name books.csv --store_html
```

---


## 💻 Modules

| File                | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Module              |
|:--------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------|
| config.toml         | This code snippet provides the core functionalities for preprocessing HTML code. It removes unwanted content such as specified tags, classes, and IDs, reducing the cost of using the OpenAI API. Additionally, it includes configuration parameters related to the Nimble API for rendering and the OpenAI API for specifying the models to be used.                                                                                                                                            | config/config.toml  |
| secrets.toml        | The provided code snippet contains a configuration file that sets up variables for username, password, and OpenAI API key. The "username" and "password" variables can be filled in with relevant login credentials. The "api_key" variable is also provided and should be populated with the appropriate OpenAI API key.                                                                                                                                                | config/secrets.toml |
| config.py           | This code snippet provides a function, `_read_config_file()`, that reads a TOML configuration file and returns its contents as a dictionary. An additional function, `read_config()`, calls `_read_config_file()` twice, once for the main configuration file and once for a secrets file. The code then decodes and returns a base64-encoded credential string from the secrets file. The main purpose of this code is to facilitate reading and retrieving configuration data from TOML files. | config/config.py    |
| main.py             | The provided code snippet is a Python script that performs web scraping on a given set of URLs. It uses libraries like Loguru for logging, tqdm for progress tracking, and pprint for pretty-printing. The code retrieves HTML content from the URLs, extracts specific elements using selectors, and collects product URLs from the pages. It also supports pagination and writes the collected data to an output file or prints it as a formatted table. | main.py             |
| preprocess_html.py | This code snippet provides functions for preprocessing HTML content. It removes unwanted elements such as specified tags, classes, and IDs from the HTML using regular expressions and CSS selectors. It also removes HTML comments and minifies the modified HTML content using the minify_html library. The code snippet includes commented out code that demonstrates how to use these functions to process HTML files in bulk.                                                             | preprocess_html.py |
| nimble.py          | This code snippet defines a function called "hit_nimble_api" that makes a POST request to the Nimble API with specified headers and data. The function utilizes the Tenacity library for retrying failed attempts based on exponential backoff. It also logs any errors using the Loguru library. The response from the API is returned as JSON, and in case of errors, an error message is logged.                                                                                            | nimble.py          |
| llm_html_parser.py | The provided code snippet involves several functionalities. It includes importing necessary libraries, defining a Pydantic model for CSS selectors, calling an API using OpenAI's ChatGPT model, extracting links from HTML using CSS selectors, and obtaining selectors for HTML elements using an API call and Nimble API. Additionally, it also involves storing HTML files if required.                                                                                                    | llm_html_parser.py |
| utils.py           | The provided code snippet includes functions to read input data from CSV, JSON, and TXT files, create a pandas DataFrame from the extracted data, and write the output data to a file of the same format as the input file. It also includes functions for parsing command-line arguments, getting the domain from a URL, and converting a URL to a file title. The code uses the argparse, csv, json, os, re, datetime, urllib.parse, pandas, and loguru libraries for various functionality. | utils.py           |

## ✅ Enhancement opportunities

1. Improving scraping speed for large number of pages by using concurrency.
2. Displaying tokens and cost being consumed for OpenAI API requests.
3. Storing selectors to disk. Can be used for crawling similar pages and also for fine tuning the LLM for better results.
4. Chunking large text input to multiple OpenAI API calls.
5. Automatic selection of GPT models based on token length.

## 🙏 Acknowledgments

- I would like to thank [Nimble](https://www.nimbleway.com/) for organizing this challenge. It was a fun time exploring the Nimble data extraction API's, scraping sites was a breeze and the documentation was comprehensive.
- I would also like to thank [The Web Scraping Club](https://substack.thewebscraping.club?r=u72gk). Your blogs are very well written and I have learned a lot from it.

## 📝 References

Sure! Here are the links converted to Markdown with titles:

- [Nimble API Quick Start Guide](https://docs.nimbleway.com/nimble-api/nimble-api-quick-start-guide)
- [Real-Time URL Request in Nimble API](https://docs.nimbleway.com/nimble-api/nimble-api-quick-start-guide/real-time-url-request)
- [Real-Time URL Request in Nimble API (Web API)](https://docs.nimbleway.com/nimble-api/web-api/real-time-url-request)
- [GitHub Gist: hwchase17/c7b8ea57d75bc340a23913cca8e1668f](https://gist.github.com/hwchase17/c7b8ea57d75bc340a23913cca8e1668f)
- [GitHub: openai/openai-cookbook/examples/api_request_parallel_processor.py](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py)
- [GitHub: openai/openai-cookbook/examples/How_to_count_tokens_with_tiktoken.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)
- [GitHub: openai/openai-cookbook/examples/How_to_handle_rate_limits.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb)
- [Langchain Python Documentation: Extraction](https://python.langchain.com/docs/modules/chains/additional/extraction)
- [Langchain Python Documentation: Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [Langchain Python Documentation: OpenAI Integration](https://python.langchain.com/docs/modules/model_io/models/chat/integrations/openai)
- [AI-Powered Web Scrapers by Nimble Browser](https://substack.thewebscraping.club/p/ai-powered-web-scrapers-nimble-browser)
- [Building a Price Comparison Tool](https://substack.thewebscraping.club/p/building-a-price-comparison-tool)
- [Creating a Scraper with ChatGPT](https://substack.thewebscraping.club/p/create-scraper-with-chatgpt)
- and of course [ChatGPT](https://chat.openai.com)

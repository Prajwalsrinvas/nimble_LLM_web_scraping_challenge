import argparse
import csv
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from loguru import logger


def _read_input(file_path):
    """
    Read the input from the given file based on its extension.
    Supported file types: CSV, JSON, TXT.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    with open(file_path, "r", encoding="utf-8") as file:
        if file_extension == ".csv":
            reader = csv.DictReader(file)
            column_name = reader.fieldnames[0]
            input_data = [row[column_name] for row in reader]
            return input_data

        if file_extension == ".json":
            data = json.load(file)
            return data["start_urls"]

        if file_extension == ".txt":
            input_data = [line.strip() for line in file]
            return input_data

        raise ValueError(f"Unsupported file extension: {file_extension}")


def _create_dataframe(output_data):
    start_urls, product_urls, page_numbers = [], [], []

    # Extract the data from the dictionary
    for start_url, pages in output_data.items():
        for page, urls in pages[0].items():
            for url in urls:
                start_urls.append(start_url)
                product_urls.append(url)
                page_numbers.append(page.split("_")[1])

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(
        {
            "start_url": start_urls,
            "product_url": product_urls,
            "page_number": page_numbers,
        }
    )
    return df


def _write_output(file_path, output_data):
    """
    Write the output data to a file with the same extension as the input file.
    Supported file types: CSV, JSON, TXT.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = os.path.join(
        output_dir, rf"{datetime.now():%Y_%m_%d_%H_%M_%S}_output{file_extension}"
    )

    if file_extension == ".csv":
        df = _create_dataframe(output_data)
        # Save the DataFrame as a CSV file
        df.to_csv(output_file_path, index=False)
    else:
        with open(output_file_path, "w", encoding="utf-8") as file:
            if file_extension == ".json":
                json.dump(output_data, file, indent=4)

            elif file_extension == ".txt":
                # Initialize an empty list to store the product URLs
                product_urls = []

                # Extract the product URLs from the dictionary
                for pages in output_data.values():
                    for urls in pages[0].values():
                        product_urls.extend(urls)

                # Write the product URLs to a text file
                for url in product_urls:
                    file.write(f"{url}\n")

            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")

        logger.info(f"Output file written to: {output_file_path}")


def _parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process start URLs.")
    # Create a mutually exclusive group for start_url and start_urls_file
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--start_url",
        help="URL to be scraped. Scraped product urls will be displayed as a table.",
    )
    group.add_argument(
        "--start_urls_file",
        help="Path to file containing list of URLs. JSON, CSV and TXT files are supported.",
    )
    parser.add_argument(
        "--output_file_name",
        help="Path to file to store scraped product URLs. JSON, CSV and TXT files are supported. If not provided, it is stored in '{Y_m_d_H_M_S}_output.{start_urls_file extension}' by defult",
    )
    parser.add_argument(
        "--max_pages",
        type=int,
        help="Maximum number of pages to be scraped. This overrides default value set in config.toml.",
    )
    parser.add_argument(
        "--store_html",
        action="store_true",
        help="Writes Raw and processed HTML to disk.",
    )
    return parser


def _get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def _convert_url_to_file_title(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Remove invalid characters from domain
    domain = re.sub(r"[^\w\-_.]", "_", domain)

    # Create the file title by combining domain and time
    file_title = f"{domain}_{current_time}"

    return file_title

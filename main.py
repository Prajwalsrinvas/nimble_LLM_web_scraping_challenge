from datetime import datetime
from pprint import pformat

from loguru import logger
from tqdm.auto import tqdm

from config.config import config
from src.llm_html_parser import extract_elements, get_selectors
from src.nimble import hit_nimble_api
from src.utils import (_create_dataframe, _parse_arguments, _read_input,
                       _write_output)


def main():
    # Generate a timestamp or unique identifier for the log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"logs/my_log_file_{timestamp}.log"

    # Configure the Loguru logger to write logs to the new log file
    logger.add(log_file_name)
    parser = _parse_arguments()
    args = parser.parse_args()

    if args.start_url:
        start_urls = [args.start_url]

    elif args.start_urls_file:
        start_urls = _read_input(args.start_urls_file)

    if args.output_file_name:
        output_file_name = args.output_file_name
    else:
        output_file_name = args.start_urls_file

    max_pages = args.max_pages if args.max_pages else config["nimble"]["max_pages"]

    logger.debug(f"start_urls={pformat(start_urls)}")

    for index, url in enumerate(tqdm(start_urls), start=1):
        all_urls = {url: []}
        current_urls = {}
        all_urls_count = 0
        logger.info(f"Scraping {url=}")
        selectors, html = get_selectors(url, args.store_html)
        if selectors is None:
            continue
        logger.debug(f"selectors={pformat(selectors)}")

        product_urls, pagination_urls = extract_elements(url, html, selectors)

        # remove duplicates while maintaining order
        product_urls = list(dict.fromkeys(product_urls))
        logger.info(f"Found {len(product_urls)} product urls in current page")
        all_urls_count += len(product_urls)

        current_urls[f"page_{index}_urls"] = product_urls

        pagination_urls = list(dict.fromkeys(pagination_urls))
        logger.info(f"Found {len(pagination_urls)} pagination urls")

        max_pagination_urls = pagination_urls[: max_pages - 1]
        logger.debug(f"Scraping {len(max_pagination_urls)} more pages")

        for index, pagination_url in enumerate(max_pagination_urls, start=2):
            logger.info(f"Scraping {pagination_url=}")
            html = hit_nimble_api(pagination_url)
            product_urls, _ = extract_elements(url, html, selectors)
            product_urls = list(dict.fromkeys(product_urls))
            logger.info(f"Found {len(product_urls)} product urls in current page")
            all_urls_count += len(product_urls)
            current_urls[f"page_{index}_urls"] = product_urls
        all_urls[url].append(current_urls)
        logger.info(f"Found {all_urls_count} product urls in total")

    if output_file_name:
        _write_output(output_file_name, all_urls)
    else:
        df = _create_dataframe(all_urls)
        print(df.to_markdown(index=False, tablefmt="rounded_grid"))


if __name__ == "__main__":
    main()

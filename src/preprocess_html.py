import re

from bs4 import BeautifulSoup, Comment
from minify_html import minify_html

from config.config import config

preprocess_html_config = config["preprocess_html"]


def _remove_unwanted_elements(soup):
    for tag in soup.find_all(preprocess_html_config["remove_tags"]):
        tag.decompose()

    class_pattern = re.compile(
        rf'\b.*({"|".join(map(re.escape, preprocess_html_config["remove_classes"]))}).*\b',
        re.IGNORECASE,
    )

    id_pattern = re.compile(
        rf'\b.*({"|".join(map(re.escape, preprocess_html_config["remove_ids"]))}).*\b',
        re.IGNORECASE,
    )

    for tag in soup.find_all(class_=class_pattern):
        tag.decompose()

    for tag in soup.find_all(id=id_pattern):
        tag.decompose()

    # Remove elements matching the selectors
    for selector in preprocess_html_config["remove_css_selectors"]:
        elements_to_remove = soup.select(selector)
        for element in elements_to_remove:
            element.decompose()


def _remove_comments(soup):
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()


def _minify_html_content(html):
    return minify_html.minify(html, minify_js=True, remove_processing_instructions=True)


def _process_html(html):
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted elements
    _remove_unwanted_elements(soup)

    # Remove HTML comments
    _remove_comments(soup)

    # Get the modified HTML
    modified_html = str(soup)

    return _minify_html_content(modified_html)


# files = glob("*.html")


# for file in files:
#     with open(file, encoding="utf-8") as f:
#         html = f.read()

#     with open(f"{file.replace('.html','')}_clean.html", "w", encoding="utf-8") as f:
#         f.write(process_html(html))

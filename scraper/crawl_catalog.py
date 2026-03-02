import requests
from bs4 import BeautifulSoup
import json
import time
import os

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_product_links():
    start = 0
    step = 12
    all_links = set()

    while True:
        url = f"{CATALOG_URL}?start={start}"
        print(f"Fetching start={start}")

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("a", href=True)

        page_links = []

        for a in cards:
            href = a["href"]

            if "/products/product-catalog/view/" in href:
                if "job-solutions" not in href:
                    full_link = BASE_URL + href
                    page_links.append(full_link)

        if not page_links:
            break

        print(f"Found {len(page_links)} links")
        all_links.update(page_links)

        start += step
        time.sleep(1)

    return list(all_links)


def parse_product(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    name_tag = soup.find("h1")
    name = name_tag.text.strip() if name_tag else "N/A"

    description = ""
    meta_desc = soup.find("meta", property="og:description")
    if meta_desc:
        description = meta_desc.get("content", "")

    # Extract test type
    test_type = []
    type_section = soup.find_all("div", class_="product-catalogue__key")

    for t in type_section:
        text = t.get_text(strip=True)
        if text:
            test_type.append(text)

    # Extract duration (if available)
    duration = None
    duration_tag = soup.find(string=lambda x: x and "min" in x.lower())
    if duration_tag:
        try:
            duration = int("".join(filter(str.isdigit, duration_tag)))
        except:
            duration = None

    return {
        "name": name,
        "url": url,
        "description": description,
        "duration": duration,
        "adaptive_support": "Yes",   # default (update if parsed)
        "remote_support": "Yes",     # default (update if parsed)
        "test_type": test_type
    }


def crawl():
    os.makedirs("data/raw", exist_ok=True)

    links = get_product_links()
    print(f"Total product links found: {len(links)}")

    products = []

    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping: {link}")
        product = parse_product(link)

        if product["name"] != "N/A":
            products.append(product)

        time.sleep(0.5)

    print(f"Total products scraped: {len(products)}")

    with open("data/raw/shl_catalog_raw.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    crawl()
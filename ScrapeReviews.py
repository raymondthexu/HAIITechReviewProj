import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging

headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
}

def get_page_html(page_url: str) -> str:
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        logging.error(f"Failed to retrieve data from {page_url}, status code {response.status_code}")
        return ""

def get_reviews_from_html(page_html: str) -> list:
    soup = BeautifulSoup(page_html, "lxml")
    reviews = soup.find_all("div", {"data-hook": "review"})
    if not reviews:
        logging.warning("No reviews found on the page.")
    return reviews

def get_review_details(soup_object: BeautifulSoup) -> str:
    review_text = soup_object.find("span", {"data-hook": "review-body"})
    review_text = review_text.get_text(strip=True) if review_text else "No review text available"
    return review_text

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    url = input("Please enter the Amazon product reviews URL: ")
    URLS = [url]  

    all_results = []
    review_number = 1
    
    for u in URLS:
        logging.info(f"Processing URL: {u}")
        html = get_page_html(u)
        if html:
            reviews = get_reviews_from_html(html)
            for rev in reviews:
                review_text = get_review_details(rev)
                all_results.append({
                    "Review Number": review_number,
                    "Review": review_text
                })
                review_number += 1

    if all_results:
        df = pd.DataFrame(all_results)
        save_name = "SingleProductReview.csv"
        df.to_csv(save_name, index=False)
        logging.info(f"Data saved to {save_name}")
    else:
        logging.info("No data to save.")

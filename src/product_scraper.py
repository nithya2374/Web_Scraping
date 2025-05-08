import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Set up sentiment analyzer
sentiments = SentimentIntensityAnalyzer()

# Function to fetch a single product page asynchronously
async def fetch_product(session, url, url_index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        start_time = time.time()  # Start time for speed tracking
        async with session.get(url, headers=headers, timeout=8) as response:
            duration = time.time() - start_time  # Calculate time taken
            if response.status == 200:
                print(f"✅ Scraped product {url_index + 1} in {duration:.2f} seconds")
                return url_index, url, await response.text(), duration
            else:
                print(f"❌ Failed to fetch {url}, Status Code: {response.status}")
                return url_index, url, None, duration
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return url_index, url, None, 0  # Return 0 duration for failed requests

# Function to extract product details
def extract_product_details(html, url_index, url):
    if not html:
        return {
            "Name": f"Unknown Product {url_index}",
            "Price": "N/A",
            "Rating": "N/A",
            "Positive": 0,
            "Negative": 0,
            "Neutral": 0,
            "Link": f'<a href="{url}" target="_blank">CLICK HERE TO BUY</a>'
        }

    soup = BeautifulSoup(html, "html.parser")

    # Extract product details
    name = soup.find("span", {"id": "productTitle"})
    price = soup.find("span", {"class": "a-price-whole"})
    rating = soup.find("span", {"class": "a-icon-alt"})
    reviews = soup.find_all("span", {"data-hook": "review-body"})

    # Get text values
    name = name.get_text(strip=True) if name else f"Unknown Product {url_index}"
    price = price.get_text(strip=True).replace(",", "") if price else "N/A"

    # Fix rating extraction
    rating_text = rating.get_text(strip=True) if rating else ""
    rating_match = re.search(r"(\d+(\.\d+)?)", rating_text)
    rating = rating_match.group(1) if rating_match else "N/A"

    # Sentiment Analysis
    if reviews:
        sentiment_scores = [sentiments.polarity_scores(review.get_text(strip=True)) for review in reviews]
        avg_sentiment = {
            "Positive": sum(s["pos"] for s in sentiment_scores) / len(sentiment_scores),
            "Negative": sum(s["neg"] for s in sentiment_scores) / len(sentiment_scores),
            "Neutral": sum(s["neu"] for s in sentiment_scores) / len(sentiment_scores)
        }
    else:
        avg_sentiment = {"Positive": 0, "Negative": 0, "Neutral": 0}

    return {
        "Name": name,
        "Price": price,
        "Rating": rating,
        "Positive": avg_sentiment["Positive"],
        "Negative": avg_sentiment["Negative"],
        "Neutral": avg_sentiment["Neutral"],
        "Link": f'<a href="{url}" target="_blank">CLICK HERE TO BUY</a>'
    }

# Async function to scrape all product details in parallel
async def scrape_product_details(urls):
    product_data = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_product(session, url, i) for i, url in enumerate(urls)]
        html_results = await asyncio.gather(*tasks)

    for url_index, url, html, duration in html_results:
        product_info = extract_product_details(html, url_index, url)
        product_data.append(product_info)

    return pd.DataFrame(product_data)

# Wrapper function to run async scraping
def run_scraper(urls):
    start_time = time.time()
    df = asyncio.run(scrape_product_details(urls))
    total_time = time.time() - start_time
    
    # Calculate performance metrics
    avg_time_per_product = total_time / len(urls) if urls else 0
    scraping_speed = len(urls) / total_time if total_time > 0 else 0
    
    print(f"⏳ Total Scraping Time: {total_time:.2f} seconds")
    print(f"⚡ Average Time per Product: {avg_time_per_product:.2f} seconds")
    print(f"🚀 Scraping Speed: {scraping_speed:.2f} products/second")
    
    return df

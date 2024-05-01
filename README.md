# Amazon Review Analysis Tool

## Overview
This tool is designed to perform three main functions: scrape product reviews from Amazon, compute star ratings based on review text sentiment, and analyze reviews to provide category-based ratings. It aims to assist businesses and analysts in understanding customer sentiments and trends from Amazon product reviews.

## Features

### Web Scraping (ScrapeReviews.py)
- **Automated Review Collection**: Automatically scrapes reviews from specified Amazon product pages.
- **Customizable URL input**: Users can input the URL of the Amazon product for which they want to gather reviews.
- Script Adopted from https://gist.github.com/jrjames83/4653d488801be6f0683b91eda8eeb627 
    -  **Changes Made**
        - Output CSV file format 
        - Doesn't require links for each page
        - Error logging

### Star Rating Prediction (StarRating.py)
- **Sentiment Analysis**: Utilizes the Natural Language Toolkit (nltk) and TextBlob libraries to analyze the sentiment of each review and predict a star rating.
- **Model Training**: Includes a pipeline for training a sentiment analysis model on custom datasets.
- **Rating Aggregation**: Computes an overall star rating from individual review sentiments.

### Category Rating (CategoriesRating.py)
- **Category Identification**: Identifies key categories mentioned in reviews using keyword extraction.
- **Category-based Sentiment Scoring**: Scores each category based on the sentiments expressed in the reviews.

## Major Changes

### Challenges
- **Amazon changes webpage markup, affecting HTML content 
- **As a result, previous web scraping script no longer works for new layouts

### Future Challenges
- **Robot Verification systems like CAPTCHA can prevent automated visits to the site
- **Proxy Connection needs to be strong, can be optimized

## Deprecated Code

### No longer used due to changes in Amazon webpage layout
- All files in 'ReviewScraping' folder

## Requirements
- Python 3.9
- Libraries: `pandas`, `numpy`, `nltk`, `sklearn`, `beautifulsoup4`, `requests`

## Installation
To set up the review analysis tool, follow these steps:
```bash
# Clone the repository
git clone https://github.com/your-repo/amazon-review-analysis.git
cd amazon-review-analysis

# Install required Python packages
pip install -r requirements.txt


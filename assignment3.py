import argparse
import urllib.request
import csv
import re
import collections
from datetime import datetime

def download_file(url):
    filename = "weblog.csv"
    urllib.request.urlretrieve(url, filename)
    return filename

def process_csv(filename):
    
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def count_image_requests(data):
    
    image_pattern = re.compile(r".*\.(jpg|png|gif)$", re.IGNORECASE)
    total_requests = len(data)
    image_requests = sum(1 for row in data if image_pattern.match(row[0]))
    percentage = (image_requests / total_requests) * 100
    print(f"Image requests account for {percentage:.2f}% of all requests")

def find_popular_browser(data):
    """Finds the most used browser using regular expressions."""
    browser_counts = collections.Counter()

    for row in data:
        user_agent = row[2].lower()

        if re.search(r"chrome", user_agent):
            browser_counts["Chrome"] += 1
        if re.search(r"firefox", user_agent):
            browser_counts["Firefox"] += 1
        if re.search(r"internet explorer", user_agent):
            browser_counts["Internet Explorer"] += 1
        if re.search(r"safari", user_agent) and not re.search(r"chrome", user_agent):
            browser_counts["Safari"] += 1

    most_common = browser_counts.most_common(1)[0]
    print(f"The most popular browser is {most_common[0]} with {most_common[1]} hits.")


def main(url):
    print(f"Running main with URL = {url}...")
    filename = download_file(url)
    data = process_csv(filename)

    count_image_requests(data)
    find_popular_browser(data)
    

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

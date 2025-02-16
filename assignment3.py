import argparse
import urllib.request
import csv
import re
from collections import Counter

def fetch_log_data(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8').splitlines()

def parse_log_entries(log_entries):
    reader = csv.reader(log_entries)
    structured_data = []
    
    for record in reader:
        if len(record) == 5:
            structured_data.append({
                "file_path": record[0],
                "timestamp": record[1],
                "user_agent": record[2],
                "http_status": record[3],
                "file_size": record[4]
            })
    return structured_data

def analyze_image_requests(entries):
    image_regex = re.compile(r'.*\.(jpg|gif|png)$', re.IGNORECASE)
    
    total_hits = len(entries)
    image_hits = sum(1 for item in entries if image_regex.match(item["file_path"]))
    
    proportion = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Image-related requests constitute {proportion:.2f}% of total requests.")

def identify_top_browser(entries):
    browser_signatures = {
        "Firefox": re.compile(r'Firefox'),
        "Chrome": re.compile(r'Chrome'),
        "IE": re.compile(r'MSIE|Trident'),
        "Safari": re.compile(r'Safari(?!.*Chrome)')
    }
    
    browser_distribution = Counter()
    
    for item in entries:
        agent_info = item["user_agent"]
        for browser, regex in browser_signatures.items():
            if regex.search(agent_info):
                browser_distribution[browser] += 1
                break
    
    top_browser = browser_distribution.most_common(1)
    if top_browser:
        print(f"Leading browser of the day: {top_browser[0][0]}")
    else:
        print("No valid browser data detected.")

def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='Provide the URL for the log file')
    args = parser.parse_args()
    
    log_entries = fetch_log_data(args.url)
    structured_entries = parse_log_entries(log_entries)
    
    analyze_image_requests(structured_entries)
    identify_top_browser(structured_entries)

if __name__ == "__main__":
    execute()

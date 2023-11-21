import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

headers = {
    "authority":"www.hindustantimes.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-IN,en;q=0.9,gu-IN;q=0.8,gu;q=0.7,en-GB;q=0.6,en-US;q=0.5",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Safari/537.36"

}

def scrape_artical(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the title of the website
            raw_title = soup.title.text.strip()

            # Use regex to extract text before the first "-" or "|"
            match = re.search(r'[^-|]+', raw_title)

            if match:
                title = match.group().strip()
            else:
                title = raw_title

            # Try to find the og:image meta tag
            og_image_tag = soup.find('meta', {'property': 'og:image'})

            if og_image_tag and 'content' in og_image_tag.attrs:
                img_url = urljoin(url, og_image_tag['content'])
                return title, img_url
            else:
                return title, None

        else:
            return "Failed to retrieve the website content.", None
    
    except Exception as e:
            return "Failed to retrieve the website content.", None
from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re

try:
    user_url = input('Enter Target URL To Scan: ')

    urls = deque([user_url])
    scraped_uris = set()
    emails = set()

    count = 0
    while urls and count < 100:
        url = urls.popleft()

        if url in scraped_uris:
            continue

        scraped_uris.add(url)

        print('Processing URL #%d: %s' % (count + 1, url))
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            continue

        emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', response.text, re.I))

        soup = BeautifulSoup(response.text, features="lxml")

        for a_tag in soup.find_all('a'):
            new_url = a_tag.get('href')
            if new_url and not new_url.startswith('http'):
                new_url = urllib.parse.urljoin(url, new_url)
            urls.append(new_url)

        count += 1

except KeyboardInterrupt:
    print('\nProgram interrupted by user.')

print('\nScan completed. Emails found:')
for email in emails:
    print(email)

import os
import re
import requests
import yaml
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
CX = os.getenv('CX')

# Load settings from settings.yaml
with open('settings.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)

QUERY = config['QUERY']
MAX_RESULTS = config['MAX_RESULTS']
RESULTS_PER_PAGE = config['RESULTS_PER_PAGE']
OUTPUT_FILE = config['OUTPUT_FILE']

def clean_title(title: str) -> str:
    # Remove suffix after dash or en dash
    cleaned = re.split(r'–|-', title)[0].strip()
    # Replace commas with spaces to preserve CSV integrity
    return cleaned.replace(',', ' ')

def clean_url(link: str) -> str:
    parsed = urlparse(link)

    # Special handling for t.me links
    if parsed.netloc == 't.me':
        path_parts = parsed.path.strip('/').split('/')
        if path_parts and path_parts[0] == 's':
            path_parts.pop(0)
        if path_parts:
            new_path = '/' + path_parts[0]
        else:
            new_path = ''
        parsed = parsed._replace(path=new_path)

    # Remove query and fragment
    parsed = parsed._replace(query='', fragment='')
    return urlunparse(parsed)

# Store unique links
seen_links = set()

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('GROUP_NAME,GROUP_URL\n')  # Write CSV header

    for start in range(1, MAX_RESULTS + 1, RESULTS_PER_PAGE):
        url = (
            f'https://www.googleapis.com/customsearch/v1'
            f'?q={QUERY}&key={API_KEY}&cx={CX}&start={start}&num={RESULTS_PER_PAGE}'
        )

        response = requests.get(url)

        if response.status_code != 200:
            print(f'Ошибка при запросе с start={start}: {response.status_code} - {response.text}')
            break

        items = response.json().get('items', [])
        if not items:
            print(f'Нет результатов при start={start}')
            break

        for item in items:
            raw_link = item.get('link', '')
            cleaned_link = clean_url(raw_link)

            if cleaned_link in seen_links:
                continue

            seen_links.add(cleaned_link)

            title = clean_title(item.get('title', 'Без названия'))
            # Write line in CSV-safe format
            f.write(f'{title},{cleaned_link}\n')

print(f'✅ Результаты записаны в {OUTPUT_FILE}')

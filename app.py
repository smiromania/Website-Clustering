import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import imagehash
import os
from tqdm import tqdm



# Vars
PARQUET_FILE = 'logos.snappy.parquet'
OUTPUT_DIR = 'logos'
HASH_THRESHOLD = 5  # Lower = more strict

# LOAD WEB LINKS
df = pd.read_parquet(PARQUET_FILE)
urls = df['domain'].dropna().unique().tolist()
urls = ['https://' + domain.strip() for domain in urls]


# EXTRACT LOGO FROM A WEBSITE
def find_logo_url(site_url):
    try:
        response = requests.get(site_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for <link rel="icon"> or similar
        icons = soup.find_all('link', rel=lambda x: x and 'icon' in x.lower())
        if icons:
            icon_href = icons[0].get('href')
            if icon_href:
                if icon_href.startswith('//'):
                    return 'http:' + icon_href
                elif icon_href.startswith('http'):
                    return icon_href
                else:
                    return requests.compat.urljoin(site_url, icon_href)
        # fallback: try finding img with "logo" in class or id
        img = soup.find('img', {'class': lambda x: x and 'logo' in x.lower()})
        if img and img.get('src'):
            return requests.compat.urljoin(site_url, img['src'])
    except Exception as e:
        pass
    return None

# DOWNLOAD AND HASH LOGO
def download_and_hash_image(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content)).convert('RGB')
        hash_val = imagehash.phash(image)
        return image, hash_val
    except Exception as e:
        return None, None

# HASH
os.makedirs(OUTPUT_DIR, exist_ok=True)
logo_data = []

print("Extracting and hashing logos...")
for url in tqdm(urls):
    logo_url = find_logo_url(url)
    if logo_url:
        img, hash_val = download_and_hash_image(logo_url)
        if img and hash_val:
            filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
            img_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
            img.save(img_path)
            logo_data.append({'url': url, 'hash': hash_val, 'path': img_path})

# CLUSTERING BASED ON HASH DISTANCE
def group_by_similarity(logo_data, threshold=HASH_THRESHOLD):
    groups = []
    used = set()

    for i, item1 in enumerate(logo_data):
        if i in used:
            continue
        group = [item1]
        used.add(i)
        for j, item2 in enumerate(logo_data[i+1:], start=i+1):
            if j in used:
                continue
            dist = item1['hash'] - item2['hash']
            if dist <= threshold:
                group.append(item2)
                used.add(j)
        groups.append(group)
    return groups

groups = group_by_similarity(logo_data)

# SAVE FILE
with open('grouped_logos.txt', 'w') as f:
    for i, group in enumerate(groups, 1):
        f.write(f"\n--- Group {i} ---\n")
        for item in group:
            f.write(f"{item['url']}  |  {item['path']}\n")

print(f"Done! Found {len(groups)} groups. Results saved in 'grouped_logos.txt'.")

import json
import os
import re
from time import sleep

import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

cookies = {
    'TiPMix': '33.062219816351714',
    'x-ms-routing-name': 'self',
    'ASP.NET_SessionId': 'fvfacthdbhpyrzbmlco2konk',
    'ARRAffinity': 'cd96875fc303e27007d9c206602ea27bf1feed32164e2807972e120f5aafec02',
    'ARRAffinitySameSite': 'cd96875fc303e27007d9c206602ea27bf1feed32164e2807972e120f5aafec02',
    '_culture': 'en-GB',
}

root_url = 'https://legislation.mt/'
file_name = 'all_links.jsonp'

# json per line

all_pdfs = []
with open(file_name, 'r') as f:
    for line in f:
        data = json.loads(line)
        url = data['URL']
        all_pdfs.append({'url': url})

p_bar = tqdm(all_pdfs)
for pdf in p_bar:
    url = pdf['url']
    target_file_name = f'./pdfs/{url.replace("/", "-")}.pdf'
    if os.path.exists(target_file_name):
        # print('Skipped!')
        p_bar.set_description_str(f'{url} skipped')
        continue
    target_url = f'https://legislation.mt/{url}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        # 'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://legislation.mt',
        'Connection': 'keep-alive',
        'Referer': 'https://legislation.mt/Legislation',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    response = requests.get(target_url, headers=headers, cookies=cookies)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find_all('script')
    for s in script:
        if 'SuggestionsToShow = {' in s.text:
            # print(s.text)
            match = re.search(r"SnapshotId:\s*'(\w+)'", s.text)
            if not match:
                print('No match!')
                p_bar.set_description_str(f'{url} No SnapshotId')
                continue
            snapshot_id = match.group(1)
            target_url = f'https://legislation.mt/getpdf/{snapshot_id}'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            p_bar.set_description_str(f'Retrieving {url}')
            response = requests.get(
                target_url, headers=headers, cookies=cookies)
            response.raise_for_status()
            with open(target_file_name, 'wb') as f:
                f.write(response.content)
    # print(pdf)
    p_bar.set_description_str(f'Waiting after retrieving {url}')
    sleep(2)

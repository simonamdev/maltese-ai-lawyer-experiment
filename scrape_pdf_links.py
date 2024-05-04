import json
import requests
import math
from tqdm import tqdm
import time

cookies = {
    'TiPMix': '33.062219816351714',
    'x-ms-routing-name': 'self',
    'ASP.NET_SessionId': 'fvfacthdbhpyrzbmlco2konk',
    'ARRAffinity': 'cd96875fc303e27007d9c206602ea27bf1feed32164e2807972e120f5aafec02',
    'ARRAffinitySameSite': 'cd96875fc303e27007d9c206602ea27bf1feed32164e2807972e120f5aafec02',
    '_culture': 'en-GB',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://legislation.mt',
    'Connection': 'keep-alive',
    'Referer': 'https://legislation.mt/Legislation',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data_to_send = {
    "draw": "5",
    "columns[0][data]": "",
    "columns[0][name]": "",
    "columns[0][searchable]": "true",
    "columns[0][orderable]": "false",
    "columns[0][search][value]": "",
    "columns[0][search][regex]": "false",
    "columns[1][data]": "ItemType",
    "columns[1][name]": "",
    "columns[1][searchable]": "true",
    "columns[1][orderable]": "true",
    "columns[1][search][value]": "",
    "columns[1][search][regex]": "false",
    "columns[2][data]": "Chapter",
    "columns[2][name]": "",
    "columns[2][searchable]": "true",
    "columns[2][orderable]": "true",
    "columns[2][search][value]": "",
    "columns[2][search][regex]": "false",
    "columns[3][data]": "ChapterTitle",
    "columns[3][name]": "",
    "columns[3][searchable]": "true",
    "columns[3][orderable]": "true",
    "columns[3][search][value]": "",
    "columns[3][search][regex]": "false",
    "columns[4][data]": "",
    "columns[4][name]": "",
    "columns[4][searchable]": "true",
    "columns[4][orderable]": "false",
    "columns[4][search][value]": "",
    "columns[4][search][regex]": "false",
    "order[0][column]": "0",
    "order[0][dir]": "asc",
    "start": "0",
    "length": "200",
    "search[value]": "",
    "search[regex]": "false",
    "search[SearchString]": "",
    "search[SearchOn]": "Whole+Phrase",
    "search[SearchBy]": "Title",
    "search[WholeWordSetting]": "false",
    "search[SearchType]": "CONS,SL,ACTS,LEGALNOTICES,BYELAWS",
    "search[ContentSortSetting]": "false",
    "search[IsCustomSort]": "false"
}


def request_links(start: int) -> dict:
    data_to_send['start'] = str(start)
    # print(f'Requesting from https://legislation.mt/Search/SearchFinal with start value {start}')
    response = requests.post('https://legislation.mt/Search/SearchFinal',
                             cookies=cookies, headers=headers, data=data_to_send)
    data = json.loads(response.text)
    # print(data)
    return data


print('Requesting data to determine page count...')
initial_data = request_links(0)
total_record_count = initial_data['recordsFiltered']
page_count = int(math.ceil(float(total_record_count) / 200.0))
print(f'Page Count: {page_count}')

with open('all_links.jsonp', 'a') as f:
    p_bar = tqdm(range(0, page_count + 1))
    for i in p_bar:
        start = i * 200
        p_bar.set_description_str(f'Start Value {start}')
        data = request_links(start)
        for d in data['data']:
            f.write(f'{json.dumps(d)}\n')
        time.sleep(10)

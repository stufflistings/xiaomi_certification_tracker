#!/usr/bin/env python3.7
"""wi-fi.org scrapper that gets Xiaomi devices info"""

from os import rename, path
from bs4 import BeautifulSoup
from requests import get

import extra

# backup
if path.exists('data/wifi.md'):
    rename('data/wifi.md', 'data/wifi_old.md')

# scrap
DATA = BeautifulSoup(get(
    'https://www.wi-fi.org/product-finder-results?' +
    'sort_by=certified&sort_order=desc&keywords=Xiaomi&items=150').content,
                     'html.parser').find("ul", {"class": "result-list"}).findAll("li")
with open('data/wifi.md', 'w') as o:
    o.write("| Product | Model | Type | Date | Certification |" + '\n')
    o.write("|---|---|---|---|---|" + '\n')
    for i in DATA:
        product = i.find("div", {"class": "details"}).findAll("span")[0]['title']
        model = i.find("div", {"class": "details"}).findAll("span")[1]['title']
        type_ = i.find("div", {"class": "details"}).findAll("span")[3]['title']
        date = i.find("div", {"class": "details"}).findAll("span")[4]['title']
        link = i.find("a", {"class": "download-cert"})['href']
        o.write("|{}|{}|{}|{}|[Here]({})|".format(product, model, type_, date, link) + '\n')

# diff
extra.compare('data/wifi_old.md', 'data/wifi.md')

# post
with open('data/wifi_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        product = data[1]
        model = data[2]
        type_ = data[3]
        date = data[4]
        link = data[5]
        if '2019' not in date:
            print('This is not a new device')
            continue
        telegram_message = "New Wi-Fi Alliance Certificate detected! \n" \
                           "*Name:* `{}`\n" \
                           "*Model:* `{}`\n" \
                           "*Type:* `{}`\n" \
                           "*Date:* `{}`\n" \
                           "*Certification:* {}\n"\
            .format(product, model, type_, date, link)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('wifi.md')

import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

pages = range(1, 17)
months = ['Gen', 'Feb', 'Mar','Apr', 'Mag', 'Giu','Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
all_episodes = []
data = []

def replace_month(date):
    [day, month_str, year] = date.split(" ")
    month = months.index(month_str) + 1
    parsed_date = f"{day}/{month}/{year}"
    ts = datetime.strptime(parsed_date, "%d/%m/%Y").timestamp()
    return [parsed_date, ts]
    
for page in pages:
    response = requests.get(f"https://www.ilpost.it/podcasts/morning/page/{page}/")
    parsed = BeautifulSoup(response.text, "html.parser")
    elements = parsed.select("[aria-label='Play']")
    for el in elements:
        try:
            url = unidecode(el["data-url"])
            desc = unidecode(el["data-desc"])
            title = unidecode(el["data-title"])
            [date, timestamp] = replace_month(desc.split(" - ")[0])
            [ep_number, *ep_title] = title.split(" - ")
            ep_title = " - ".join(ep_title)
            ep_number = int(ep_number.replace("Ep.", ""))
            episode = {
                "URL": url,
                "title": ep_title,
                "date": date,
                "raw_date": desc,
                "timestamp": timestamp,
                "number": ep_number
            }
            data.append(episode)
            all_episodes.append([url, desc])
        except Exception as e:
            print(e)
            pass

open(f"./episodes/episodes.json", "w").write(json.dumps(data, indent=2))
for episode in all_episodes:
    [url, desc] = episode
    filename = f"{desc}.mp3"
    response = requests.get(url)
    open(f"./episodes/{filename}", "wb").write(response.content)

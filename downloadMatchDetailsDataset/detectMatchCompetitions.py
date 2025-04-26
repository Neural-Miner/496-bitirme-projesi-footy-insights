import requests
from bs4 import BeautifulSoup
import re
import json
import os

def formatTeamName(teamName):
    words = teamName.split(" ")

    # (Buyuk Harf).(Buyuk Harf). formatina uyan kelimeler
    pattern = re.compile(r"^[A-Z]\.[A-Z]\.$")

    formatted_words = []
    for word in words:
        if word == "A.Ş." or pattern.match(word):
            formatted_words.append(word.upper())
        else:
            formatted_words.append(word.capitalize())

    return " ".join(formatted_words)

# TFF sitesinden macin kadrosunu cekebilmek icin
def fetchMatchInfo(season):
    url = "https://www.tff.org/default.aspx?pageID=545"   # tff arsiv

    # Send an HTTP GET request to fetch the page content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print("Veriler çekilemedi. Hata Kodu:", response.status_code)
        return None
    
    with open("fetched_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content saved to fetched_page.html")

    # Parse the HTML content
    soupObject = BeautifulSoup(response.text, "html.parser")

    link = soupObject.find('a', href=True, string=lambda x: x and season in x)

    if not link:
    # Tüm <a> etiketlerini tara ve içindeki <font> gibi alt etiketleri kontrol et
        all_links = soupObject.find_all('a', href=True)
        for a_tag in all_links:
            font_tag = a_tag.find('font')  # <font> etiketi varsa bul
            if font_tag and season in font_tag.text:
                link = a_tag
                break

    # Link of the season
    if link:
        seasonURL = link['href']
        # print(f"{season} sezonuna ait link: {seasonURL}")
    else:
        print(f"{season} sezonuna ait bir bağlantı bulunamadı.")

    # Fetch the HTML of season
    response = requests.get(seasonURL, headers=headers)
    # Check if the request was successful
    if response.status_code != 200:
        print("Veriler çekilemedi. Hata Kodu:", response.status_code)
        return None
    
    with open("fetched_page_2.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    # print("HTML content saved to fetched_page_2.html")
    
    # Parse the HTML content
    soupObject = BeautifulSoup(response.text, "html.parser")
    
    # Find all 'td' elements with the week information
    weekElements = soupObject.find_all('td', class_='belirginYazi')

    matchLink = None
    weekText = None
    firstTeamExtracted = None
    secondTeamExtracted = None

    for weekElement in weekElements:
        weekText = weekElement.text.strip()

        # print(weekText)
        # Find the parent element of the week
        parentTable = weekElement.find_parent('table', class_='softBG')

        if parentTable:
            rows = parentTable.find_all('tr')
            for row in rows:
                cells = row.find_all('a')
                if len(cells) == 3:  # Ensure it's a valid match row
                    firstTeamExtracted = cells[0].text
                    secondTeamExtracted = cells[2].text

                    scoreCell = cells[1].text

                    week = weekText.split('.')[0]

                    homeScore, awayScore = scoreCell.split(" - ")

                    add_match(season, week, formatTeamName(firstTeamExtracted), formatTeamName(secondTeamExtracted), homeScore, awayScore)


def add_match(season, week, home_team, away_team, home_score, away_score):
    jsonFile = "./mac_verileri/matches.json"
    if os.path.exists(jsonFile):
        with open(jsonFile, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Sezon yoksa ekle
    if season not in data:
        data[season] = {}

    # Hafta yoksa ekle
    if week not in data[season]:
        data[season][week] = []

    # Yeni maç bilgisini ekle
    match_info = {
        "homeTeam": home_team,
        "awayTeam": away_team,
        "homeScore": home_score,
        "awayScore": away_score,
    }

    # Listeye ekle
    data[season][week].append(match_info)

    # JSON dosyasına yaz
    with open(jsonFile, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"{season} Sezonu, {week}. Hafta: {home_team} {home_score}-{away_score} {away_team} eklendi!")


seasons = ['2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023', '2023-2024']

for s in seasons:
    fetchMatchInfo(s)
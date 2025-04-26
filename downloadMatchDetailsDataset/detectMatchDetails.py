import webbrowser
import requests
from bs4 import BeautifulSoup
import unicodedata
#from fuzzywuzzy import fuzz
import re
import json

def processStringToSet(s):
    cleanedString = [char for char in s.strip().lower() if re.match(r'[a-zA-ZçÇğĞıİöÖşŞüÜ]', char)]
    return sorted(cleanedString)

def extract_team_data(soup, team_key, team_id_prefix, takimAdi, macDetaylari):
    # Team Name
    macDetaylari["takimlar"][team_key]["takimAdi"].append(takimAdi)

    score_element = None
    if team_key == "takim_1":
        score_element = soup.select_one('span[id$="_lblTakim1Skor"]')
    elif team_key == "takim_2":
        score_element = soup.select_one('span[id$="_Label12"]')

    macDetaylari["takimlar"][team_key]["skor"].append(score_element.text.strip())

    # Starting 11
    players = soup.select(f'a[id*="_{team_id_prefix}_rptKadrolar"]')
    for player in players:
        player_name = player.text.strip()
        jersey_number = player.find_previous('span').text.strip()
        jersey_number = jersey_number[:-1] if jersey_number.endswith('.') else jersey_number
        macDetaylari["takimlar"][team_key]["ilk11"].append({
            "oyuncuAdi:": player_name,
            "formaNo": jersey_number
        })

    # Substitutes
    substitutes = soup.select(f'a[id*="_{team_id_prefix}_rptYedekler"]')
    for substitute in substitutes:
        player_name = substitute.text.strip()
        jersey_number = substitute.find_previous('span').text.strip()
        jersey_number = jersey_number[:-1] if jersey_number.endswith('.') else jersey_number
        macDetaylari["takimlar"][team_key]["yedekler"].append({
            "oyuncuAdi:": player_name,
            "formaNo": jersey_number
        })

    # Technical Staff
    technical_staff = soup.select(f'a[id*="_{team_id_prefix}_rptTeknikKadro_ctl01_lnkTeknikSorumlu"]')
    for staff in technical_staff:
        macDetaylari["takimlar"][team_key]["teknikSorumlu"].append(staff.text.strip())

    # Cards
    cards = soup.select(f'a[id*="_{team_id_prefix}_rptKartlar"]')
    for card in cards:
        player_name = card.text.strip()
        card_type = card.find_previous('img')['alt']
        minute = card.find_next('span').text.strip()
        macDetaylari["takimlar"][team_key]["kartlar"].append({
            "oyuncu": player_name,
            "kartTuru": card_type,
            "dakika": minute
        })

    # Substituted Out Players
    outgoing_players = soup.select(f'a[id*="_{team_id_prefix}_rptCikanlar"]')
    for player in outgoing_players:
        player_name = player.text.strip()
        minute = player.find_next('span').text.strip()
        macDetaylari["takimlar"][team_key]["oyundanCikanlar"].append({
            "oyuncu": player_name,
            "dakika": minute
        })

    # Substituted In Players
    incoming_players = soup.select(f'a[id*="_{team_id_prefix}_rptGirenler"]')
    for player in incoming_players:
        player_name = player.text.strip()
        minute = player.find_next('span').text.strip()
        macDetaylari["takimlar"][team_key]["oyunaGirenler"].append({
            "oyuncu": player_name,
            "dakika": minute
        })

    # Goller
    goals = soup.select(f'a[id*="_{team_id_prefix}_rptGoller"]')
    for goal in goals:
        # regex kullanarak
        match = re.match(r"^(.*?),(\d+\+?\d*\.dk) \((.*?)\)$", goal.text.strip())

        if match:
            player_name = match.group(1)
            goal_minute = match.group(2)
            goal_type = match.group(3)

            macDetaylari["takimlar"][team_key]["goller"].append({
                "oyuncu": player_name,
                "dakika": goal_minute,
                "golTipi": goal_type
            })


# TFF sitesinden macin kadrosunu cekebilmek icin
def fetchMatchInfo(season, week, firstTeam, secondTeam):
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
        print(f"{season} sezonuna ait link: {seasonURL}")
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
    print("HTML content saved to fetched_page_2.html")
    
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

        if weekText == week:
            # Find the parent element of the week
            parentTable = weekElement.find_parent('table', class_='softBG')

            if parentTable:
                rows = parentTable.find_all('tr')
                for row in rows:
                    cells = row.find_all('a')
                    if len(cells) == 3:  # Ensure it's a valid match row
                        firstTeamExtracted = cells[0].text
                        secondTeamExtracted = cells[2].text

                        #print("Score deneme ", cells[1])
                        
                        inputTeams = [processStringToSet(firstTeam), processStringToSet(secondTeam)]
                        extractedTeams = [processStringToSet(firstTeamExtracted), processStringToSet(secondTeamExtracted)]

                        # print(type(firstTeamExtracted))
                        # print(type(firstTeam))

                        # for i in inputTeams:
                        #     print(f"Input: {i} - Length: {len(i)}")
                        # for i in extractedTeams:
                        #     print(f"Extracted: {i} - Length: {len(i)}")

                        if sorted(inputTeams) == sorted(extractedTeams):  # Match the teams
                            print("Match found!")
                            scoreCell = cells[1]  # The middle cell contains the score
                            matchLink = scoreCell.get('href')  # Extract the href
                            break
                if matchLink:  # If the match is found, exit the loop
                    break

    if matchLink:
        matchLink = "https://www.tff.org" + matchLink
        print(f"The detailed link for the match between {firstTeam} and {secondTeam} is: {matchLink}")
    else:
        print("No link was found for the specified teams.")


        # Kadro bilgisini alma

    # Fetch the HTML of specified match
    response = requests.get(matchLink, headers=headers)
    # Check if the request was successful
    if response.status_code != 200:
        print("Veriler çekilemedi. Hata Kodu:", response.status_code)
        return None
    
    with open("fetched_page_3.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content saved to fetched_page_3.html")
    
    # Parse the HTML content
    soupObject = BeautifulSoup(response.text, "html.parser")


    macDetaylari = {
        "sezon": [],
        "hafta": [],
        "takimlar": {
            "takim_1": {
                "takimAdi": [],
                "skor": [],
                "ilk11": [],
                "yedekler": [],
                "teknikSorumlu": [],
                "kartlar": [],
                "oyundanCikanlar": [],
                "oyunaGirenler": [],
                "goller": []
            },
            "takim_2": {
                "takimAdi": [],
                "skor": [],
                "ilk11": [],
                "yedekler": [],
                "teknikSorumlu": [],
                "kartlar": [],
                "oyundanCikanlar": [],
                "oyunaGirenler": [],
                "goller": []
            }
        }
    }

    week = week.split('.')[0]

    macDetaylari["sezon"].append(season)
    macDetaylari["hafta"].append(week)

    # Extract data for team 1
    extract_team_data(soupObject, "takim_1", "grdTakim1", firstTeamExtracted, macDetaylari)

    # Extract data for team 2
    extract_team_data(soupObject, "takim_2", "grdTakim2", secondTeamExtracted, macDetaylari)

    # Write to JSON file
    with open(f"{season}_{week}_{firstTeamExtracted}_{secondTeamExtracted}.json", 'w', encoding='utf-8') as json_file:
        json.dump(macDetaylari, json_file, ensure_ascii=False, indent=4)



# season = input("Sezon?")
# week = input("Hafta?") + "" + ".Hafta"
# firstTeam = input("Birinci Takım Adı?")
# secondTeam = input("İkinci Takım Adı?")

season = "2013-2014"
week = "2.Hafta"
firstTeam = "Gençlerbirliği"
secondTeam = "Akhisar Belediye Gençlik ve Spor"

fetchMatchInfo(season, week, firstTeam, secondTeam)
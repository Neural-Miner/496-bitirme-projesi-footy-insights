import webbrowser
import requests
from bs4 import BeautifulSoup
import unicodedata
#from fuzzywuzzy import fuzz

def normalize_string(s):
    return unicodedata.normalize('NFKD', s).strip().casefold()

def string_to_set(s):
    return sorted(s.lower().strip())  # Stringi sıralanmış bir listeye dönüştür

# Flashscore icin
"""
def fetchMatchInfo(season, week, firstTeam, secondTeam):
    seasonURL = f"https://www.flashscore.com/football/turkey/super-lig-{season}/results/"
    print(seasonURL)

    # Send an HTTP GET request to fetch the page content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(seasonURL, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print("Veriler çekilemedi. Hata Kodu:", response.status_code)
        return None
    
    with open("fetched_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content saved to fetched_page.html")

    
    # Parse the HTML content
    soupObject = BeautifulSoup(response.text, "html.parser")

    # Find the specified week
    roundElement = soupObject.find("div", class_="event__round", string=f"Round {week}")
    if not roundElement:
        print(f"Week {week} not found.")
        return None
"""

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
    
    # Search for rows in the table
    # rows = soupObject.find('table', class_='genelBorder fiksturListesiTable').find_all('tr')

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
                        
                        inputTeams = sorted([string_to_set(firstTeam), string_to_set(secondTeam)])
                        extractedTeams = sorted([string_to_set(firstTeamExtracted), string_to_set(secondTeamExtracted)])

                        # print(type(firstTeamExtracted))
                        # print(type(firstTeam))

                        # for i in inputTeams:
                        #     print(f"Input: {i}")
                        # for i in extractedTeams:
                        #     print(f"Extracted: {i}")

                        if inputTeams == extractedTeams:  # Match the teams
                            print("Deneme!!!")
                            scoreCell = cells[1]  # The middle cell contains the score
                            matchLink = scoreCell.get('href')  # Extract the href
                            break
                if matchLink:  # If the match is found, exit the loop
                    break


    print(firstTeamExtracted)
    #print(firstTeam)
    print(secondTeamExtracted)
    #print(secondTeam)
    print(weekText)

    if matchLink:
        print(f"The detailed link for the match between {firstTeam} and {secondTeam} is: {matchLink}")
    else:
        print("No link was found for the specified teams.")


    # for row in rows:
    #     if 'belirginYazi' in row.get('class', []):
    #         currentWeek = row.text.strip()  # Update the current week
    #     elif currentWeek == week:  # If we are in the target week
    #         cells = row.find_all('a')  # Find all <a> tags in the row
    #         if len(cells) == 3:  # Ensure the row has three columns (team1, score, team2)
    #             extractedFirstTeam = cells[0].text.strip()
    #             extractedSecondTeam = cells[2].text.strip()
    #             # Compare team names (case-insensitive and order-independent)
    #             input_teams = {firstTeam.lower(), secondTeam.lower()}
    #             extracted_teams = {extractedFirstTeam.lower(), extractedSecondTeam.lower()}
    #             if input_teams == extracted_teams:
    #                 matchDetailLink = cells[1]['href']  # Extract the match link
    #                 break

    



season = input("Sezon?")
week = input("Hafta?")
firstTeam = input("Birinci Takım Adı?")
secondTeam = input("İkinci Takım Adı?")
fetchMatchInfo(season, week, firstTeam, secondTeam)

# webbrowser.open(seasonURL)


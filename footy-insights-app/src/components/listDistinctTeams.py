import json

def listDistinctTeams(jsonFilePath):
    distinctTeams = set()

    with open(jsonFilePath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Tüm sezonları, haftaları ve maçları dolaş
    for seasonKey, weeksVal in data.items():
        for weekKey, matchesVal in weeksVal.items():
            for matchVal in matchesVal:
                distinctTeams.add(matchVal['homeTeam'])
                distinctTeams.add(matchVal['awayTeam'])

    print("Distinct team count:", len(distinctTeams))
    print("Teams:")
    for team in sorted(distinctTeams):
        print(team)

# Fonksiyonu çağırma örneği
jsonPath = "matches_with_paths_copy.json"
listDistinctTeams(jsonPath)
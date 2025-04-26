import json

match_highlights = []

for year in range(2023, 2009, -1):
    season = f"{year}-{year + 1}"
    if year == 2020:
        weeks = 42
    elif year >= 2019:
        weeks = 38
    else:
        weeks = 34
    for week in range(1, weeks + 1):
        match_highlights.append(
            {
                "season": season,
                "week": str(week),
                "url": f"https://beinsports.com.tr/mac-ozetleri-goller/super-lig/ozet/{season}/{week}",
            }
        )

data = {"match_highlights": match_highlights}

with open("match_highlights.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

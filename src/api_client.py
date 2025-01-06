import requests
import json
import pandas as pd


base_url = "https://edh.ub.uni-heidelberg.de/data/api/inschrift/suche"

params = {
    ## Roman provinces whose dataset of roman inscriptions is complete:
    # "provinz": ["Ach", "AlG", "AlP", "AlC", "AlM", "Bri", "Dac", "Dal", "Epi", "Gel", "GeS", "Mak", "Mol", "MoS", "Nor", "Pal", "PaS", "Rae", "Thr"],
    "inschriftgattung": "titsep",  # value for type of inscription: epitaph
    "jahr_a": "200", # earliest possible timeframe for christian monuments
    "jahr_b": "600", # 
    "limit": 1000000
}


response = requests.get(base_url, params=params)

if response.status_code == 200:
    print("choo choo, you got a response")
    data = response.json()

    # print(json.dumps(data, indent=2, ensure_ascii=False))

    # Save to a JSON file
    with open("data/results.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
    print("Data saved in data/results.json successfully")

    # save as csv file
    # df = pd.DataFrame(data)
    # df.to_csv("data/results.csv", index=False, encoding="utf-8")
    # print("data saved in data/results.csv sucessfully")

else:
    print(f"oh no: {response.status_code}")
    print(response.text)  

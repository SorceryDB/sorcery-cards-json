import pandas as pd
import json
from pprint import pprint as pp
import re

with open("Sorcery Cards - Sheet1.csv") as file:
    df1 = pd.read_csv(file)

df1 = df1.fillna("")

limits = {
    "ordinary" : 4,
    "exceptional" : 3,
    "elite" : 2,
    "unique": 1,
    "token" : 0,
    "": 0

}

def strip_text(s, keep_spaces = False):
    if not keep_spaces:
        s = s.replace(" ", "_").replace('-', '_')
    s = re.sub(r"[^a-zA-Z0-9_]", "", s)
    return s.lower()


#card_id = 40000
position = 1

pack_json = []
printing_json = []

for index, row in df1.iterrows():
    '''
    artist:"Marta Molina"
    card_type_id:"spell",
    cost:2.0,
    deck_limit:4,
    health:"",
    id:"riptide",
    is_unique:false,
    keywords:"",
    lore_text:"",
    noun:"",
    power:1,
    rarity:"Ordinary",
    splash_damage_center:"",
    splash_damage_grid:"",
    splash_damage_total:"",
    stripped_text:"Pull an Avatar or minion to a Water site adjacent to them. Draw a Spell.",
    stripped_type_line:"Ordinary Magic to trap the unwary.",
    sub_type:"",
    super_type:"Spell",
    threshold_granted:"",
    threshold_required:1.0,
    threshold_type:"Water",
    type:"Magic",
    '''

    threshold_granted_earth = row["Threshold Granted Earth"]
    threshold_granted_fire = row["Threshold Granted Fire"]
    threshold_granted_water = row["Threshold Granted Water"]
    threshold_granted_wind = row["Threshold Granted Wind"]

    threshold_required_earth = row["Threshold Required Earth"]
    threshold_required_fire = row["Threshold Required Fire"]
    threshold_required_water = row["Threshold Required Water"]
    threshold_required_wind = row["Threshold Required Wind"]


    card_dict = {
        "card_type_id" : row["Super Type"].lower(),
        "deck_limit": limits[row["Rarity"].lower()],
        "faction_id": "neutral",
        "id": str(row["ID"]),
        "is_unique": False,
        "keywords": row["Keywords"],
        "card_rarity_id": row["Rarity"].lower(),
        "stripped_text": row["Oracle"],
        "stripped title": row["Title"],
        "subtypes": row["Sub Type"],
        "text": row["Oracle"],
        "title": row["Title"],

    }

    if row["Cost"] != "":
        card_dict["cost"] = int(row["Cost"]) if row["Cost"] else 0
    if row["Health"] != "":
        card_dict["health"] = int(row["Health"]) if row["Health"] else 0
    if row["Nouns"] != "":
        card_dict["nouns"] =  row["Nouns"]
    if row["Power"] != "":
        card_dict["power"] =  int(row["Power"]) if row["Power"] else 0


    if row["Splash Damage Grid"] != "":
        card_dict["splash_damage_center"] =  row["Splash Damage Center"]
        card_dict["splash_damage_grid"] =  row["Splash Damage Grid"]
        card_dict["splash_damage_total"] =  row["Splash Damage Total"]

    if row["Threshold Granted Earth"] != "":
        print([threshold_granted_earth, threshold_granted_fire, threshold_granted_water, threshold_granted_wind])
        card_dict["threshold_granted_earth"] =  int(threshold_granted_earth)
        card_dict["threshold_granted_fire"] =  int(threshold_granted_fire)
        card_dict["thresholg_granted_total"] =  int(sum([threshold_granted_earth, threshold_granted_fire, threshold_granted_water, threshold_granted_wind]))
        card_dict["threshold_granted_water"] =  int(threshold_granted_water)
        card_dict["threshold_granted_wind"] =  int(threshold_granted_wind)

    #if row["Threshold Required"] != "":
    #    card_dict["threshold_required"] =  int(row["Threshold Required"]) if row["Threshold Required"] else 0
    #    card_dict["threshold_type"] =  row["Threshold Type"].lower()

    if row["Threshold Required Earth"] != "":
        print([threshold_granted_earth, threshold_granted_fire, threshold_granted_water, threshold_granted_wind])
        card_dict["threshold_required_earth"] =  int(threshold_required_earth)
        card_dict["threshold_required_fire"] =  int(threshold_required_fire)
        card_dict["thresholg_required_total"] =  int(sum([threshold_required_earth, threshold_required_fire, threshold_required_water, threshold_required_wind]))
        card_dict["threshold_required_water"] =  int(threshold_required_water)
        card_dict["threshold_required_wind"] =  int(threshold_required_wind)

    if row["Type"] != "":
        card_dict["type"] =  row["Type"].lower()


    printing_dict = {
        "card_id" : strip_text(row["Title"]),
        "card_set_id": "pksc",
        "flavor": row["Lore Text"],
        "id": str(row["ID"]),
        "illustrator": row["Artist"],
        "position": position, #ascending
        "printed_is_unique": False,
        "printed_text": row["Oracle"],
        "quantity": 1,
        "stripped_printed_text": row["Oracle"]

    }

    pack_dict = {
        "code": str(row["ID"]),
        "cost": int(row["Cost"]) if row["Cost"] else 0,
        "deck_limit": limits[row["Rarity"].lower()],
        "faction_code": "neutral",
        "flavor": row["Lore Text"],
        "illustrator": row["Artist"],
        "keywords": row["Keywords"],
        "nouns": row["Nouns"],
        "pack_code": "pksc",
        "position": position, # ascending
        "power": int(row["Power"]) if row["Power"] else 0,
        "quantity": 1,  # more for precons
        "rarity_code": row["Rarity"].lower(),
        "stripped_text": row["Oracle"],
        "stripped_title": row["Title"],
        "stripped_type_line": row["Type Line"],
        "type_line": row["Type Line"],
        "text": row["Oracle"],
        "title": row["Title"],
        "type_code": row["Super Type"].lower(),
        "uniqueness": False
    }


    print("\n\r")
    print("CARD JSON:")
    print(card_dict)
    with open(rf".\json_exports\cards\{strip_text(row['Title'])}.json", 'w', newline='\n') as file:
        json.dump(card_dict, file, indent=4, sort_keys=True)
    print("PRINTING JSON:")
    print(printing_dict)
    printing_json.append(printing_dict)
    print("PACK JSON:")
    print(pack_dict)
    pack_json.append(pack_dict)
    #card_id += 1
    position += 1

    #if card_id > 40005:
    #    break
with open(rf".\json_exports\printings\pksc.json", 'w', newline='\n') as file:
        json.dump(printing_json, file, indent=4, sort_keys=True)
with open(rf".\json_exports\packs\pksc.json", 'w', newline='\n') as file:
        json.dump(pack_json, file, indent=4, sort_keys=True)




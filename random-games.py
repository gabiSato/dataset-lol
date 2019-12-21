from api import Api
import json
import numpy
import pandas

key = 'LOL_API_KEY'

api = Api('br1', key)
matches = api.get_random_matches()

match_list = []
columns_list = []

for match in matches:
    item = []
    item_name = []
    teams = match['teams']
    participants = match['participants']

    # Criação de variáveis para match
    win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald = 0, 0, 0, 0, 0, 0, 0

    # Loop para lista de teams
    for i in range(2):
        if teams[i]['win'] == 'Win':
            win = i+1
        if teams[i]['firstBlood'] == True:
            firstBlood = i+1
        if teams[i]['firstTower'] == True:
            firstTower = i+i
        if teams[i]['firstInhibitor'] == True:
            firstInhibitor = i+1
        if teams[i]['firstBaron'] == True:
            firstBaron = i+1
        if teams[i]['firstDragon'] == True:
            firstDragon = i+1
        if teams[i]['firstRiftHerald'] == True:
            firstRiftHerald = i+1

    # Adiciona as variáveis na lista
    item.append(win)
    item.append(firstBlood)
    item.append(firstTower)
    item.append(firstInhibitor)
    item.append(firstBaron)
    item.append(firstDragon)
    item.append(firstRiftHerald)
    item_name.append("win")
    item_name.append("first_blood")
    item_name.append("first_tower")
    item_name.append("first_inhibitor")
    item_name.append("first_baron")
    item_name.append("first_dragon")
    item_name.append("first_rift_herald")

    for i in range(2):
        teamId = str(teams[i]['teamId'])
        item.append(teams[i]["towerKills"])
        item.append(teams[i]["inhibitorKills"])
        item.append(teams[i]["baronKills"])
        item.append(teams[i]["dragonKills"])
        item.append(teams[i]["vilemawKills"])
        item.append(teams[i]["riftHeraldKills"])

        item_name.append("tower_kills" + "_team_" + teamId[0])
        item_name.append("inhibitor_kills" + "_team_" + teamId[0])
        item_name.append("baron_kills" + "_team_" + teamId[0])
        item_name.append("dragon_kills" + "_team_" + teamId[0])
        item_name.append("vilemaw_kills" + "_team_" + teamId[0])
        item_name.append("rift_herald_kills" + "_team_" + teamId[0])

    part_keys = [
        "kills_top_team_1",
        "assists_top_team_1",
        "deaths_top_team_1",
        "gold_earned_20m_top_team_1",
        "cs_20m_top_team_1",
        "xp_20m_top_team_1",
        "damege_taken_20m_top_team_1",
        "kills_middle_team_1",
        "assists_middle_team_1",
        "deaths_middle_team_1",
        "gold_earned_20m_middle_team_1",
        "cs_20m_middle_team_1",
        "xp_20m_middle_team_1",
        "damege_taken_20m_middle_team_1",
        "kills_jungle_team_1",
        "assists_jungle_team_1",
        "deaths_jungle_team_1",
        "gold_earned_20m_jungle_team_1",
        "cs_20m_jungle_team_1",
        "xp_20m_jungle_team_1",
        "damege_taken_20m_jungle_team_1",
        "kills_bottom_duo_support_team_1",
        "assists_bottom_duo_support_team_1",
        "deaths_bottom_duo_support_team_1",
        "gold_earned_20m_bottom_duo_support_team_1",
        "cs_20m_bottom_duo_support_team_1",
        "xp_20m_bottom_duo_support_team_1",
        "damege_taken_20m_bottom_duo_support_team_1",
        "kills_bottom_duo_carry_team_1",
        "assists_bottom_duo_carry_team_1",
        "deaths_bottom_duo_carry_team_1",
        "gold_earned_20m_bottom_duo_carry_team_1",
        "cs_20m_bottom_duo_carry_team_1",
        "xp_20m_bottom_duo_carry_team_1",
        "damege_taken_20m_bottom_duo_carry_team_1",
        "kills_top_team_2",
        "assists_top_team_2",
        "deaths_top_team_2",
        "gold_earned_20m_top_team_2",
        "cs_20m_top_team_2",
        "xp_20m_top_team_2",
        "damege_taken_20m_top_team_2",
        "kills_middle_team_2",
        "assists_middle_team_2",
        "deaths_middle_team_2",
        "gold_earned_20m_middle_team_2",
        "cs_20m_middle_team_2",
        "xp_20m_middle_team_2",
        "damege_taken_20m_middle_team_2",
        "kills_jungle_team_2",
        "assists_jungle_team_2",
        "deaths_jungle_team_2",
        "gold_earned_20m_jungle_team_2",
        "cs_20m_jungle_team_2",
        "xp_20m_jungle_team_2",
        "damege_taken_20m_jungle_team_2",
        "kills_bottom_duo_support_team_2",
        "assists_bottom_duo_support_team_2",
        "deaths_bottom_duo_support_team_2",
        "gold_earned_20m_bottom_duo_support_team_2",
        "cs_20m_bottom_duo_support_team_2",
        "xp_20m_bottom_duo_support_team_2",
        "damege_taken_20m_bottom_duo_support_team_2",
        "kills_bottom_duo_carry_team_2",
        "assists_bottom_duo_carry_team_2",
        "deaths_bottom_duo_carry_team_2",
        "gold_earned_20m_bottom_duo_carry_team_2",
        "cs_20m_bottom_duo_carry_team_2",
        "xp_20m_bottom_duo_carry_team_2",
        "damege_taken_20m_bottom_duo_carry_team_2"
    ]

    part_list = []

    # Loop para lista de participants
    for p in participants:
        timeline = p['timeline']
        stats = p['stats']
        teamId = str(p['teamId'])

        lane = timeline["lane"].casefold()

        if timeline["lane"] == "BOTTOM":
            lane = lane + "_" + timeline["role"].casefold()

        part = {}

        key = "kills_" + lane + "_team_" + teamId[0]
        part[key] = stats["kills"]

        key = "assists_" + lane + "_team_" + teamId[0]
        part[key] = stats["assists"]

        key = "deaths_" + lane + "_team_" + teamId[0]
        part[key] = stats["deaths"]

        key = "gold_earned_20m_" + lane + "_team_" + teamId[0]
        part[key] = timeline['goldPerMinDeltas']['10-20'] if 'goldPerMinDeltas' in timeline else 0

        key = "cs_20m_" + lane + "_team_" + teamId[0]
        part[key] = timeline['creepsPerMinDeltas']['10-20'] if 'goldPerMinDeltas' in timeline else 0

        key = "xp_20m_" + lane + "_team_" + teamId[0]
        part[key] = timeline['xpPerMinDeltas']['10-20'] if 'goldPerMinDeltas' in timeline else 0

        key = "damege_taken_20m_" + lane + "_team_" + teamId[0]
        part[key] = timeline['damageTakenPerMinDeltas']['10-20'] if 'goldPerMinDeltas' in timeline else 0

        part_list.append(part)

    for key in part_keys:
        item_name.append(key)
        for part in part_list:
            if key in part:
                item.append(part[key])

    if len(item) == len(item_name):
        match_list.append(item)
        columns_list.append(item_name)

dataset = pandas.DataFrame(match_list)
dataset.sample(3)
dataset.columns = columns_list[0]
dataset.index = pandas.RangeIndex(len(dataset.index))
dataset.to_csv("random-games",index=False)
from api import Api
import json
import numpy
import pandas

key = 'LOL_API_KEY'
api = Api('br1', key)

matches = api.get_all_matches()
match_list = []
columns_list = []

for match in matches:
    item = []
    item_name = []
    matchDto = match
    teams = match['teams']
    participants = match['participants']

    # Deleta campos de Match
    del matchDto['gameCreation'], matchDto['mapId'], matchDto['gameVersion'], matchDto['gameMode'], matchDto['gameType']
    del matchDto['platformId'], matchDto['teams'], matchDto['participants'], matchDto['participantIdentities']

    # Adiciona os campos de Match na lista
    for name, value in matchDto.items():
        item.append(value)
        item_name.append(name)

    # CriaÃ§Ã£o de variÃ¡veis para match
    win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald = 0, 0, 0, 0, 0, 0, 0

    # Loop para lista de teams
    for i in range(2):

        # Verifica que time compÃµe esses atributos
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

        # Deleta campos em cada team
        del teams[i]['bans']
        del teams[i]['win'], teams[i]['firstBlood'], teams[i]['firstTower'], teams[i]['firstInhibitor'], teams[i]['firstBaron']
        del teams[i]['firstDragon'], teams[i]['firstRiftHerald']

    # Adiciona as variÃ¡veis na lista
    item.append(win)
    item.append(firstBlood)
    item.append(firstTower)
    item.append(firstInhibitor)
    item.append(firstBaron)
    item.append(firstDragon)
    item.append(firstRiftHerald)
    item_name.append("win")
    item_name.append("firstBlood")
    item_name.append("firstTower")
    item_name.append("firstInhibitor")
    item_name.append("firstBaron")
    item_name.append("firstDragon")
    item_name.append("firstRiftHerald")

    # Adiciona os campos de cada team na lista
    for name, value in teams[0].items():
        if name != "teamId":
            teamId = str(teams[0]['teamId'])
            item.append(value)
            item_name.append(name + "Team" + teamId[0])

    for name, value in teams[1].items():
        if name != "teamId":
            teamId = str(teams[1]['teamId'])
            item.append(value)
            item_name.append(name + "Team" + teamId[0])

    # CriaÃ§Ã£o de variáveis para match com o id do participante
    firstBloodPartId, firstBloodAssistPartId, firstTowerPartId, firstTowerAssistPartId, firstInhibitorPartId, firstInhibitorAssistPartId = 0, 0, 0, 0, 0, 0

    # Loop para lista de participants
    for p in participants:

        # Separa as listas de dentro de participants
        part = p
        timeline = p['timeline']
        stats = p['stats']

        # Deleta campos em part
        del part['timeline'], part['stats']

        # Verifica a existência de atributos e seta o id do participante nas variáveis
        if "firstBloodAssist" and "firstBloodKill" in stats:
            if stats['firstBloodKill'] == True:
                firstBloodPartId = stats['participantId']
            if stats['firstBloodAssist'] == True:
                firstBloodAssistPartId = stats['participantId']
            del stats['firstBloodAssist'], stats['firstBloodKill']

        if "firstTowerAssist" and "firstTowerKill" in stats:
            if stats['firstTowerKill'] == True:
                firstTowerPartId = stats['participantId']
            if stats['firstTowerAssist'] == True:
                firstTowerAssistPartId = stats['participantId']
            del stats['firstTowerAssist'], stats['firstTowerKill']

        if "firstInhibitorAssist" and "firstInhibitorKill" in stats:
            if stats['firstInhibitorKill'] == True:
                firstInhibitorPartId = stats['participantId']
            if stats['firstInhibitorAssist'] == True:
                firstInhibitorAssistPartId = stats['participantId']
            del stats['firstInhibitorAssist'], stats['firstInhibitorKill']

        # Deleta campos em stats
        del stats['win'], stats['participantId']

        del stats['item0'], stats['item1'], stats['item2'], stats['item3'], stats['item4'], stats['item5'],stats['item6']
        del stats['combatPlayerScore'], stats['objectivePlayerScore'], stats['totalPlayerScore'], stats['totalScoreRank']
        del stats['playerScore0'], stats['playerScore1'], stats['playerScore2'], stats['playerScore3'], stats['playerScore4']
        del stats['playerScore5'], stats['playerScore6'], stats['playerScore7'], stats['playerScore8'], stats['playerScore9']

        del stats['perk0'], stats['perk0Var1'], stats['perk0Var2'], stats['perk0Var3'], stats['perk1'], stats['perk1Var1']
        del stats['perk1Var2'], stats['perk1Var3'], stats['perk2'], stats['perk2Var1'], stats['perk2Var2'], stats['perk2Var3']
        del stats['perk3'], stats['perk3Var1'], stats['perk3Var2'], stats['perk3Var3'], stats['perk4'], stats['perk4Var1']
        del stats['perk4Var2'], stats['perk4Var3'], stats['perk5'], stats['perk5Var1'], stats['perk5Var2'], stats['perk5Var3']
        del stats['perkPrimaryStyle'], stats['perkSubStyle'], stats['statPerk0'], stats['statPerk1'], stats['statPerk2']

        if not "highestAchievedSeasonTier" in part:
            part['highestAchievedSeasonTier'] = "NONE"

        # Adiciona campos de part na lista
        for name, value in part.items():
            if name != "teamId":
                item.append(value)
                if part['teamId'] == 200:
                    partId = str(part['participantId'] - 5)
                    item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + partId + "_" + name)
                else:
                    item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + str(part['participantId']) + "_" + name)

        # Adiciona campos de timeline
        item.append(timeline['lane'] + "/" + timeline['role'])
        if part['teamId'] == 200:
            partId = str(part['participantId'] - 5)
            item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + partId + "_" + "lane/role")
        else:
            item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + str(part['participantId']) + "_" + "lane/role")

        # Adiciona campos de stats na lista
        for name, value in stats.items():
            item.append(value)
            if part['teamId'] == 200:
                partId = str(part['participantId'] - 5)
                item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + partId + "_" + name)
            else:
                item_name.append("T" + str(part['teamId'])[0] + "_" + "P" + str(part['participantId']) + "_" + name)

    # Adiciona as variáveis na lista
    item.append(firstBloodPartId)
    item.append(firstBloodAssistPartId)
    item.append(firstTowerPartId)
    item.append(firstTowerAssistPartId)
    item.append(firstInhibitorPartId)
    item.append(firstInhibitorAssistPartId)
    item_name.append("firstBloodPartId")
    item_name.append("firstBloodAssistPartId")
    item_name.append("firstTowerPartId")
    item_name.append("firstTowerAssistPartId")
    item_name.append("firstInhibitorPartId")
    item_name.append("firstInhibitorAssistPartId")

    match_list.append(item)
    columns_list.append(item_name)

dataset = pandas.DataFrame(match_list)
dataset.sample(12)
dataset.columns = columns_list[0]
dataset.index = pandas.RangeIndex(len(dataset.index))
dataset.to_csv("general-challenger",index=False)
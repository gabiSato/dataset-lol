import requests
import json
import time
from random import seed
from random import randint

class Api:

    def __init__(self, host, key):
        self.host = "https://" + host + ".api.riotgames.com"
        self.key = key
        self.tiers = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
        self.divisions = ["I", "II", "III", "IV"]

    def make_request(self, request):
        url = self.host + request + "?api_key=" + self.key
        response = requests.get(url).json()
        time.sleep(0.5)
        return response

    def make_request_with_params(self, request, params):
        url = self.host + request + params + "&api_key=" + self.key
        response = requests.get(url).json()
        time.sleep(0.5)
        return response

    def get_challenger_by_queue(self, queue):
        request = "/lol/league/v4/challengerleagues/by-queue/" + queue
        return self.make_request(request)

    def get_summoners_by_name(self, name):
        request = "/lol/summoner/v4/summoners/by-name/" + name
        return self.make_request(request)

    def get_matchlists_by_account(self, account_id, params):
        request = "/lol/match/v4/matchlists/by-account/" + account_id
        time.sleep(0.01)
        return self.make_request_with_params(request, params)

    def get_match(self, match_id):
        request = "/lol/match/v4/matches/" + str(match_id)
        return self.make_request(request)

    def get_all_challengers_accounts_id(self, challenger_list):
        account_id_list = []
        for challenger in challenger_list:
            summoner = self.get_summoners_by_name(challenger['summonerName'])
            account_id_list.append(summoner['accountId'])
        return account_id_list

    def get_league_entries(self, tier, division):
        request = "/lol/league/v4/entries/RANKED_SOLO_5x5/" + tier + "/" + division
        return self.make_request_with_params(request, "?page=1")

    def get_all_challengers_matchID(self, challengers_accounts_id, queue, season, qtd):
        params = "?queue=" + queue + "&season=" + season + "&endIndex=" + qtd + "&beginIndex=0"
        matchesID_list = []
        for account in challengers_accounts_id:
            matches = self.get_matchlists_by_account(account, params)
            for match in matches['matches']:
                matchesID_list.append(match['gameId'])
        return matchesID_list

    def get_all_matches_by_matchID(self, matchesID):
        matches = []
        for id in matchesID:
            match = self.get_match(id)
            matches.append(match)
        return matches

    def get_all_matches(self):
        params = "?queue=420&season=13&endIndex=5&beginIndex=0"
        challengers = self.get_challenger_by_queue('RANKED_SOLO_5x5')
        matches = []
        for challenger in challengers['entries']:
            summoner = self.get_summoners_by_name(challenger['summonerName'])
            matchlist = self.get_matchlists_by_account(summoner['accountId'], params)
            for match in matchlist['matches']:
                game = self.get_match(match['gameId'])
                print(json.dumps(game, indent=4, sort_keys=True))
                if game['gameDuration'] >= 1200:
                    matches.append(game)
        return matches

    def get_random_matches(self):
        params = "?queue=420&season=13&endIndex=1&beginIndex=0"
        matches = []
        seed(1)
        for _ in range(1000):
            tier = randint(0, len(self.tiers) - 1)
            division = randint(0, len(self.divisions) - 1)
            summoner_from_division = self.get_league_entries(self.tiers[tier], self.divisions[division])
            summoner = self.get_summoners_by_name(summoner_from_division[0]["summonerName"])
            matchlist = self.get_matchlists_by_account(summoner['accountId'], params)
            game = self.get_match(matchlist['matches'][0]['gameId'])
            print(json.dumps(game, indent=4, sort_keys=True))
            if game['gameDuration'] >= 1200:
                matches.append(game)
        return matches
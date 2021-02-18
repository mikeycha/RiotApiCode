# This script grabs your last played game with information of all players who played in it. Very simple to OP.GG. Uses RiotWatcher and pandas for the data structures 

from riotwatcher import LolWatcher, ApiError
import pandas as pd

# Riot API key is needed to access their API. Easily attainable with a Riot account. 
api_key = "Enter API Key Here"
watcher = LolWatcher(api_key)
region = "na1"

# Enter your summoner name here and it will grab its last played Summoners Rift game
player = "Enter Summoner Name Here"

info = watcher.summoner.by_name(region, player)

player_ranked_stats = watcher.league.by_summoner(region, info['id'])

my_matches = watcher.match.matchlist_by_account(region, info['accountId'])

# fetch last match detail
last_match = my_matches['matches'][0]
match_detail = watcher.match.by_id(region, last_match['gameId'])

participants = []
for row1 in match_detail['participants']:
    participants_row1 = {}
    participants_row1['Champion'] = row1['championId']
    participants_row1['Summoner Spell 1'] = row1['spell1Id']
    participants_row1['Summoner Spell 2'] = row1['spell2Id']
    participants_row1['Kills'] = row1['stats']['kills']
    participants_row1['Deaths'] = row1['stats']['deaths']
    participants_row1['Assists'] = row1['stats']['assists']
    participants_row1['Damage Dealt'] = row1['stats']['totalDamageDealt']
    participants_row1['Gold Earned'] = row1['stats']['goldEarned']
    participants_row1['Level'] = row1['stats']['champLevel']
    participants_row1['CS'] = row1['stats']['totalMinionsKilled'] + row1['stats']['neutralMinionsKilled']
    participants_row1['Item 1'] = row1['stats']['item0']
    participants_row1['Item 2'] = row1['stats']['item1']
    participants_row1['Item 3'] = row1['stats']['item2']
    participants_row1['Item 4'] = row1['stats']['item3']
    participants_row1['Item 5'] = row1['stats']['item4']
    participants_row1['Item 6'] = row1['stats']['item5']
    participants.append(participants_row1)

df1 = pd.DataFrame(participants)

participantIdentities = []

for row2 in match_detail['participantIdentities']:
    participants_row2 = {}
    participants_row2['Summoner'] = row2['player']['summonerName']
    participantIdentities.append(participants_row2)


latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
item_list = watcher.data_dragon.items(latest, 'en_US')
spell_list = watcher.data_dragon.summoner_spells(latest, 'en_US')

champ_dic = {}

for key in champ_list['data']:
    row1 = champ_list['data'][key]
    champ_dic[row1['key']] = row1['id']
for row1 in participants:
    row1['Champion'] = champ_dic[str(row1['Champion'])]

item_names = []
item_ids = []
for name in item_list['data']:
    row1 = item_list['data'][name]
    item_names.append(row1['name'])

item_raw = item_list['data']
for key in item_raw.keys():
    item_ids.append(key)

items = dict(zip(item_ids, item_names))
items['0'] = "None"

for row1 in participants:
    row1['Item 1'] = items[str(row1['Item 1'])]
    row1['Item 2'] = items[str(row1['Item 2'])]
    row1['Item 3'] = items[str(row1['Item 3'])]
    row1['Item 4'] = items[str(row1['Item 4'])]
    row1['Item 5'] = items[str(row1['Item 5'])]
    row1['Item 6'] = items[str(row1['Item 6'])]

spell_dic = {}

for key in spell_list['data']:
    row1 = spell_list['data'][key]
    spell_dic[row1['key']] = row1['name']
for row1 in participants:
    row1['Summoner Spell 1'] = spell_dic[str(row1['Summoner Spell 1'])]
    row1['Summoner Spell 2'] = spell_dic[str(row1['Summoner Spell 2'])]

df1 = pd.DataFrame(participants)
df2 = pd.DataFrame(participantIdentities)

result = pd.concat([df2, df1], axis=1, join="inner")

result

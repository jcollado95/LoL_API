import os
import requests
import yaml
import pandas as pd
import json
import time
from tqdm import tqdm

def get_summoner_by_summoner_name(summoner_name, api_key, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_entries_by_summoner_id(summoner_id, api_key, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_challenger_league(api_key, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_summoner_by_summoner_id(summoner_id, api_key, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_matches_by_puuid(puuid, api_key, region="europe", start=0, count=20):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_match_by_match_id(match_id, api_key, region="europe"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_matches_by_summoner_id(summoner_id, api_key, region="euw1", start=0, count=20):
    summoner = get_summoner_by_summoner_id(summoner_id, api_key)
    match_ids = get_matches_by_puuid(summoner['puuid'], api_key, start=start, count=count)
    matches = [get_match_by_match_id(match_id, api_key) for match_id in match_ids]
    return matches


def main(*args, **kwargs):
    try:
        # Get the full challenger league
        challenger_league = get_challenger_league(cfg['api_key'])

        # Get every summonerId in the list
        summoner_ids = [entry["summonerId"] for entry in challenger_league['entries']]
    except Exception as e:
        print(e)

    for summoner_id in tqdm(summoner_ids):
        print(f"Downloading {summoner_id} data.")
        time.sleep(10)

        # Get match data
        try:
            matches = get_matches_by_summoner_id(summoner_id, cfg['api_key'])
            for match in matches:
                print(f"Match: {match['metadata']['matchId']}")

                # TODO: Check if the match already exists in the JSON file.

                if match['info']['gameMode'] != 'CLASSIC' or match['info']['gameType'] != 'MATCHED_GAME':
                    print("ERROR!: This game is not ranked")
                    continue

                # Create match_info object
                match_info = {'match_id': match['metadata']['matchId']}
                match_info['game_duration'] = match['info']['gameDuration']
                match_info['game_version'] = match['info']['gameVersion']

                # Get teams info
                teams = match['info']['teams']

                for team_id, team in enumerate(teams):
                    match_info["_".join(["win", str(team_id)])] = team['win']

                    # Bans
                    for ban in team['bans']:
                        match_info["_".join(["ban", str(ban['pickTurn'])])] = ban['championId']
                    
                    # Objectives
                    for obj_key, obj_value in team['objectives'].items():
                        for obj_subkey, obj_subvalue in obj_value.items():
                            match_info["_".join(["objectives", str(team_id), str(obj_key), str(obj_subkey)])] = obj_subvalue

                    # Participants
                    participant_data = [
                        "kills",
                        "deaths",
                        "assists",
                        "champLevel",
                        "firstBloodKill",
                        "neutralMinionsKilled",
                        "totalMinionsKilled",
                        "visionScore",
                        "championId",
                        "goldEarned",
                        "teamPosition"
                    ]

                    for offset in range(5):
                        participant_id = team_id * 5 + offset
                        participant = match['info']['participants'][participant_id]
                        participant_info = {k: participant[k] for k in participant_data}
                        
                        for info_key, info_value in participant_info.items():
                            match_info["_".join(["participant", str(participant_id), info_key])] = info_value

                with open("matches.jsonl", "a") as f:
                    jout = json.dumps(match_info)
                    f.write(jout)
                    f.write("\n")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    with open("config.yml", "r") as f:
        try:
            cfg = yaml.safe_load(f)
        except yaml.YAMLError as e:
           print(e)

    main(cfg)

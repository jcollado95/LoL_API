import requests

def requestSummonerData(region, summonerName, APIKey):

    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/positions/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def main():
    region = 'euw1'
    summonerName = (str)(input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))
    APIKey = 'RGAPI-628633b8-72f0-4a01-b971-ee5074d99e18'

    responseJSON  = requestSummonerData(region, summonerName, APIKey)

    ID = responseJSON['id']
    ID = str(ID)

    responseJSON = requestRankedData(region, ID, APIKey)
    print (responseJSON[0]['tier'] + " " + responseJSON[0]['rank'])
    print (responseJSON[0]['leaguePoints'])

#This starts my program!
if __name__ == "__main__":
    main()

#This tutorial was built by me, Farzain! You can ask me questions or troll me on Twitter (@farzatv)

#First we need to import requests. Installing this is a bit tricky. I included a step by step process on how to get requests in readme.txt which is included in the file along with this program.
import requests

def requestSummonerData(region, summonerName, APIKey):

    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()
    
def main():
    region = 'euw1'
    summonerName = (str)(input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))
    APIKey = 'RGAPI-9a0556ce-cb6f-4cb5-a5fa-4159303c74ff'

    responseJSON  = requestSummonerData(region, summonerName, APIKey)
    
    ID = responseJSON['id']
    ID = str(ID)
    
    responseJSON = requestRankedData(region, ID, APIKey)
    print (responseJSON[0]['tier'] + " " + responseJSON[0]['rank'])
    print (responseJSON[0]['leaguePoints'])

#This starts my program!
if __name__ == "__main__":
    main()


import functools
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib.parse
 
# VARIABLES
server = "euw"
players = [{"name": "Main","account": "V9 Altbert"},{"name": "Second","account": "Alberner Albert"},{"name": "Smurf","account":"Albert Number 1"}]
printable_list = []

session = HTMLSession()
 
for name in players:
    summoner_name = name["account"]
    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://' + server + '.op.gg/summoner/userName=' + summoner_name_encoded
    html = session.get(page)
    soup = BeautifulSoup(html.content, 'html.parser')
 
    rank = soup.find("div", {"class": "tier"}).text.strip()
    lp = soup.find("div", {"class": "lp"}).text.strip()
    winrate = soup.find("div", {"class": "ratio"}).text.strip()
    winlose = soup.find("div", {"class": "win-lose"}).text.strip()
    wins, losses = winlose.split(" ")
    
    printable_list.append({"pos": 0, "player": name["name"] ,"name": name["account"], "rank":rank, "lp":lp, "winrate": winrate, "wins": wins, "losses":losses})
 
pos = 1
for entry in printable_list:
    entry["pos"] = pos
    pos += 1
 
print(tabulate(printable_list, headers={"pos": "Pos", "player": "Account", "name": "Name", "rank": "Rank", "lp": "LP", "winrate": "Winrate", "wins":"Wins", "losses":"Losses"}))

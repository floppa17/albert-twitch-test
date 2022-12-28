from flask import Flask, request
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET'])
def opgg():
    name = "Main"
    summoner_name = "V9 Altbert"
    session = HTMLSession()

    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
    html = session.get(page)
    soup = BeautifulSoup(html.content, 'html.parser')
 
    rank = soup.find("div", {"class": "tier"}).text.strip()
    lp = soup.find("div", {"class": "lp"}).text.strip()
    winrate = soup.find("div", {"class": "ratio"}).text.strip()
    wins, losses = soup.find("div", {"class": "win-lose"}).text.strip().split(" ")
    lastupdate = soup.find("div", {"class": "last-update"}).text.strip().partition("Last updated: ")[2]
    return(""+summoner_name+" ist stuck in "+rank+", "+lp+", "+wins+" "+losses+", "+winrate+" ("+lastupdate+")")

if __name__ == '__main__':
    app.run()

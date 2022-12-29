from flask import Flask, request
from bs4 import BeautifulSoup
import urllib.parse
from requests_html import HTMLSession



app = Flask(__name__)

@app.route('/')
def opgg():
  summoner_name = request.args.get('summoner_name')
  if summoner_name is None or summoner_name == '' or summoner_name == "''":
    string = ""
    string += lookup("V9 Altbert")
    string += lookup("Alberner Albert")
    string += lookup("Albert Number 1")
    return string
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

def lookup(acc):
  summoner_name = acc
  session = HTMLSession()
  summoner_name_encoded = urllib.parse.quote(summoner_name)
  page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
  html = session.get(page)
  soup = BeautifulSoup(html.content, 'html.parser')

  rank = soup.find("div", {"class": "tier"}).text.strip().replace(" ", "")
  lp = soup.find("div", {"class": "lp"}).text.strip()
  winrate = soup.find("div", {"class": "ratio"}).text.strip()
  return("[ "+summoner_name+" | "+rank+" "+lp+" | "+winrate+" ] ")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

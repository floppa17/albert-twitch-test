import functools
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib.parse
 
def main():
    result = opgg()
    return result


# VARIABLES

    


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

import uvloop
import aiohttp
import asyncio
from fastapi import FastAPI, Path
from bs4 import BeautifulSoup
import urllib.parse
import time
from fastapi.responses import PlainTextResponse



app = FastAPI()

uvloop.install()

cache = {}

async def get_page_cached(url):
    if url in cache:
        data, timestamp = cache[url]
        if time.time() - timestamp < 15 * 60:  # 15 minutes
            return data
    data = await get_page(url)
    cache[url] = (data, time.time())
    return data

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_page(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return html

def parse_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  rank = soup.find("div", {"class": "tier"}).text.strip().replace(" ", "")
  lp = soup.find("div", {"class": "lp"}).text.strip()
  winrate = soup.find("div", {"class": "ratio"}).text.strip()
  mmr = soup.find("div", {"class": "average-tier"}).text.strip()
  wins, losses = soup.find("div", {"class": "win-lose"}).text.strip().split(" ")
  games = int(wins.replace("W", ""))+int(losses.replace("L", ""))
  return {"rank": rank, "lp": lp, "winrate": winrate, "mmr": mmr, "games": games}

def parse_html_streak(html):
  soup = BeautifulSoup(html, 'html.parser')
  results = soup.find_all("div", {"class": "result"})
  streak = 0
  for result in results:
    print()
    if result.text.strip() == "Defeat":
      streak = streak + 1
    else:
      break
  return streak


async def lookupSummary(acc):
    summoner_name = acc
    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
    html = await get_page_cached(page)
    data = parse_html(html)
    wr = data['winrate'].split(" ")[2]
    lp = data['lp'].replace(" ", "")
    return f"{summoner_name}; {data['rank']} {lp}; mmr:{data['mmr']}; {wr}:{data['games']}"


@app.get("/summoner/{summoner_name}", response_class=PlainTextResponse)
async def opgg(summoner_name: str = Path(None, title="Summoner name of player"), fetch_match_history: bool = False):
  if summoner_name == "''":
    tasks = [asyncio.create_task(lookupSummary("V9 Altbert")),asyncio.create_task(lookupSummary("Alberner Albert")),asyncio.create_task(lookupSummary("Albert Number 1"))]
    results = await asyncio.gather(*tasks)
    return " ;; ".join(results)
  else:
    summoner_name = summoner_name.replace("'", "")
    print(summoner_name)
    if summoner_name == "#smurf":
      summoner_name = "Albert Number 1"
    elif summoner_name == "#main":
      summoner_name = "V9 Altbert"
    elif summoner_name == "#alt":
      summoner_name = "Alberner Albert"

    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
    html = await get_page(page)
    data = parse_html(html)

    if parse_html_streak(html) > 1:
      return f"{summoner_name} ist stuck in {data['rank']} {data['lp']} mit {data['games']} games, {data['winrate']}, {data['mmr']} mmr, {parse_html_streak(html)} games losing streak"
    else:
      return f"{summoner_name} ist stuck in {data['rank']} {data['lp']} mit {data['games']} games, {data['winrate']}, {data['mmr']} mmr"
    
  return("Error")

  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

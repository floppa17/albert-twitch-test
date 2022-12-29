import uvloop
import aiohttp
import asyncio
from fastapi import FastAPI
from bs4 import BeautifulSoup
import urllib.parse
import time


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
    return {"rank": rank, "lp": lp, "winrate": winrate}

async def lookup(acc):
    summoner_name = acc
    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
    html = await get_page_cached(page)
    data = parse_html(html)
    return f"[ {summoner_name} | {data['rank']} {data['lp']} | {data['winrate']} ] "

@app.get("/")
async def opgg(summoner_name: str = None):
    if summoner_name is None or summoner_name == '' or summoner_name == "''":
        tasks = [
            asyncio.create_task(lookup("V9 Altbert")),
            asyncio.create_task(lookup("Alberner Albert")),
            asyncio.create_task(lookup("Albert Number 1"))
        ]
        results = await asyncio.gather(*tasks)
        return "\n".join(results)

    summoner_name_encoded = urllib.parse.quote(summoner_name)
    page = 'https://euw.op.gg/summoner/userName=' + summoner_name_encoded
    html = await get_page(page)
    data = parse_html(html)
    return f"{summoner_name} is stuck in {data['rank']}, {data['lp']}, {data['winrate']}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

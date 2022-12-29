
# OP.GG fetcher

My first experience with Python web developement

## Usage
!opgg  
@$(user) $(urlfetch https://FastAPI-opgg-fetcher.leon16c.repl.co/summoner/'$(querystring)')


## Optimizations

I switched to FastAPI instead of Flask, but I don't think that it really made a difference.
Some major improvements were:
- Deployment using uvicorn instead of using Werkzeug which is only intended for development
- Using aiohttp and asyncio to make asynchronous requests for the lookup of three accounts
- Simple caching for 15 minutes using time()


## Acknowledgements

 - [Inspiration for this project](https://github.com/hamzab70/op.gg-scraper)
 - [ChatGPT for code suggestions](https://chat.openai.com/chat)
 - [README generator](https://readme.so/de/editor)



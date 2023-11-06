# shcherbin_trade_bot

A test demo project of a Django Telegram bot.

For simplicity initial balances are generated every time a new chat is registered in ETH, BTC, USDT with initial balances of 100, 10, 1000000000

The bot is containerized and is being run via docker-compose together with Redis cache and PostgreSQL database.
To build docker image run
```make build```
To run the but add three secrets to the .env file in ./trade_bot:
SWAP_ZONE_KEY
SECRET_KEY amd TELEGRAM_BOT_TOKEN and then run ```make upd```. That will start respective containers.  
Then it is required to run ```make connect_bot```. That will start a telegram bot polling.  

Since the bot is run locally setting up a webhook would be a problem
so it runs as a management command constantly polling the Telegram API. (The bot could be implemented as a Celery task but that would increase complexity of installation).
Now you can communicate with your bot in Telegram!

To stop the bot run ```make down```, don't forget there is a volume with a database,
you can remove it using ```docker volume rm``` .
from pyrogram import Client
from config import *
from aiohttp import web
from plugins import web_server

API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = BOT_TOKEN
ADMIN = ADMINS

print("Bot Started")


class Bot(Client):

    def __init__(self):
        super().__init__(
        "droplink search bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins"),
        workers=50,
        sleep_threshold=10
        )

    async def start(self):
        await super().start()

        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, 8000).start()

        print('Bot started')

    async def stop(self, *args):
        await super().stop()
        
# Running the bot.
Bot().run()


from translation import *
from pyrogram import Client, filters
from plugins.groups import group_send_handler
from plugins.database import collection
from pymongo import TEXT
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)

@Client.on_message(filters.command('start'))
async def start_message(c,m):
    collection.create_index([("title" , TEXT),("caption", TEXT)],name="movie_index")
    if len(m.command) == 1:
        return await m.reply_photo("https://telegra.ph/file/32fdcdd2e76a4df454e39.jpg",
            caption=START_MESSAGE.format(m.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                     InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'https://t.me/SpiderSearchBot?startgroup=true'),
                     ],[
                     InlineKeyboardButton("⚡ 𝙶𝚁𝙾𝚄𝙿 ⚡", url="https://t.me/MX_Movie_Request"),                             
                     InlineKeyboardButton("🤖 𝚄𝙿𝙳𝙰𝚃𝙴𝚂 🤖", url="https://t.me/MX_Networks")
                    ]
                ]
            )
        )
    else:
        return await group_send_handler(c,m)

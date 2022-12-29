import ast
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import collection
from config import *
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


# Add Movie to database
@Client.on_message(filters.chat(ADMINS) & filters.media)
async def web_db(c: Client, m: Message):
    if m.caption_entities:
        message = m.caption
        captions = m.caption_entities

        for count, i in enumerate(await caption(captions)):
            message = message.replace("👉 Link 🔗", i['url'], 1)

        id = collection.insert_one(
            {"caption": message,
                'title': message.splitlines()[0]}
        )

        reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Delete", callback_data=f"delete#{id.inserted_id }")],
        ])

        txt = await m.reply('Added Successfully', reply_markup=reply_markup)

    else:
        txt = await m.reply('Something went wrong')
        
        
async def caption(caption_entities):
	x = []
	string = str(caption_entities)
	res = ast.literal_eval(string)
	for i in res:
		if "url" in i:
			obj = {
				"type": i["type"],
				"offset": i["offset"],
				"length": i["length"],
				"url": i["url"]
			}
			x.append(obj)
	return x

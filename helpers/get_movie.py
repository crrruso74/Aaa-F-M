from pyrogram.types import Message
from plugins.database import collection
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from translation import *
from helpers.validate_query import validate_q

BUTTONS = {}
async def get_movies(query:str, m:Message):
    list2 = []
    results = await search_for_videos(query)
    if results is not None:
        for result in results:   
            id = str(result['_id'])
            list2.append(
                {
                'id': id,
                'caption': f'**{result["caption"]}**'
                }
            )

        if len(list2) > 1: 
            ls = split_list(list2, 1)
            btns = list(ls) 
            keyword = f"{m.chat.id}-{m.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = []
            buttons.append(
                   [InlineKeyboardButton("•∆ sᴛʀᴇᴀᴍ ✓ᴅᴏᴡɴʟᴏᴀᴅ ∆•", url="https://youtube.com/shorts/hQMU8-eTVLQ?feature=share")]
                )
            buttons.append(
                [InlineKeyboardButton(text="📃 ᴘᴀɢᴇs 1/1",callback_data="pages")]
            )

            if m.chat.id in ADMINS:
                buttons.append(
                [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{list2[0]['id']}")]
            )   
            
            reply_markup= InlineKeyboardMarkup(buttons)
            txt = await m.reply(text=list2[0]['caption'], reply_markup=reply_markup, disable_web_page_preview=True)
            return txt

        data = BUTTONS[keyword]

        buttons = []
        buttons.append(
                [InlineKeyboardButton("•∆ sᴛʀᴇᴀᴍ ✓ᴅᴏᴡɴʟᴏᴀᴅ ∆•", url="https://youtube.com/shorts/hQMU8-eTVLQ?feature=share")]
            )
        buttons.append(
            [InlineKeyboardButton(text="ɴᴇxᴛ ►",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 ᴘᴀɢᴇs 1/{data['total']}", callback_data="pages")]
        )

        if m.chat.id in ADMINS:
            buttons.append(
            [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{list2[0]['id']}")]
        )   

        reply_markup = InlineKeyboardMarkup(buttons) 
        txt = await m.reply(text=list2[0]['caption'], reply_markup=reply_markup, disable_web_page_preview=True, quote=True)
        return txt


async def search_for_videos(search_text:str):
    query = await validate_q(search_text)
    x = f"\"{query}\""
    pipeline= {
            '$text':{'$search': x }
        }
    db_list = collection.find(
            pipeline, 
            {'score': {'$meta':'textScore'}}
        )

    query = db_list.sort([("score", {'$meta': 'textScore'})]) 
    
    if query.count() > 0:
        return query

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          




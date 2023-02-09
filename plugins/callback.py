import re
from pyrogram import Client, filters
from .database import collection
from bson.objectid import ObjectId
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.get_movie import get_movies
from helpers.get_movie import BUTTONS
from helpers.auto_delete import auto_delete

@Client.on_callback_query(filters.regex(r"^send")) 
async def cb_send_handler(c,m):
    await m.answer()
    id = m.data.split('#')[1]
    result = collection.find_one({'_id': ObjectId(id)})

    try:
        caption = result['caption']
    except Exception as e:
        return await m.message.reply("Some error occurred")

    caption = await replace_username(caption)
    if m.message.chat.id in ADMINS:  
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Delete", callback_data=f"delete#{id}")],
            ])
    else:
        reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Join", url=f"https://t.me/{USERNAME}")],
        ])   

    txt = await m.message.reply(
        f"**{caption}**", 
        disable_web_page_preview=True, 
        reply_markup=reply_markup)


@Client.on_callback_query(filters.regex(r"^delete"))
async def cb_delete_handler(c,m):
    await m.answer()
    try:

        id = m.data.split('#')[1]
        my_query = {'_id': ObjectId(id)}
        collection.delete_one(my_query)
        txt = await m.message.edit(f"Deleted Successfully", disable_web_page_preview=True)
    except Exception as e:
        print(e)
        txt = await m.message.edit(f"Some error occurred while deleting", disable_web_page_preview=True)

    await auto_delete(m.message, txt)

async def replace_username(text):
    usernames = re.findall("([@#][A-Za-z0-9_]+)", text)

    for i in usernames:
        text = text.replace(i, f"@{USERNAME}")

    telegram_links = re.findall(r'[(?:http|https)?://]*(?:t.me|telegram.me)[^\s]+', text)

    for i in telegram_links:
        text = text.replace(i, f"@{USERNAME}")

    return text


@Client.on_callback_query(filters.regex(r"^close"))
async def cb_close_handler(c,m):
    await m.answer()
    await m.message.delete()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def send_spell_checker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Search for yourself", show_alert=True)

    
    results = await get_movies(movie_, query.message)
    if results is None:
      return await  query.answer("Movie not found in Database )", show_alert=True)
    
    await auto_delete(query.message, results)

# Next Button

@Client.on_callback_query(filters.regex(r"^next"))
async def next_btn_cb_handler(client: Client, query: CallbackQuery):
    txt = None
    ident, index, keyword = query.data.split("_")
    search = BUTTONS.get(keyword)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.",show_alert=True)
        return
    if query.data.startswith("next"):
        await query.answer()
        ident, index, keyword = query.data.split("_")
        data = BUTTONS[keyword]

        if int(index) == int(data["total"]) - 2:
            buttons = []
            id = data['buttons'][int(index)+1][0]['id']
            cap = data['buttons'][int(index)+1][0]['caption']
            buttons.append(
                [InlineKeyboardButton("💥 ʜᴏᴡ ᴛᴏ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ 💥", url="https://t.me/mdiskshortnerlink_tutorial")]
            )
            buttons.append(
                [InlineKeyboardButton("◄ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)+1}_{keyword}")]
            )
            buttons.append(
                [InlineKeyboardButton(f"📃 𝐏𝐀𝐆𝐄𝐒 {int(index)+2}/{data['total']}", callback_data="pages")]
            )

            if query.message.chat.id in ADMINS:
                buttons.append(
                [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{id}")]
            )   
        
            try:
                txt = await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            except Exception as e:
                print(e)
        else:
            buttons = []
            cap = data['buttons'][int(index)+1][0]['caption']
            id = data['buttons'][int(index)+1][0]['id']
            buttons.append(
                [InlineKeyboardButton("💥 ʜᴏᴡ ᴛᴏ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ 💥", url="https://t.me/Mdiskshortnerlink_Tutorial")]
            )
            buttons.append(
                [InlineKeyboardButton("◄ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
            )
            buttons.append(
                [InlineKeyboardButton(f"📃 𝐏𝐀𝐆𝐄𝐒 {int(index)+2}/{data['total']}", callback_data="pages")]
            )

            if query.message.chat.id in ADMINS:
                buttons.append(
                [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{id}")]
            )   
        
            try:
                txt = await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            except Exception as e:
                print(e)

        await auto_delete(query.message, txt)
    return

        

# Back Button
@Client.on_callback_query(filters.regex(r"^back"))
async def back_btn_cb_handler(client: Client, query: CallbackQuery):

    txt = None
    ident, index, keyword = query.data.split("_")
    search = BUTTONS.get(keyword)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.",show_alert=True)
        return

   
    if query.data.startswith("back"):
        await query.answer()
        ident, index, keyword = query.data.split("_")
        data = BUTTONS[keyword]
        print(int(index))
        if int(index) == 1: 

            buttons = []
            
            cap = data['buttons'][int(index)-1][0]['caption']
            id = data['buttons'][int(index)-1][0]['id']
            buttons.append(
                [InlineKeyboardButton("💥 ʜᴏᴡ ᴛᴏ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ 💥", url="https://t.me/Mdiskshortnerlink_Tutorial")]
            )
            buttons.append(
                    [InlineKeyboardButton("𝐍𝐄𝐗𝐓 ►", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
            buttons.append(
                [InlineKeyboardButton(f"📃 𝐏𝐀𝐆𝐄𝐒 {int(index)}/{data['total']}", callback_data="pages")]
            )

            if query.message.chat.id in ADMINS:
                buttons.append(
                [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{id}")]
            )   

            try:
                txt = await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            except Exception as e:
                print(e)
        

        else:

            buttons = []

            cap = data['buttons'][int(index)-1][0]['caption']
            id = data['buttons'][int(index)-1][0]['id']
            buttons.append(
                [InlineKeyboardButton("💥 ʜᴏᴡ ᴛᴏ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ 💥", url="https://t.me/Mdiskshortnerlink_Tutorial")]
            )
            buttons.append(
                [InlineKeyboardButton("◄ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝐍𝐄𝐗𝐓 ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
            )
            buttons.append(
                [InlineKeyboardButton(f"📃 𝐏𝐀𝐆𝐄𝐒 {int(index)}/{data['total']}", callback_data="pages")]
            )
                            
            if query.message.chat.id in ADMINS:
                buttons.append(
                [InlineKeyboardButton("🗑 Delete", callback_data=f"delete#{id}")]
            )   

            try:
                txt = await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            except Exception as e:
                print(e)

        await auto_delete(query.message, txt)
    return   


from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from translation import *
import urllib.parse
from helpers.get_movie import get_movies
from helpers.send_movies import send_movie_pvt_handler
from helpers.validate_query import validate_q
from helpers.auto_delete import auto_delete

@Client.on_message(filters.private & filters.text & filters.incoming & ~filters.command(['start', 'total']))
async def find_movies(c: Client, m:Message):
    query = m.text
    query = await validate_q(query)
    if query:
        if m.text:
            reply_markup = await get_movies(query=query, m=m)
            if reply_markup is None or reply_markup is False: 
                await send_movie_pvt_handler(m=m, query=query, reply_markup=reply_markup)
    await auto_delete(m, reply_markup) 

    
def escape_url(str):
    escape_url = urllib.parse.quote(str)
    return escape_url

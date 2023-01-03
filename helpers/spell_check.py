import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
import requests
from imdb import IMDb
imdb = IMDb() 
from config import *
import requests

async def advantage_spell_chok(msg, q):
    txt = await msg.reply('```Searching...🍳```')
    try:
        # query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", q, flags=re.IGNORECASE) # pls contribute some common words 
        query = q + " movie"
        g_s = await search_gagala(query)
        g_s += await search_gagala(msg.text)
        gs_parsed = []
        if not g_s:
            await txt.delete()
            return False, False
        regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
        gs = list(filter(regex.match, g_s))
        gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in gs]
        if not gs_parsed:
            reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*", re.IGNORECASE) # match something like Watch Niram | Amazon Prime 
            for mv in g_s:
                match  = reg.match(mv)
                if match:
                    gs_parsed.append(match.group(1))
        user = msg.from_user.id if msg.from_user else 0
        movielist = []
        gs_parsed = list(dict.fromkeys(gs_parsed)) # removing duplicates https://stackoverflow.com/a/7961425
        if len(gs_parsed) > 3:
            gs_parsed = gs_parsed[:3]
        if gs_parsed:
            for mov in gs_parsed:
                imdb_s = await get_poster(mov.strip(), bulk=True) # searching each keyword in imdb
                if imdb_s:
                    movielist += [movie.get('title') for movie in imdb_s]
        movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
        movielist = list(dict.fromkeys(movielist)) # removing duplicates
        if not movielist:
            await txt.delete()
            return False, False
        btn = [[
                    InlineKeyboardButton(
                        text=movie.strip()[:25] + '..' if len(movie.strip()) > 75 else movie.strip(),
                        callback_data=f"spolling#{user}#{movie.strip()[:25] + '..' if len(movie.strip()) > 25 else movie.strip()}",
                    )
                ] for k, movie in enumerate(movielist)]
        btn.append([InlineKeyboardButton(text="Close", callback_data='close')])
        await txt.delete()
        return True, InlineKeyboardMarkup(btn)

    except Exception as e:
        print(e)
        await txt.delete()
        return False, False


async def search_gagala(text):
    usr_agent = {
        'User-Agent': 'your bot 0.1'
        }
    text = text.replace(" ", '+')
    url = f'https://www.google.com/search?q={text}'
    response = requests.get(url, headers=usr_agent)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all( 'h3' )
    return [title.getText() for title in titles]

async def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        # https://t.me/GetTGLink/4183
        query = (query.strip()).lower()
        title = query
        year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
        if year:
            year = await list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
            if year:
                year = await list_to_str(year[:1]) 
        else:
            year = None
        if bulk:
            results = 10
        else:
            results = 1
        movieid = imdb.search_movie(title.lower(), results=results)

        if not movieid:
            return None

        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = int(query)
    movie = imdb.get_movie(movieid)

    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"

    if movie.get('full-size cover url'):
        poster = movie.get('full-size cover url')
    else:
        poster = 'https://i.ibb.co/Tvb5wB3/kisspng-photographic-film-movie-camera-cinema-website-and-mobile-application-development-service-5d3.jpg'

    return {
        'title': movie.get('title'),
        "aka": await list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "runtime": await list_to_str(movie.get("runtimes")),
        "certificates": await list_to_str(movie.get("certificates")),
        "languages": await list_to_str(movie.get("languages")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': await list_to_str(movie.get("genres")),
        'poster': poster,
        'rating': str(movie.get("rating")),
        'url':f'https://www.imdb.com/title/tt{movieid}'
    }

async def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    elif MAX_LIST_ELM:
        k = k[:int(MAX_LIST_ELM)]
        return ' '.join(f'{elem}, ' for elem in k)
    else:
        return ' '.join(f'{elem}, ' for elem in k)



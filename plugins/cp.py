import urllib
import urllib.parse
import requests
import base64
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import time
from pyrogram import Client as bot
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import sys
import re
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
import aiohttp
import requests
import json
from pyrogram.types import Message
from pyrogram import Client, filters

import json
import cloudscraper
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["khan"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text    
    await input1.delete(True)
    
    url = "https://admin2.khanglobalstudies.com/api/login-with-password?medium=0"
    payload = {
        "phone": raw_text.split("*")[0],
        "password": raw_text.split("*")[1],
        "remember": True
    }
    headers = {
        'Host': 'admin2.khanglobalstudies.com',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://www.khanglobalstudies.com',
        'Referer': 'https://www.khanglobalstudies.com/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    s = cloudscraper.create_scraper()
    response = s.post(url=url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        authorization = data["token"]
        await editable.edit(f"**Login Successful**")
    else:
        await m.reply_text("Go back to response")
        return

    headers1 = {
        'Host': 'admin2.khanglobalstudies.com',
        'access-control-allow-origin': '*',
        'accept': 'application/json',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'authorization': 'Bearer ' + authorization,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.khanglobalstudies.com',
        'referer': 'https://www.khanglobalstudies.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }

    html1 = s.get('https://admin2.khanglobalstudies.com/api/user/v2/courses', headers=headers1).text
    output = json.loads(html1)
    bdata = output.get("data", [])
    
    if not bdata:
        await m.reply_text("No data available")
        return

    cool = ""
    for data in bdata:
        FFF = "**BATCH-ID  -  BATCH NAME**"
        aa = f" ```{data['id']}```- **{data['title']}**\n\n"
        if len(f'{cool}{aa}') > 4096:      
            await m.reply_text(aa)
            cool = ""
        cool += aa

    if cool:
        await m.reply_text(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    else:
        await m.reply_text("No data available")

    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    input2 = await bot.listen(editable1.chat.id)
    raw_text2 = input2.text
    html2 = s.get(f'https://admin2.khanglobalstudies.com/api/user/courses/{raw_text2}/lessons', headers=headers1).text
    output = json.loads(html2)
    lesson = output.get('data', {}).get('lessons', [])
    
    vj = ""
    for data in lesson:
        tids = data['id']
        idid = f"{tids}&"
        if len(f"{vj}{idid}") > 4096:
            vj = ""
        vj += tids
        await editable1.edit(f"**Send the Subject id :-**\n```{vj}```")
        input4 = await bot.listen(editable1.chat.id)
        raw_text4 = input4.text
        response02 = s.get(f'https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{raw_text4}/topics?page=1', headers=headers).json().get('data', [])
        cool2 = ""
        vj = ""
        for dat in response02:
            FF = "**SUBJECT-ID - SUBJECT NAME - TOTAL VIDEOS - PDFS**"
            aa = f" ```{dat['_id']}```- **{dat['name']} - {dat['videos']} - {dat['notes']}**\n\n"
            idid = f"{dat['_id']}&"
            if len(f"{vj}{idid}") > 4096:
                vj = ""
            vj += idid     
            cool2 += aa
        await editable1.edit(f'{"**You have these Subjects in this Batch:-**"}\n\n{FF}\n\n{cool2}')
        editable2 = await m.reply_text(f"**Enter this to download full batch :-**\n```{vj}```")
        input5 = await bot.listen(editable2.chat.id)
        raw_text5 = input5.text
        xv = raw_text5.split('&')
        for y in range(0, len(xv)):
            t = xv[y].strip()
            html3 = s.get("https://api.penpencil.xyz/v2/batches/"+raw_text3+"/subject/"+raw_text4+"/contents?page=1&tag="+t+"&contentType=videos",headers=headers).text
            ff = json.loads(html3)
            tpage = (ff["paginate"])["totalCount"]//ff["paginate"]["limit"]+2
            print("Total page:", tpage)
            for i in range(1, tpage)[::-1]:
                html4 = s.get("https://api.penpencil.xyz/v2/batches/"+raw_text3+"/subject/"+raw_text4+"/contents?page="+str(i)+"&tag="+t+"&contentType=videos",headers=headers).json().get('data', [])
                html4.reverse()
                for dat in html4:
                    try:
                        class_title = (dat["topic"])
                        class_url = dat["url"].replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
                        cc = f"{dat['topic']}:{dat['url']}"
                        with open(f"{mm}-{batch}.txt", 'a') as f:
                            f.write(f"{class_title}:{class_url}\n")
                    except KeyError:
                        pass
        await m.reply_document(f"{mm}-{batch}.txt")

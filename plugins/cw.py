import urllib
import urllib.parse
import requests
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
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import sys
import re
from pyrogram import Client as bot
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from pyrogram import Client as bot
import time
from typing import List, Dict

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1VmXspFMod94-pT7xDCvmBEYt8U7f0mRB6XnG5huPE7I9qjhDW0qpx3LRyTD9WX7W6JvUGtgKN-qf1pJoZO-QXBMIykDivtAOgkJOmN-kyv4m_F0thrJ45z95hqWON0nsKBwvd"
bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

@bot.on_message(filters.command("master"))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    await input1.delete(True)

    headersa = {
    'Host': 'elearn.crwilladmin.com',
    'accept': 'application/json',
    'usertype': '2',
    'origintype': 'web',
    'user-agent': 'Mozilla/5.0 (Lund ; choot) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    #'token': token,
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://web.careerwill.com',
    'x-requested-with': 'mark.via.gp',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://web.careerwill.com/',
    # 'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9',
    }

    try:
        if "*" in raw_text:
           em = raw_text.split("*")[0]
           ps = raw_text.split("*")[1]
           data = {
           'email': em,
           'password': ps,
           }

           r = requests.post('https://elearn.crwilladmin.com/api/v3/login-other', headers=headersa, data=data).json()
           #print(r)
           token = r['data']['token']
           print('Token :- '+token)
           await editable.edit(f"**Login Successful**")
            await m.reply_text(f**Token :** `{token}`)          
        else:
           token = raw_text
           print('Token :- '+token)
           await editable.edit("**Login Successful**")
    except Exception as e:
      await m.reply_text(e)
    headers = {
    'Host': 'elearn.crwilladmin.com',
    'accept': 'application/json',
    'usertype': '2',
    'origintype': 'web',
    'user-agent': 'Mozilla/5.0 (Lund ; choot) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'token': token,
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://web.careerwill.com',
    'x-requested-with': 'mark.via.gp',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://web.careerwill.com/',
    # 'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9',
    } 
    
    url1 = requests.get('https://elearn.crwilladmin.com/api/v3/my-batch', headers=headers)
    keydata = json.loads(url1.text)
    bdata = keydata["data"]["batchData"]

    if not bdata:  # Check if there are no batches available
        await editable.edit("You don't have any batches available.")
        return

    cool = ""
    FFF = "**BATCH-ID  -  BATCH NAME**"
    for data in bdata:
        aa = f"`{data['id']}` - **{data['batchName']}**\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa

    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1= await m.reply_text("**Now send the Batch ID to Download**")

    input2 = await bot.listen(editable1.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    editable2 = await m.reply_text("📥Please wait patiently. 🧲Scraping Url...")

    url2 = requests.get(f"https://elearn.crwilladmin.com/api/v3/batch-topic/{raw_text2}?type=class", headers=headers)
    keydata2 = json.loads(url2.text)
    b_data = keydata2["data"]["batch_topic"]
    filename = keydata2["data"]["batch_detail"]["name"]

    all_urls = ""
    for data in b_data:
        t_name = (data["topicName"].replace(" ", ""))
        tid = (data["id"])
        url3 = requests.get(f"https://elearn.crwilladmin.com/api/v3/batch-detail/{raw_text2}?redirectBy=mybatch&b_data={tid}", headers=headers)
        keydata3 = json.loads(url3.text)
        vvx = keydata3["data"]["class_list"]["classes"]
        vvx.reverse()
        try:
            for data in vvx:
                vidid = data["id"]
                lessonName = data["lessonName"].replace("/", "_")
                bcvid = data["lessonUrl"][0]["link"]
                if bcvid.startswith("62"):
                    try:
                        html1 = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                        video = json.loads(html1)
                        video_source = video["sources"][5]
                        video_url = video_source["src"]
                        html2 = requests.get(f"https://elearn.crwilladmin.com/api/v3/livestreamToken?type=brightcove&vid={vidid}", headers=headers)
                        surl = json.loads(html2.text)
                        stoken = surl["data"]["token"]
                        link = video_url + "&bcov_auth=" + stoken
                        #await editable2.edit(f"🧲**Scraping video Url**: `{lessonName}`")
                    except Exception as e:
                        print(str(e))
                elif bcvid.startswith("63"):
                    try:
                        html3 = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                        video1 = json.loads(html3.text)
                        video_source1 = video1["sources"][5]
                        video_url1 = video_source1["src"]
                        html4 = requests.get(f"https://elearn.crwilladmin.com/api/v3/livestreamToken?type=brightcove&vid={vidid}", headers=headers)
                        surl1 = json.loads(html4.text)
                        stoken1 = surl1["data"]["token"]
                        link = video_url1 + "&bcov_auth=" + stoken1
                        #await editable2.edit(f"🧲**Scraping video Url**: `{lessonName}`")
                    except Exception as e:
                        print(str(e))
                else:
                    link = "https://www.youtube.com/embed/" + bcvid
                cc = f"{lessonName}::{link}"
                all_urls += f"{cc}\n"
        except Exception as e:
            await editable1.reply_text(str(e))

        try:
            html5 = requests.get(f"https://elearn.crwilladmin.com/api/v3/batch-notes/{raw_text2}?b_data={raw_text2}", headers=headers)
            pdfD = json.loads(html5.text)
            k = pdfD["data"]["notesDetails"]
            bb = len(pdfD["data"]["notesDetails"])
            ss = f"Total PDFs Found in Batch id **{raw_text2}** is - **{bb}** "
            await editable1.reply_text(ss)
            k.reverse()
            count1 = 1
            try:
                for data in k:
                    name = data["docTitle"]
                    s = data["docUrl"]
                    xi = data["publishedAt"]
                    all_urls += f"{name}::{s}\n"
                    #await editable2.edit(f"🧲**Scraping notes Url**: `{name}`")
            except Exception as e:
                await m.reply_text(str(e))
        except Exception as e:
            print(str(e))
    await editable2.edit("Scraping completed successfully!")
    await editable2.delete()
    # Write all URLs into one document file
    with open(f"{filename}.txt", 'w') as f:
        f.write(all_urls)

    await m.reply_document(
        document=f"{filename}.txt",
        caption=f"📍**APP Name**: Career Will\n🔰**Batch Name**: `{filename}`"
    )

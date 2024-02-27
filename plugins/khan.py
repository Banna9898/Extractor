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
import time
from typing import List, Dict

@bot.on_message(filters.command(["khan"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text    
    await input1.delete(True)    
    # Login process
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
    s = requests.Session()
    response = s.post(url=url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        authorization = data["token"]
        await editable.edit(f"**Login Successful:**")
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
    url1 = s.get('https://admin2.khanglobalstudies.com/api/user/v2/courses', headers=headers1)
    bdata = json.loads(url1.text)

    if not bdata:  # Check if there are no batches available
        await editable.edit("You don't have any batches available.")
        return
    cool = ""
    for data in bdata:
        FFF = "**BATCH-ID  -  BATCH NAME**"
        aa = f"`{data['id']}` - **{data['title']}** ❇️**{data['price']}₹**\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa  

    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text    
    await input2.delete(True)  
    await editable.delete()
    await editable1.delete()
    slugdata = next((x['slug'] for x in bdata if str(x['id']) == raw_text2), None)
    if slugdata:
        bname = next((item["title"] for item in bdata if item.get("slug") == slugdata), None)
        url2 = s.get(f'https://admin2.khanglobalstudies.com/api/user/courses/{slugdata}/lessons?medium=0', headers=headers1)
        cdata = json.loads(url2.text)
        cdata['lessons'].reverse()  # Reverse the data if needed
        with open(f"{bname}.json", "w") as json_file:
            json.dump(cdata, json_file)
        editable2 = await m.reply_text("📥**Please wait keep patientce.** 🧲    `Scraping Url...`")
        # Initialize a counter for the progress messages
        counter = 1  

        # Initialize the caption with headers
        caption = (
            f"✅ **JSON FILE** ✅\n"
            f"📍 **APP Name**: KHAN Global Studies\n"
            f"🔰 **Batch Name**: `{bname}`\n"
            "|\n"  # Vertical line separator
            "Field | Value\n"
            "--- | ---\n"
        )

        # Scraping videos
        for lesson in cdata['lessons']:
            lesson_name = lesson['name']
            for video in lesson['videos']:
                video_name = video['name']
                video_url = video['video_url']
                caption += f"{lesson_name} | {video_name}: {video_url}\n"
                # Update progress message for videos with a unique identifier
                await editable2.edit(f"🧲**Scraping videos Url**: `{lesson_name}` ({counter})")
                counter += 1  # Increment the counter for the next message

        # Scraping notes
        for note in cdata['notes']:
            note_name = note['name']
            note_url = note['video_url']
            caption += f"Notes | {note_name}: {note_url}\n"
            # Update progress message for notes
            #await editable2.edit(f"🧲**Scraping notes Url**: `{note_name}`")

        # Final progress message
        await editable2.edit("Scraping completed successfully!")
        await editable2.delete()

        # Sending the JSON document with vertically aligned content
        try:
            await m.reply_document(
                document=f"{bname}.json",
                caption=caption
            )
        except Exception as e:
            print("Error sending JSON document:", e)


        # Sending the text document
        try:
            await m.reply_document(
                document=f"{bname}.txt",
                caption=f"✅** TEXT FILE **✅ \n📍**APP Name**: KHAN Global Studies\n🔰**Batch Name**: `{bname}`"
            )
        except Exception as e:
            print("Error sending text document:", e)
    else:
        await m.reply_text("Invalid Batch ID.")

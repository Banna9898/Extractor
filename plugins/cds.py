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
from subprocess import getstatusoutput
import logging
import os
import sys
import re
from pyrogram import Client as bot
import time
from typing import List, Dict
from typing import Any, Dict

@bot.on_message(filters.command("cds"))
async def account_login(bot: Client, message: Message):
    editable = await message.reply_text("Please send your **USER ID** inside your Profile")
    input_message: Message = await bot.listen(editable.chat.id)
    raw_text = input_message.text
    await input_message.delete(True)
    token = raw_text
    headers = {
        'Host': 'api.cdsjourney.com',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'accept': 'application/json, text/plain, */*',
        'userid': token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.cdsjourney.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cdsjourney.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    
    try:
        url = requests.get("https://api.cdsjourney.com/subscribed?is_valid=1", headers=headers)
        url.raise_for_status()  # Raise an exception for non-200 status codes
        bdata = url.json()
    except requests.RequestException as e:
        await message.reply_text(f"Error accessing the API: {e}")
        return
    
    if bdata.get("items"):
        first_batch = bdata["items"][0].get("batch", {})
        batch_id = first_batch.get("batch_id")
        batch_name = first_batch.get("name")
        batch_fee = first_batch.get("fee")
        
        cool = f"`{batch_id}` - **{batch_name}** ❇️**{batch_fee}₹**\n\n"
        await editable.edit(f'{"**You have these batches :-**"}\n\n**BATCH-ID  -  BATCH NAME**\n\n{cool}')
        
        editable1 = await message.reply_text("**Now send the Batch ID to Download**")
        input2 = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        await editable.delete()
        await editable1.delete()
        
        batch_id_input = raw_text2
        if batch_id_input:
            try:
                url2 = requests.get(f'https://api.cdsjourney.com/batches/{batch_id_input}/topics', headers=headers)
                url2.raise_for_status()
                cdata = url2.json()
                
                with open(f"{batch_name}.json", "w") as json_file:
                    json.dump(cdata, json_file)
                
                editable2 = await message.reply_text("📥**Please wait patiently.** 🧲    `Scraping Url...`")
                counter = 1
                
                with open(f"{batch_name}.txt", "w") as f:
                    for video in cdata.get('topics', []):
                        if isinstance(video, dict):
                            video_name = video.get('name', 'Unnamed Video')
                            video_url = video.get('class_video_recording_play', {}).get('url')
                            if video_url:
                                f.write(f"{video_name}: {video_url}\n")
                                await editable2.edit(f"🧲**Scraping videos Url**: `{video_name}` ({counter})")
                                counter += 1
                        else:
                            print("Unexpected data type for video:", type(video))
                            counter += 1
                await editable2.edit("Scraping completed successfully!")
                await editable2.delete()
                
                # Sending the JSON document
                await message.reply_document(
                    document=f"{batch_name}.json",
                    caption=f"✅** JSON FILE **✅\n📍**APP Name**: Cds Journey\n🔰**Batch Name**: `{batch_name}`"
                )

                # Sending the text document
                await message.reply_document(
                    document=f"{batch_name}.txt",
                    caption=f"✅** TEXT FILE **✅\n📍**APP Name**: CDS Journey\n🔰**Batch Name**: `{batch_name}`"
                )

            except requests.RequestException as e:
                await message.reply_text(f"Error accessing batch topics: {e}")
        else:
            await message.reply_text("Invalid Batch ID.")
    else:
        await message.reply_text("No subscribed batches found.")



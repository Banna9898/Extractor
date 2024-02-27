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

# Your import statements here

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
    url = requests.get("https://api.cdsjourney.com/subscribed?is_valid=1", headers=headers)
    if url.status_code == 200:
        # User ID is valid
        await message.reply_text("Login successful!")
    else:
        # User ID is invalid
        await message.reply_text("Invalid user ID. Please try again.")
    bdata = json.loads(url.text)
    first_item = bdata["items"][0]  # Access the first item in the list
    batch_data = bdata["items"][0]["batch"]
    # Extract batch details
    batch_id = batch_data.get("batch_id")
    batch_name = batch_data.get("name")
    batch_fee = batch_data.get("fee")
    print("keydata:", batch_data)
    cool = ""
    FFF = "**BATCH-ID  -  BATCH NAME**"
    aa = f"`{batch_id}` - **{batch_name}** ❇️**{batch_fee}₹**\n\n"
    if len(f'{cool}{aa}') > 4096:
        cool = ""
    cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1 = await message.reply_text("**Now send the Batch ID to Download**")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    await editable.delete()
    await editable1.delete()
    batchid = raw_text2
    if batchid:
        url2 = requests.get(f'https://api.cdsjourney.com/batches/{batchid}/topics', headers=headers)
        if url2.status_code == 200:
            cdata = url2.json()  # Parse JSON response
            # Dumping JSON data to a file
            with open(f"{batch_name}.json", "w") as json_file:
                json.dump(cdata, json_file)
    
            editable2 = await message.reply_text("📥**Please wait patiently.** 🧲    `Scraping Url...`")
            counter = 1  # Initialize a counter
    
            with open(f"{batch_name}.txt", "w") as f:
                topics = cdata.get('topics', [])
                for topic in topics:  # Iterate through each topic in the 'topics' list
                    sub_topics = topic.get('sub_topics', [])
                    for sub_topic in sub_topics:  # Iterate through each sub-topic in the 'sub_topics' list
                        if isinstance(sub_topic, dict):  # Check if sub_topic is a dictionary
                            video_name = sub_topic.get('name', 'Unnamed Video')
                            video_url = sub_topic.get('class_video_recording_play', {}).get('url')
                            if video_url:
                                f.write(f"{video_name}: {video_url}\n")
                                await editable2.edit(f"🧲**Scraping videos Url**: `{video_name}` ({counter})")
                                counter += 1
                        else:
                            print("Unexpected data type for sub_topic:", type(sub_topic))
                            counter += 1
            await editable2.edit("Scraping completed successfully!")
            await editable2.delete()
        else:
            await message.reply_text("Failed to fetch batch topics. Please try again.")
    else:
        await message.reply_text("Invalid Batch ID.")

        # Sending the JSON document
        try:
            await message.reply_document(
                document=f"{batch_name}.json",
                caption=f"✅** JSON FILE **✅\n📍**APP Name**: Cds Journey\n🔰**Batch Name**: `{batch_name}`"
            )
        except Exception as e:
            print("Error sending JSON document:", e)

        # Sending the text document
        try:
            await message.reply_document(
                document=f"{batch_name}.txt",
                caption=f"✅** TEXT FILE **✅\n📍**APP Name**: CDS Journey\n🔰**Batch Name**: `{batch_name}`"
            )
        except Exception as e:
            print("Error sending text document:", e)






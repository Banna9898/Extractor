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
    keydata = first_item.get("batch", {})  # Use .get() to handle missing key gracefully
    print("keydata:", keydata)
    # Ensure keydata is a dictionary before proceeding
    if not isinstance(keydata, dict):
        await editable.edit("Batch data is not available.")
        return

    cool = ""
    FFF = "**BATCH-ID  -  BATCH NAME**"
    for data_key, data_value in keydata.items():  # Iterate over the key-value pairs of keydata
        if isinstance(data_value, dict):  # Check if data_value is a dictionary
            batch_id = data_value.get("batch_id")
            batch_name = data_value.get("name")
            batch_fee = data_value.get("fee")
            if batch_id and batch_name and batch_fee:  # Ensure all required fields are present
                aa = f"`{batch_id}` - **{batch_name}** ❇️**{batch_fee}₹**\n\n"
                if len(f'{cool}{aa}') > 4096:
                    cool = ""
                cool += aa
            else:
                print("Missing required fields in batch data.")
        else:
            print(f"Unexpected data type for key '{data_key}': {type(data_value)}")

    # Access batch details
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
        cdata = json.loads(url2.text)
        # Dumping JSON data to a file
        batch_name = first_item.get("name", "Unknown Batch")
        with open(f"{batch_name}.json", "w") as json_file:
            json.dump(cdata, json_file)
        editable2 = await message.reply_text("📥**Please wait keep patientce.** 🧲    `Scraping Url...`")
        counter = 1  # Initialize a counter

        with open(f"{batch_name}.txt", "w") as f:
            # Scraping videos
            for video in cdata:
                video_name = video.get('name', 'Unnamed Video')
                video_url = video.get('class_video_recording_play', {}).get('url')
                if video_url:
                    f.write(f"{video_name}: {video_url}\n")
                    # Update progress message for videos with a unique identifier
                    await editable2.edit(f"🧲**Scraping videos Url**: `{video_name}` ({counter})")
                    counter += 1  # Increment the counter for the next message
        await editable2.edit("Scraping completed successfully!")
        await editable2.delete()

        # Sending the JSON document
        try:
            await message.reply_document(
                document=f"{batch_name}.json",
                caption=f"✅** JSON FILE **✅\n📍**APP Name**: KHAN Global Studies\n🔰**Batch Name**: `{batch_name}`"
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
    else:
        await message.reply_text("Invalid Batch ID.")

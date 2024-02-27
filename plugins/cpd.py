# Importing necessary libraries and modules
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from subprocess import getstatusoutput
#from aiohttp import ClientSession
import helper
#from logger import logging
import time
#import asyncio
from pyrogram.types import User, Message
import sys
import re
import os
import tgcrypto
import pyrogram
import logging
from pyrogram import Client as bot
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
import urllib
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from subprocess import getstatusoutput
#from aiohttp import ClientSession
import helper
#from logger import logging
import time
#import asyncio
from pyrogram.types import User, Message
import sys
import re
import os
import tgcrypto
import pyrogram
import base64
import logging
from pyrogram import Client as bot
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
import urllib
import urllib.parse 

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1VmXspFMod94-pT7xDCvmBEYt8U7f0mRB6XnG5huPE7I9qjhDW0qpx3LRyTD9WX7W6JvUGtgKN-qf1pJoZO-QXBMIykDivtAOgkJOmN-kyv4m_F0thrJ45z95hqWON0nsKBwvd"

# URL for Brightcove videos
bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

# Initializing Pyrogram client for the bot
#bot = Client("my_account")

# Command handler for the bot
@bot.on_message(filters.command(["cw3"]))
async def account_login(bot: Client, m: Message):
    try:
        # URL for login API
        url = "https://elearn.crwilladmin.com/api/v5/login-other"

        # Data for login request
        data = {
            "deviceType": "android",
            "password": "",
            "deviceIMEI": "08750aa91d7387ab",
            "deviceModel": "Realme RMX2001",
            "deviceVersion": "R(Android 11.0)",
            "email": "",
            "deviceToken": "fYdfgaUaQZmYP7vV4r2rjr:APA91bFPn3Z4m_YS8kYQSthrueUh-lyfxLghL9ka-MT0m_4TRtlUu7cy90L8H6VbtWorg95Car6aU9zjA-59bZypta9GNNuAdUxTnIiGFxMCr2G3P4Gf054Kdgwje44XWzS9ZGa4iPZh"
        }

        # Headers for login request
        headers = {
            'Host': 'elearn.crwilladmin.com',
            'token': '',
            'usertype': '',
            'appver': '84',
            'apptype': 'android',
            'content-type': 'application/json; charset=UTF-8',
            'content-length': '341',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/5.0.0-alpha.2'
        }

        # Prompting user to send login credentials
        editable = await m.reply_text("Send ID & Password in this manner otherwise bot will not respond.\n\nSend like this:-  ID*Password \n or \nSend TOKEN like This this:-  TOKEN")

        # Listening for user input
        input1: Message = await bot.listen(editable.chat.id)
        raw_text = input1.text
        s = requests.Session()

        # Handling login based on user input
        if "*" in raw_text:
            # Extracting email and password from user input
            data["email"] = raw_text.split("*")[0]
            data["password"] = raw_text.split("*")[1]
            await input1.delete(True)

            # Sending login request
            response = s.post(url=url, headers=headers, json=data, timeout=10)

            # Processing login response
            if response.status_code == 200:
                # Extracting token from response
                data = response.json()
                token = data["data"]["token"]
                await editable.edit("login Successful")
                await m.reply_text(token)
            else:
                await m.reply_text("go back to response")
        else:
            token = raw_text

        # Retrieving batch data using token
        url1_response = s.get("https://elearn.crwilladmin.com/api/v5/my-batch", headers=headers, data=data)
        cool = ""  # Initialize the 'cool' variable here
        FFF = ""  # Initialize the 'FFF' variable here

        # Attempt to parse JSON response
        url1_data = url1_response.json()
        b_data = url1_data.get("data", {}).get("batchData", [])

        # Check if 'data' key exists in the response
        if not b_data:
            print("Error: 'data' key not found in response")
        else:
            # Formatting and sending batch data to user
            for data in b_data:
                FFF = "BATCH-ID - BATCH NAME - INSTRUCTOR"
                aa = f"`{data['id']}```\nBatch Name -{data['batchName']}\nBy - {data['instructorName']}\n\n"
                if len(f'{cool}{aa}') > 4096:
                    await m.reply_text(aa)
                    cool = ""
                cool += aa
# Editing the original message to display batch information
            await editable.edit(f'{"You have these batches :-"}\n\n{FFF}\n\n{cool}')

            # Prompting user to send Batch ID for downloading topics
            editable1 = await m.reply_text("Now send the Batch ID to Download")
            input2 = message = await bot.listen(editable.chat.id)
            raw_text2 = input2.text

            # Continue with your code...

    except Exception as e:
        print("Error occurred:", e)
        await m.reply_text("An error occurred. Please try again later.")

        # Continue with your code...
        url2 = s.get("https://elearn.crwilladmin.com/api/v5/batch-topic/" + raw_text2 + "?type=class", headers=headers, data=payload)
        topicid = url2.json()["data"]["batch_topic"]
        bn = url2.json()["data"]["batch_detail"]["name"]
    # Sending batch details to user
#    await m.reply_text(f'Batch details of **{bn}** are :')
#    cool1 = ""
        vj=""
        for data in topicid:
            tids = (data["id"])
            idid=f"{tids}&"
            if len(f"{vj}{idid}")>4096:
                await m.reply_text(idid)
                vj = ""
            vj+=idid
            
        
        
        vp = ""
        for data in topicid:
            tn = (data["topicName"])
            tns=f"{tn}&"
            if len(f"{vp}{tn}")>4096:
                await m.reply_text(tns)
                vp=""
            vp+=tns
        cool1 = ""               
        # Iterating over topics and retrieving details
        for data in topicid:
            t_name = (data["topicName"].replace(" ", ""))
            tid = (data["id"])
            scraper = cloudscraper.create_scraper()
            ffx = s.get("https://elearn.crwilladmin.com/api/v5/batch-detail/" + raw_text2 + "?redirectBy=mybatch&b_data=" + tid + ", headers=headers, data=payload ")
            vcx = ffx["data"]["class_list"]["batchDescription"]
            vvx = ffx["data"]["class_list"]["classes"]
            vvx.reverse()
            zz = len(vvx)
            BBB = f"{'**TOPIC-ID - TOPIC - VIDEOS**'}"
            hh = f"```{tid}```     - **{t_name} - ({zz})**\n"
            hh = f"**Topic -** {t_name}\n**Topic ID - ** ```{tid}```\nno. of videos are : {zz}\n\n"
            if len(f'{cool1}{hh}') > 4096:
                await m.reply_text(hh)
                cool1 = ""
            cool1 += hh
        
        # Sending batch details to user
        await m.reply_text(f'Batch details of **{bn}** are:\n\n{BBB}\n\n{cool1}\n\n**{vcx}**')
        
        # Prompting user for Topic IDs for downloading
        editable2 = await m.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n```{vj}```")    
        input3 = message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        
        try:
            # Splitting Topic IDs
            xv = raw_text3.split('&')
            
            # Iterating over Topic IDs for downloading
            for y in range(0, len(xv)):
                t = xv[y]
                
                # Retrieving details of each Topic ID
                html4 = s.get("https://elearn.crwilladmin.com/api/v5/batch-detail/" + raw_text2 + "?redirectBy=mybatch&b_data=" + t + "&token=" + token).content
                ff = json.loads(html4)
                mm = ff["data"]["class_list"]["batchName"].replace("/ ", " ")
                vv = ff["data"]["class_list"]["classes"]
                vv.reverse()
                count = 1
                
                try:
                    # Iterating over videos in the topic
                    for data in vv:
                        vidid = data["id"]
                        lessonName = data["lessonName"].replace("/", "_")
                        bcvid = data["lessonUrl"][0]["link"]
                        
                        # Handling video sources
                        if bcvid.startswith("62"):
                            try:
                                html6 = s.get(f"{bc_url}/{bcvid}", headers=bc_hdr).content
                                video = json.loads(html6)
                                video_source = video["sources"][5]
                                video_url = video_source["src"]
                                html5 = s.get("https://elearn.crwilladmin.com/api/v5/livestreamToken?type=brightcove&vid=" + vidid + "&token=" + token).content
                                surl = json.loads(html5)
                                stoken = surl["data"]["token"]
                                link = video_url + "&bcov_auth=" + stoken
                            except Exception as e:
                                print(str(e))
                        elif bcvid.startswith("63"):
                            try:
                                html7 = s.get(f"{bc_url}/{bcvid}", headers=bc_hdr).content
                                video1 = json.loads(html7)
                                video_source1 = video1["sources"][5]
                                video_url1 = video_source1["src"]
                                html8 = s.get("https://elearn.crwilladmin.com/api/v5/livestreamToken?type=brightcove&vid=" + vidid + "&token=" + token).content
                                surl1 = json.loads(html8)
                                stoken1 = surl1["data"]["token"]
                                link = video_url1 + "&bcov_auth=" + stoken1
                            except Exception as e:
                                print(str(e))
                        else:
                            link = "https://www.youtube.com/embed/" + bcvid
                        
                        # Writing video details to a text file
                        cc = f"{lessonName}::{link}"
                        with open(f"{mm}{t_name}.txt", 'a') as f:
                            f.write(f"{lessonName}:{link}\n")
                except Exception as e:
                    await m.reply_text(str(e))
            
            # Sending the text file containing video details to user
            await m.reply_document(f"{mm}{t_name}.txt")
        
        except Exception as e:
            await m.reply_text(str(e))
        
        # Prompting user for downloading notes
        try:
            notex = await m.reply_text("Do you want download notes ?\n\nSend **y** or **n**")
            input5 = message = await bot.listen(editable.chat.id)
            raw_text5 = input5.text
            
            if raw_text5 == 'y':
                # Retrieving PDF details for the batch
                scraper = cloudscraper.create_scraper()
                html7 = scraper.get("https://elearn.crwilladmin.com/api/v5/batch-notes/" + raw_text2 + "?b_data=" + raw_text2 + "&token=" + token).content
                pdfD = json.loads(html7)
                k = pdfD["data"]["notesDetails"]
                bb = len(pdfD["data"]["notesDetails"])
                ss = f"Total PDFs Found in Batch id **{raw_text2}** is - **{bb}** "
                await m.reply_text(ss)
                k.reverse()
                count1 = 1
                
                # Iterating over PDFs and saving them to text file
                try:
                    for data in k:
                        name = data["docTitle"]
                        s = data["docUrl"] 
                        xi = data["publishedAt"]
                        with open(f"{mm}{t_name}.txt", 'a') as f:
                            f.write(f"{name}:{s}\n")
                        continue
                    await m.reply_document(f"{mm}{t_name}.txt")
                except Exception as e:
                    await m.reply_text(str(e))
        
        except Exception as e:
            print(str(e))
        
        await m.reply_text("Done")        

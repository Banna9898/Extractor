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
ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1VmXspFMod94-pT7xDCvmBEYt8U7f0mRB6XnG5huPE7I9qjhDW0qpx3LRyTD9WX7W6JvUGtgKN-qf1pJoZO-QXBMIykDivtAOgkJOmN-kyv4m_F0thrJ45z95hqWON0nsKBwvd"
bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}
@bot.on_message(filters.command("cwd"))
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
           await editable.edit(f"**login Successful**\n\n**Token :** `{token}`")
        else:
           token = raw_text
           print('Token :- '+token)
           await editable.edit("**login Successful**")
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
    url1 = requests.get("https://elearn.crwilladmin.com/api/v3/my-batch", headers=headers)
    b_data = url1.json()['data']['batchData']

    cool=""
    for data in b_data:
        FFF="**BATCH-ID - BATCH NAME - INSTRUCTOR**"
        aa =f" `{data['id']}` - **{data['batchName']}** By {data['instructorName']}\n\n"
        #aa=f"**Batch Name -** {data['batchName']}\n**Batch ID -** ```{data['id']}```\n**By -** {data['instructorName']}\n\n"
        if len(f'{cool}{aa}')>4096:
            await m.reply_text(aa)
            cool =""
        cool+=aa
    await editable.edit(f'**You have these batches :-**\n\n{FFF}\n\n{cool}')
    await m.reply_text(f'**Login Token :** `{token}`')

    editable1= await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

# topic id url = https://elearn.crwilladmin.com/api/v1/comp/batch-topic/881?type=class&token=d76fce74c161a264cf66b972fd0bc820992fe576
    url2 = requests.get("https://elearn.crwilladmin.com/api/v3/batch-topic/"+raw_text2+"?type=class", headers=headers)
    topicid = url2.json()["data"]["batch_topic"]
    bn =url2.json()["data"]["batch_detail"]["name"]
#     await m.reply_text(f'Batch details of **{bn}** are :')
    vj=""
    for data in topicid:
        tids = (data["id"])
        idid=f"{tids}&"
        if len(f"{vj}{idid}")>4096:
            await m.reply_text(idid)
            vj = ""
        vj+=idid
        
    vl=""
    for data in topicid:
        tds = (data["id"])
        tsn = (data["topicName"])
        idsd=f"{tds}*{tsn}&"
        if len(f"{vl}{idsd}")>4096:
            await m.reply_text(idsd)
            vl = ""
        vl+=idsd
    
    vp = ""
    for data in topicid:
        tn = (data["topicName"])
        tns=f"{tn}&"
        if len(f"{vp}{tn}")>4096:
            await m.reply_text(tns)
            vp=""
        vp+=tns
        
    cool1 = ""    
    for data in topicid:
        t_name=(data["topicName"])
        tid = (data["id"])
        
        urlx = f"https://elearn.crwilladmin.com/api/v3/batch-detail/{raw_text2}?topicId={tid}"
        ffx = requests.get(urlx, headers=headers)
        vcx =ffx.json()["data"]["class_list"]["batchDescription"]
        vvx =ffx.json()["data"]["class_list"]["classes"]
        vvx.reverse()
        zz= len(vvx)
        BBB = f"{'**TOPIC-ID * TOPIC - VIDEOS**'}"
        hh = f"`{tid}*{t_name}` - **({zz})**\n"
        
        #if len(f'{cool1}{hh}')>4096:
        #    await m.reply_text(hh)
        #    cool1=""
        cool1+=hh
    await m.reply_text(f'Batch details of **{bn}** are:\n\n{BBB}\n\n{cool1}\n\n**{vcx}**')
#     await m.reply_text(f'**{vcx}**')
#     await m.reply_text(f'```{vj}```')

    editable3= await m.reply_text("**Now send the Resolution**")
    input4 = message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text

    editable4= await m.reply_text("Now send the **Thumb url** Eg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text


    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
    
    editable2= await m.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n`{vl}`")
    
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    try:
        xv = raw_text3.split('&')
        for y in range(0,len(xv)):
            av =xv[y]
            t = av.split('*')[0]
            va = av.split('*')[1]
            url3 = f"https://elearn.crwilladmin.com/api/v3/batch-detail/{raw_text2}?topicId={t}" 
            ff = requests.get(url3, headers=headers)
            #vc =ff.json()["data"]["class_list"]["batchDescription"]
            mm = ff.json()["data"]["class_list"]["batchName"]
            
            vv =ff.json()["data"]["class_list"]["classes"]
            vv.reverse()
            #clan =f"**{vc}**\n\nNo of links found in topic-id {raw_text3} are **{len(vv)}**"
            #await m.reply_text(clan)
            count = 1
            try:
                for data in vv:
                    vidid = (data["id"])
                    lessonName = (data["lessonName"]).replace("/", "_").replace(":", "_").replace("|", "_")
                    bcvid = (data["lessonUrl"])
#                     lessonName = re.sub('\|', '_', cf)
                    if bcvid.startswith("62"):
                        try:
                            video_response = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                            video = video_response.json()
                            video_source = video["sources"][5]
                            video_url = video_source["src"]
                            #print(video_url)

                            surl=requests.get("https://elearn.crwilladmin.com/api/v3/livestreamToken?base=web&type=brightcove&vid="+vidid, headers=headers)
                            stoken = surl.json()["data"]["token"]
                            #print(stoken)

                            link = video_url+"&bcov_auth="+stoken
                            #print(link)
                        except Exception as e:
                            print(str(e))
                    elif bcvid.startswith("63"):  
                        try:
                            video_response = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                            video = video_response.json()
                            #print(video)
                            video_source = video["sources"][5]
                            video_url = video_source["src"]
                            #print(video_url)
                            surl=requests.get("https://elearn.crwilladmin.com/api/v3/livestreamToken?base=web&type=brightcove&vid="+vidid, headers=headers)
                            stoken = surl.json()["data"]["token"]
                            #print(stoken)
                            #link = f"{lessonName}:{video_url}&bcov_auth={stoken}\n"
                            link = video_url+"&bcov_auth="+stoken
                            #print(link)
                            #pv += link
                        except Exception as e:
                            print(e)    
                    else:
                        link="https://www.youtube.com/embed/"+bcvid
                    # await m.reply_text(link)

                    #editable3= await m.reply_text("**Now send the Resolution**")
                    #input4 = message = await bot.listen(editable.chat.id)
                    #raw_text4 = input4.text

                    cc = f"{str(count).zfill(3)}.{lessonName}.mp4\n\n**Topic :-** {va}\n**Batch :** {mm}"
                    Show = f"**Downloading:-**\n**Title -** ```{lessonName}\n\nQuality - {raw_text4}```\n\n**Url :-** `{link}`"
                    prog = await m.reply_text(Show)

                    if "youtu" in link:
                        if raw_text4 in ["144", "240", "480"]:
                            ytf = f'bestvideo[height<={raw_text4}][ext=mp4]+bestaudio[ext=m4a]'
                        elif raw_text4 == "360":
                            ytf = 18
                        elif raw_text4 == "720":
                            ytf = 22
                        else:
                            ytf = 18
                    else:
                        ytf=f"bestvideo[height<={raw_text4}]"
                        
                    if ytf == f'bestvideo[height<={raw_text4}][ext=mp4]+bestaudio[ext=m4a]':
                        cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}" "{link}"'
                    else:
                        cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}+bestaudio" "{link}"'


                    #cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}+bestaudio" "{link}"'
                    try:
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25 -N 60 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                        os.system(download_cmd)
                        

                        filename = f"{lessonName}.mp4"
#                         await prog.delete (True)
#                         reply = await m.reply_text("Uploading Video")
                        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:19 -vframes 1 "{filename}.jpg"', shell=True)
    
                        #thumbnail = f"{filename}.jpg"
                        await prog.delete (True)
                        reply = await m.reply_text("Uploading Video")
                        

                        try:
                            if thumb == "no":
                                thumbnail = f"{filename}.jpg"
                            else:
                                thumbnail = thumb
                        except Exception as e:
                            await m.reply_text(str(e))



                        dur = int(helper.duration(filename))
#                         await prog.delete (True)
                        start_time = time.time()
                        await m.reply_video(f"{lessonName}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
                        count+=1
                        os.remove(f"{lessonName}.mp4")
                        
                        os.remove(f"{filename}.jpg")
                        await reply.delete (True)
                    except Exception as e:
                        await m.reply_text(f"**Video downloading failed ❌**\n{str(e)}")
                        continue
            except Exception as e:
                await m.reply_text(str(e))
            
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")

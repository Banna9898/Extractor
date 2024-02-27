from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys


@bot.on_message(filters.command(["start"]))
async def Start_msg(bot: bot , m: Message):
    await bot.send_photo(
    m.chat.id,
    photo="https://telegra.ph/file/0eca3245df8a40c7e68d4.jpg",
    caption = "**Hi i am All in One Extractor Bot**")
           
@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, m):
    await m.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["log"]))
async def log_msg(bot: bot , m: Message):   
    await bot.send_document(m.chat.id, "log.txt")

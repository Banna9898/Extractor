from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys


# async def start_command(client, message):
#     Create an inline keyboard with a button
#     keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Open /khan", callback_data="open_khan")]])
    
#     Send a message with the inline keyboard
#     await message.reply_text("Tap the button below to open /khan", reply_markup=keyboard)

# Define a handler for inline keyboard button clicks
# @app.on_callback_query()
# async def callback_handler(client, callback_query):
#     Check if the callback data is "open_khan"
#     if callback_query.data == "open_khan":
#         Trigger the /khan command
#         await callback_query.message.reply_text("/khan")
           

@bot.on_message(filters.command(["start"]))
async def start_msg(bot: bot, message: Message):
    # Send a photo with a caption
    await bot.send_photo(
        message.chat.id,
        photo="https://telegra.ph/file/0eca3245df8a40c7e68d4.jpg",
        caption="**Hi, I am All in One Extractor Bot**"
    )

# Define /start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(client, message):
    # Create an inline keyboard with multiple buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Button 1", callback_data="button1"),
                InlineKeyboardButton("Button 2", callback_data="button2")
            ],
            [
                InlineKeyboardButton("Button 3", callback_data="button3"),
                InlineKeyboardButton("Button 4", callback_data="button4")
            ]
        ]
    )

    # Send a message with the inline keyboard
    await message.reply_text("Choose an option:", reply_markup=keyboard)

# Define a handler for inline keyboard button clicks
@bot.on_callback_query()
async def callback_handler(client, callback_query):
    # Check which button is clicked based on the callback data
    if callback_query.data == "button1":
        await callback_query.message.reply_text("You clicked Button 1!")
    elif callback_query.data == "button2":
        await callback_query.message.reply_text("You clicked Button 2!")
    elif callback_query.data == "button3":
        await callback_query.message.reply_text("You clicked Button 3!")
    elif callback_query.data == "button4":
        await callback_query.message.reply_text("You clicked Button 4!")

# Define restart command handler
@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, message):
    await message.reply_text("Restarted!", True)
    # Restart the bot
    os.execl(sys.executable, sys.executable, *sys.argv)

# Define log command handler
@bot.on_message(filters.command(["log"]))
async def log_msg(bot: bot, message: Message):
    # Send the log file
    await bot.send_document(message.chat.id, "log.txt")

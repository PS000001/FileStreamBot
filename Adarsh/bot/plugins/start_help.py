from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters, ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)

button_main_channel = InlineKeyboardButton("Main Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
button_owner = InlineKeyboardButton("Owner", url="https://t.me/MadAsGhost")
button_support_channel = InlineKeyboardButton("Join Support Channel", url=f"https://t.me/{Var.SUPPORT_CHANNEL}")

buttons = [
    [button_main_channel],
    [button_owner]
]

@StreamBot.on_message((filters.command("start")) & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**New User Joined:** \n\n__My New Friend__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Started Your Bot!!__"
        )

    try:
        user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
        if user.status == "kicked":
            await b.send_message(
                chat_id=m.chat.id,
                text="__Sorry, You Are Banned Using Me. Contact Developer__\n\n  **He Will Help You**",
                disable_web_page_preview=True
            )
            return
    except UserNotParticipant:
        await b.send_photo(
            chat_id=m.chat.id,
            photo="https://graph.org/file/d454b953103d42d759f8d.jpg",
            text="To access the bot's features, please join the support channel by clicking the button below:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [button_support_channel]
                ]
            )
        )
        return

    await b.send_message(
        chat_id=m.chat.id,
        text="""<b> Send me any file or video i will give you streamable link and download link.</b>\n
<b> I also support Channels, add me to you Channel and send any media files and see miracle✨ also send /list to know all commands""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@StreamBot.on_message((filters.command("help") | filters.regex('help📚')) & filters.private )
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**New User Joined:** \n\n__My New Friend__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot!!__"
        )

    try:
        user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Sorry, You Are Banned Using Me. Contact Developer__\n\n  **He Will Help You**",
                disable_web_page_preview=True
            )
            return
    except UserNotParticipant:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://graph.org/file/d454b953103d42d759f8d.jpg",
            text="To access the bot's features, please join the support channel by clicking the button below:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [button_support_channel]
                ]
            )
        )
        return

    await bot.send_message(
        chat_id=message.chat.id,
        text="""<b> Send me any file or video i will give you streamable link and download link.</b>\n
<b> I also support Channels, add me to you Channel and send any media files and see miracle✨ also send /list to know all commands""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

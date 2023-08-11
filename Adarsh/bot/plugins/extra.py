import time
import shutil
import psutil
import platform
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Adarsh.bot import StreamBot
from utils_bot import *
from Adarsh import StartTime

total_users = 0

def get_uptime():
    uptime = time.time() - StartTime
    return time.strftime("%H:%M:%S", time.gmtime(uptime))

@StreamBot.on_message(filters.command("start"))
async def start_handler(_, message):
    global total_users
    total_users += 1
    await message.reply_text("Welcome to the bot!")

@StreamBot.on_message(filters.command("about"))
async def about_handler(bot, message):
    user = message.from_user
    user_info = f'⌬<b><i><u>User Information</u></i></b>\n\n'\
                f'├ <b>Username:</b> @{user.username}\n'\
                f'├ <b>Chat ID:</b> {message.chat.id}\n'\
                f'├ <b>DC:</b> {user.dc_id}\n'
    
    buttons = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Ping", callback_data="ping")],
        [InlineKeyboardButton("Status", callback_data="status")],
        [InlineKeyboardButton("Info", callback_data="info")]
    ]
    
    keyboard = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(user_info + "\nChoose a feature:", reply_markup=keyboard)

@StreamBot.on_callback_query
async def show_feature_info(bot, callback_query):
    feature = callback_query.data
    detailed_info = ""
    
    if feature == "help":
        detailed_info = "Need help? Here is a list of all available commands:\n\n"\
                        "/start - Start the bot\n"\
                        "/help - Display help message\n"\
                        "/about - Show user and system information\n"\
                        "/ping - Measure bot's response time\n"\
                        "/status - Display system status\n"\
    elif feature == "ping":
        start_t = time.time()
        ag = await callback_query.message.reply_text("....")
        end_t = time.time()
        time_taken_s = (end_t - start_t) * 1000
        detailed_info = f"Pong!\n{time_taken_s:.3f} ms"
    elif feature == "status":
        # Get system status and create detailed info
        currentTime = readable_time((time.time() - StartTime))
        total, used, free = shutil.disk_usage('.')
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
        recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpuUsage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        botstats = f'⌬<b><i><u>Bot Statistics</u></i></b>\n\n'\
                   f'╭ <b>Bot Uptime:</b> {currentTime}\n'\
                   f'├ <b>Total Users:</b> {total_users}\n'\
                   f'├ <b>Total disk:</b> {total}\n'\
                   f'├ <b>Used:</b> {used} \n'\
                   f'├ <b>Free:</b> {free}\n'\
                   f'├ Data Usage\n<b>Upload:</b> {sent}\n'\
                   f'├ <b>Down:</b> {recv}\n'\
                   f'├ <b>CPU:</b> {cpuUsage}% \n'\
                   f'├ <b>RAM:</b> {memory}% \n'\
                   f'╰ <b>Disk:</b> {disk}%\n\n'\
                   f'⌬-------<b>[Tomen](https://t.me/TomenMain)</b>--------⌬'
        detailed_info = f"{botstats}\n\n<b>Click 'Back' to go back or 'Close' to close.</b>"
    elif feature == "info":
        system_info = f'⌬<b><i><u>System Information</u></i></b>\n\n'\
                      f'├ <b>Host On :</b> [Heroku](https://heroku.com)\n'\
                      f'├ <b>Deployed By:</b> [Tomen](https://t.me/TomenMain)\n'\
                      f'├ <b>Python Version:</b> 3.8\n'\
                      f'├ <b>Bot Version:</b> 1.0\n'\
                      f'╰ <b>Developed by:</b> [Developer](https://github.com/BalaPriyan)'
        detailed_info = system_info
    
    back_button = InlineKeyboardButton("Back", callback_data="about")
    close_button = InlineKeyboardButton("Close", callback_data="close")
    buttons = [[back_button, close_button]]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await callback_query.edit_message_text(detailed_info, reply_markup=keyboard, parse_mode="html")


@StreamBot.on_callback_query(filters.regex("^about$"))
async def back_to_about(bot, callback_query):
    await about_handler(bot, callback_query.message)

@StreamBot.on_callback_query(filters.regex("^close$"))
async def close_detailed_info(bot, callback_query):
    await callback_query.message.delete()

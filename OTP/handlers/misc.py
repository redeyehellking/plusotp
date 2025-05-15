from pyrogram import Client, filters
from pyrogram.types import Message
from constants import HELP_TEXT, BALANCE_TEXT, HELP_TEXTA
from OTP.database.database import fetch_user_data
from config import OWNER_ID, SUDO_USERS
from pyrogram.enums import ParseMode

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    if message.from_user.id == OWNER_ID:
        await message.reply_text(HELP_TEXTA, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

@Client.on_message(filters.command(["balance", "info"]) & filters.private)
async def balance_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = await fetch_user_data(user_id)
    if user_data:
        user_details = f"**💰 Account Balance:** `${user_data['balance']}`\n**📦 Numbers Bought:** `{user_data['number_bought']}`\n**🔄 Transactions:** `{user_data['transaction_count']}`"    
        await message.reply_text(user_details, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply_text("❌ **Account Not Found!**\nPlease start the bot first using /start", parse_mode=ParseMode.MARKDOWN)

@Client.on_message(filters.command("ping") & filters.private)
async def ping_command(client: Client, message: Message):
    start_time = message.date
    ping_message = await message.reply_text("🏓 Pinging...")
    end_time = ping_message.date
    ping_time = (end_time - start_time).microseconds / 1000
    await ping_message.edit_text(f"**⏱ Pong!**\nLatency: `{ping_time:.2f} ms`", parse_mode=ParseMode.MARKDOWN)

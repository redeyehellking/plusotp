from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import UPI_ID, OWNER_ID, USDT_TRC20, USDT_BEP20, BINANCE
from OTP.utils.helpers import generate_qr_code
from OTP.database.database import fetch_user_data, update_user_data
from constants import DEPOSIT_TEXT
from pyrogram.enums import ParseMode

deposit_messages = {}

@Client.on_message(filters.command("deposit") & filters.private)
async def deposit(client: Client, message: Message):
    await message.reply_text(DEPOSIT_TEXT, reply_markup=deposit_amount_keyboard(), parse_mode=ParseMode.MARKDOWN)

def deposit_amount_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("💵 Custom Deposit", callback_data="custom_deposit")]])

def payment_method_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("INR", callback_data="payment_inr"), InlineKeyboardButton("Crypto (USDT)", callback_data="payment_crypto")]
    ])

@Client.on_callback_query(filters.regex(r'^custom_deposit$'))
async def custom_deposit(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Choose payment method from following available options:", reply_markup=payment_method_keyboard())

@Client.on_callback_query(filters.regex(r'^payment_(inr|crypto)$'))
async def handle_payment_method(client: Client, callback_query: CallbackQuery):
    payment_method = callback_query.matches[0].group(1)
    user_id = callback_query.from_user.id
    await callback_query.message.edit_text("💵 **Enter the deposit amount:**", parse_mode=ParseMode.MARKDOWN)
    
    try:
        amount_message = await client.listen(user_id)
        amount = int(amount_message.text)
    except:
        await callback_query.message.reply_text("⚠️ Please enter a valid number.")
        return
    
    if payment_method == "inr":
        qr_code = generate_qr_code(UPI_ID, amount)
        caption = f"**🔍 Payment Instructions (INR)**\n\n💳 Amount: ₹{amount}\n\n📲 Scan QR or send to:\n`{UPI_ID}`\n\n📸 Reply with payment screenshot after sending"
        deposit_message = await callback_query.message.reply_photo(qr_code, caption=caption, parse_mode=ParseMode.MARKDOWN)
    else:
        caption = f"**🔍 Payment Instructions (USDT)**\n\n💳 Amount: ${amount}\n\n🌐 USDT TRC20 Address:\n`{USDT_TRC20}`\n\n🌐 USDT BEP20 Address:\n`{USDT_BEP20}`\n\n🌐 Binance ID:\n`{BINANCE}`\n\n📸 Reply with payment screenshot after sending"
        deposit_message = await callback_query.message.reply_text(caption, parse_mode=ParseMode.MARKDOWN)
    
    deposit_messages[user_id] = {"message_id": deposit_message.id, "amount": amount, "payment_method": payment_method}

@Client.on_message(filters.photo & filters.private)
async def handle_payment_screenshot(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in deposit_messages and message.reply_to_message and message.reply_to_message.id == deposit_messages[user_id]["message_id"]:
        data = deposit_messages[user_id]
        currency = "₹" if data["payment_method"] == "inr" else "$"
        forwarded_msg = await message.forward(OWNER_ID)
        await forwarded_msg.reply_text(f"**📤 New Deposit Request**\n\n👤 User: `{user_id}`\n💵 Amount: {currency}{data['amount']}\n💳 Method: `{data['payment_method'].upper()}`\n\n⚡ Approve with:\n`/addbalance {user_id} {data['amount']}`", parse_mode=ParseMode.MARKDOWN)
        await message.reply_text("**📨 Payment Received!**\nAdmin notified! Balance will update within 24 hours.", parse_mode=ParseMode.MARKDOWN)
        del deposit_messages[user_id]
    else:
        await message.reply_text("⚠️ **Invalid Submission!**\nReply to the deposit message with your screenshot.", parse_mode=ParseMode.MARKDOWN)
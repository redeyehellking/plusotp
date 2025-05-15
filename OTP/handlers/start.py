from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from OTP.utils.keyboards import start_keyboard
from OTP.database.database import add_user_data, fetch_user_data, users_db, count_referrals
from constants import START_TEXT, START_IMG
from pyrogram.enums import ParseMode

@Client.on_message(filters.command(["start", "buy"]) & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = await fetch_user_data(user_id)
    referrer_id = None

    
    if not user_data:
        if len(message.command) > 1 and message.command[0] == 'start':
            param = message.command[1]
            try:
                referrer_id = int(param)

                if referrer_id == user_id:
                    referrer_id = None
                else:
                    referrer_data = await fetch_user_data(referrer_id)
                    if not referrer_data:
                        referrer_id = None
            except ValueError:
                referrer_id = None

      
        await add_user_data(user_id, referrer=referrer_id)

       
        if referrer_id:

            await users_db.update_one(
                {"user_id": referrer_id},
                {"$inc": {"balance": 0.5}}
            )

            try:
                await client.send_message(
                    chat_id=referrer_id,
                    text="🎉 You referred a new user! $0.5 has been added to your balance."
                )
            except:
                pass

            await message.reply_text("👋 Thanks for using the referral link! Your referrer earned $0.5.")

    await message.reply_photo(
        photo=START_IMG,
        caption=START_TEXT,
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("refer") & filters.private)
async def refer_command(client: Client, message: Message):
    user_id = message.from_user.id
    bot_username = (await client.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"
    referral_count = await count_referrals(user_id)
    
    await message.reply_text(
        f"**📊 Your Referral Stats**\n\n"
        f"🔗 Your Link: `{referral_link}`\n"
        f"👥 Total Referrals: {referral_count}\n"
        f"💰 Earned: ${referral_count * 0.5}\n\n"
        "Invite friends to earn $0.5 for each successful referral!",
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_callback_query(filters.regex(r'^refer_stats$'))
async def show_refer_stats(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bot_username = (await client.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"
    referral_count = await count_referrals(user_id)
    
    await callback_query.edit_message_text(
        f"**📊 Referral Program**\n\n"
        f"🔗 Your Referral Link:\n`{referral_link}`\n\n"
        f"👥 Total Referrals: `{referral_count}`\n"
        f"💰 Earned: `${referral_count * 0.5:.2f}`\n\n"
        "**How it works:**\n"
        "1. Share your link with friends\n"
        "2. When they join using your link\n"
        "3. You get $0.5 for each successful referral!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("↩️ Back", callback_data="back_to_start")]
        ]),
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_callback_query(filters.regex(r'^back_to_start$'))
async def back_to_start(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        text=START_TEXT,
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )   
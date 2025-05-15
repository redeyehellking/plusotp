from pyrogram import Client, filters
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, 
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid
)
from pyrogram.types import Message
from config import SUDO_USERS, API_ID, API_HASH, OWNER_ID
from OTP.database.database import add_otp_data, delete_otp_data, update_user_data, fetch_user_data, get_total_stats, fetch_all_user_ids
from pyrogram.enums import ParseMode

country_codes = {
    "🇦🇫 Afghanistan": "+93",
    "🇦🇱 Albania": "+355",
    "🇩🇿 Algeria": "+213",
    "🇦🇸 American Samoa": "+1-684",
    "🇦🇩 Andorra": "+376",
    "🇦🇴 Angola": "+244",
    "🇦🇮 Anguilla": "+1-264",
    "🇦🇶 Antarctica": "+672",
    "🇦🇬 Antigua and Barbuda": "+1-268",
    "🇦🇷 Argentina": "+54",
    "🇦🇲 Armenia": "+374",
    "🇦🇼 Aruba": "+297",
    "🇦🇺 Australia": "+61",
    "🇦🇹 Austria": "+43",
    "🇦🇿 Azerbaijan": "+994",
    "🇧🇸 Bahamas": "+1-242",
    "🇧🇭 Bahrain": "+973",
    "🇧🇩 Bangladesh": "+880",
    "🇧🇧 Barbados": "+1-246",
    "🇧🇾 Belarus": "+375",
    "🇧🇪 Belgium": "+32",
    "🇧🇿 Belize": "+501",
    "🇧🇯 Benin": "+229",
    "🇧🇲 Bermuda": "+1-441",
    "🇧🇹 Bhutan": "+975",
    "🇧🇴 Bolivia": "+591",
    "🇧🇦 Bosnia and Herzegovina": "+387",
    "🇧🇼 Botswana": "+267",
    "🇧🇷 Brazil": "+55",
    "🇮🇴 British Indian Ocean Territory": "+246",
    "🇻🇬 British Virgin Islands": "+1-284",
    "🇧🇳 Brunei": "+673",
    "🇧🇬 Bulgaria": "+359",
    "🇧🇫 Burkina Faso": "+226",
    "🇧🇮 Burundi": "+257",
    "🇰🇭 Cambodia": "+855",
    "🇨🇲 Cameroon": "+237",
    "🇨🇦 Canada": "+1",
    "🇨🇻 Cape Verde": "+238",
    "🇧🇶 Caribbean Netherlands": "+599",
    "🇰🇾 Cayman Islands": "+1-345",
    "🇨🇫 Central African Republic": "+236",
    "🇹🇩 Chad": "+235",
    "🇨🇱 Chile": "+56",
    "🇨🇳 China": "+86",
    "🇨🇽 Christmas Island": "+61",
    "🇨🇨 Cocos (Keeling) Islands": "+61",
    "🇨🇴 Colombia": "+57",
    "🇰🇲 Comoros": "+269",
    "🇨🇬 Congo": "+242",
    "🇨🇩 Congo (DRC)": "+243",
    "🇨🇰 Cook Islands": "+682",
    "🇨🇷 Costa Rica": "+506",
    "🇭🇷 Croatia": "+385",
    "🇨🇺 Cuba": "+53",
    "🇨🇼 Curaçao": "+599",
    "🇨🇾 Cyprus": "+357",
    "🇨🇿 Czechia": "+420",
    "🇩🇰 Denmark": "+45",
    "🇩🇯 Djibouti": "+253",
    "🇩🇲 Dominica": "+1-767",
    "🇩🇴 Dominican Republic": "+1-809",
    "🇪🇨 Ecuador": "+593",
    "🇪🇬 Egypt": "+20",
    "🇸🇻 El Salvador": "+503",
    "🇬🇶 Equatorial Guinea": "+240",
    "🇪🇷 Eritrea": "+291",
    "🇪🇪 Estonia": "+372",
    "🇸🇿 Eswatini": "+268",
    "🇪🇹 Ethiopia": "+251",
    "🇫🇰 Falkland Islands": "+500",
    "🇫🇴 Faroe Islands": "+298",
    "🇫🇯 Fiji": "+679",
    "🇫🇮 Finland": "+358",
    "🇫🇷 France": "+33",
    "🇬🇫 French Guiana": "+594",
    "🇵🇫 French Polynesia": "+689",
    "🇬🇦 Gabon": "+241",
    "🇬🇲 Gambia": "+220",
    "🇬🇪 Georgia": "+995",
    "🇩🇪 Germany": "+49",
    "🇬🇭 Ghana": "+233",
    "🇬🇮 Gibraltar": "+350",
    "🇬🇷 Greece": "+30",
    "🇬🇱 Greenland": "+299",
    "🇬🇩 Grenada": "+1-473",
    "🇬🇵 Guadeloupe": "+590",
    "🇬🇺 Guam": "+1-671",
    "🇬🇹 Guatemala": "+502",
    "🇬🇬 Guernsey": "+44",
    "🇬🇳 Guinea": "+224",
    "🇬🇼 Guinea-Bissau": "+245",
    "🇬🇾 Guyana": "+592",
    "🇭🇹 Haiti": "+509",
    "🇭🇳 Honduras": "+504",
    "🇭🇰 Hong Kong": "+852",
    "🇭🇺 Hungary": "+36",
    "🇮🇸 Iceland": "+354",
    "🇮🇳 India": "+91",
    "🇮🇩 Indonesia": "+62",
    "🇮🇷 Iran": "+98",
    "🇮🇶 Iraq": "+964",
    "🇮🇪 Ireland": "+353",
    "🇮🇲 Isle of Man": "+44",
    "🇮🇱 Israel": "+972",
    "🇮🇹 Italy": "+39",
    "🇨🇮 Ivory Coast": "+225",
    "🇯🇲 Jamaica": "+1-876",
    "🇯🇵 Japan": "+81",
    "🇯🇪 Jersey": "+44",
    "🇯🇴 Jordan": "+962",
    "🇰🇿 Kazakhstan": "+7",
    "🇰🇪 Kenya": "+254",
    "🇰🇮 Kiribati": "+686",
    "🇽🇰 Kosovo": "+383",
    "🇰🇼 Kuwait": "+965",
    "🇰🇬 Kyrgyzstan": "+996",
    "🇱🇦 Laos": "+856",
    "🇱🇻 Latvia": "+371",
    "🇱🇧 Lebanon": "+961",
    "🇱🇸 Lesotho": "+266",
    "🇱🇷 Liberia": "+231",
    "🇱🇾 Libya": "+218",
    "🇱🇮 Liechtenstein": "+423",
    "🇱🇹 Lithuania": "+370",
    "🇱🇺 Luxembourg": "+352",
    "🇲🇴 Macao": "+853",
    "🇲🇬 Madagascar": "+261",
    "🇲🇼 Malawi": "+265",
    "🇲🇾 Malaysia": "+60",
    "🇲🇻 Maldives": "+960",
    "🇲🇱 Mali": "+223",
    "🇲🇹 Malta": "+356",
    "🇲🇭 Marshall Islands": "+692",
    "🇲🇶 Martinique": "+596",
    "🇲🇷 Mauritania": "+222",
    "🇲🇺 Mauritius": "+230",
    "🇾🇹 Mayotte": "+262",
    "🇲🇽 Mexico": "+52",
    "🇫🇲 Micronesia": "+691",
    "🇲🇩 Moldova": "+373",
    "🇲🇨 Monaco": "+377",
    "🇲🇳 Mongolia": "+976",
    "🇲🇪 Montenegro": "+382",
    "🇲🇸 Montserrat": "+1-664",
    "🇲🇦 Morocco": "+212",
    "🇲🇿 Mozambique": "+258",
    "🇲🇲 Myanmar": "+95",
    "🇳🇦 Namibia": "+264",
    "🇳🇷 Nauru": "+674",
    "🇳🇵 Nepal": "+977",
    "🇳🇱 Netherlands": "+31",
    "🇳🇨 New Caledonia": "+687",
    "🇳🇿 New Zealand": "+64",
    "🇳🇮 Nicaragua": "+505",
    "🇳🇪 Niger": "+227",
    "🇳🇬 Nigeria": "+234",
    "🇳🇺 Niue": "+683",
    "🇳🇫 Norfolk Island": "+672",
    "🇰🇵 North Korea": "+850",
    "🇲🇰 North Macedonia": "+389",
    "🇲🇵 Northern Mariana Islands": "+1-670",
    "🇳🇴 Norway": "+47",
    "🇴🇲 Oman": "+968",
    "🇵🇰 Pakistan": "+92",
    "🇵🇼 Palau": "+680",
    "🇵🇸 Palestine": "+970",
    "🇵🇦 Panama": "+507",
    "🇵🇬 Papua New Guinea": "+675",
    "🇵🇾 Paraguay": "+595",
    "🇵🇪 Peru": "+51",
    "🇵🇭 Philippines": "+63",
    "🇵🇳 Pitcairn Islands": "+64",
    "🇵🇱 Poland": "+48",
    "🇵🇹 Portugal": "+351",
    "🇵🇷 Puerto Rico": "+1-787",
    "🇶🇦 Qatar": "+974",
    "🇷🇪 Réunion": "+262",
    "🇷🇴 Romania": "+40",
    "🇷🇺 Russia": "+7",
    "🇷🇼 Rwanda": "+250",
    "🇼🇸 Samoa": "+685",
    "🇸🇲 San Marino": "+378",
    "🇸🇹 São Tomé and Príncipe": "+239",
    "🇸🇦 Saudi Arabia": "+966",
    "🇸🇳 Senegal": "+221",
    "🇷🇸 Serbia": "+381",
    "🇸🇨 Seychelles": "+248",
    "🇸🇱 Sierra Leone": "+232",
    "🇸🇬 Singapore": "+65",
    "🇸🇽 Sint Maarten": "+1-721",
    "🇸🇰 Slovakia": "+421",
    "🇸🇮 Slovenia": "+386",
    "🇸🇧 Solomon Islands": "+677",
    "🇸🇴 Somalia": "+252",
    "🇿🇦 South Africa": "+27",
    "🇰🇷 South Korea": "+82",
    "🇸🇸 South Sudan": "+211",
    "🇪🇸 Spain": "+34",
    "🇱🇰 Sri Lanka": "+94",
    "🇸🇩 Sudan": "+249",
    "🇸🇷 Suriname": "+597",
    "🇸🇪 Sweden": "+46",
    "🇨🇭 Switzerland": "+41",
    "🇸🇾 Syria": "+963",
    "🇹🇼 Taiwan": "+886",
    "🇹🇯 Tajikistan": "+992",
    "🇹🇿 Tanzania": "+255",
    "🇹🇭 Thailand": "+66",
    "🇹🇱 Timor-Leste": "+670",
    "🇹🇬 Togo": "+228",
    "🇹🇰 Tokelau": "+690",
    "🇹🇴 Tonga": "+676",
    "🇹🇹 Trinidad and Tobago": "+1-868",
    "🇹🇳 Tunisia": "+216",
    "🇹🇷 Turkey": "+90",
    "🇹🇲 Turkmenistan": "+993",
    "🇹🇨 Turks and Caicos Islands": "+1-649",
    "🇹🇻 Tuvalu": "+688",
    "🇺🇬 Uganda": "+256",
    "🇺🇦 Ukraine": "+380",
    "🇦🇪 United Arab Emirates": "+971",
    "🇬🇧 United Kingdom": "+44",
    "🇺🇸 United States": "+1",
    "🇺🇾 Uruguay": "+598",
    "🇺🇿 Uzbekistan": "+998",
    "🇻🇺 Vanuatu": "+678",
    "🇻🇦 Vatican City": "+39",
    "🇻🇪 Venezuela": "+58",
    "🇻🇳 Vietnam": "+84",
    "🇻🇬 British Virgin Islands": "+1-284",
    "🇻🇮 U.S. Virgin Islands": "+1-340",
    "🇼🇫 Wallis and Futuna": "+681",
    "🇪🇭 Western Sahara": "+212",
    "🇾🇪 Yemen": "+967",
    "🇿🇲 Zambia": "+260",
    "🇿🇼 Zimbabwe": "+263"
}

@Client.on_message(filters.command("add_numbers") & filters.user(SUDO_USERS))
async def add_numbers(client: Client, message: Message):
    user_id = message.chat.id
    await message.reply_text("📲 **Send Phone Number to Add**\n\nFormat: `+1234567890`", parse_mode=ParseMode.MARKDOWN)
    number_msg = await client.listen(user_id)
    number = number_msg.text

    user = Client(name=f"user_{user_id}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await user.connect()

    try:
        code = await user.send_code(number)
    except ApiIdInvalid:
        await message.reply_text("❌ **Invalid API Credentials!**\nCheck config.py settings")
        return
    except PhoneNumberInvalid:
        await message.reply_text("⚠️ **Invalid Phone Number!**\nEnsure proper country code format")
        return

    await message.reply_text("🔑 **Enter Received OTP**\n\nFormat: `1 2 3 4 5`")
    otp_msg = await client.listen(user_id)
    otp = otp_msg.text.replace(" ", "")

    try:
        await user.sign_in(number, code.phone_code_hash, otp)
    except PhoneCodeInvalid:
        await message.reply_text("❌ **Invalid OTP Code!**\nRestart process with /add_numbers")
        return
    except PhoneCodeExpired:
        await message.reply_text("⌛ **OTP Expired!**\nRequest new code and try again")
        return
    except SessionPasswordNeeded:
        await message.reply_text("🔒 **2FA Required!**\nEnter account password:")
        password_msg = await client.listen(user_id)
        password = password_msg.text
        try:
            await user.check_password(password)
        except PasswordHashInvalid:
            await message.reply_text("❌ **Wrong Password!**\nProcess cancelled")
            return

    session = await user.export_session_string()
    await message.reply_text("💵 **Set Number Price**\n\nEnter amount in USD:")
    price_msg = await client.listen(user_id)
    price = float(price_msg.text)

    await message.reply_text("🕰 **Account Age**\n\nIs this an old account? (yes/no)")
    is_old_msg = await client.listen(user_id)
    is_old = is_old_msg.text.lower() == "yes"
    
    await message.reply_text("Which country is this number from?\n\nReply with country code (e.g. +1 for USA):")
    country_code_msg = await client.listen(user_id)
    country_code = country_code_msg.text.strip()
    temp = None
    for country_name, code in country_codes.items():
        if country_code == code:
            temp = country_name
            break
    if not temp:
        await message.reply_text("❌ Country code not recognized. Please try again.")
        return
    
    year = None
    if is_old:
        await message.reply_text("📅 **Account Creation Year**\n\nEnter full year (e.g. 2018):")
        year_msg = await client.listen(user_id)
        year = int(year_msg.text)

    await add_otp_data(number, session, price, is_old, year, password, temp)
    await message.reply_text(f"✅ **Number Added!**\n\n📱 `{number}`\n💰 ${price}\n{'📅 '+str(year) if is_old else '🌱 New Account'}", parse_mode=ParseMode.MARKDOWN)

@Client.on_message(filters.command("delete_number") & filters.user(SUDO_USERS))
async def delete_number(client: Client, message: Message):
    await message.reply_text("🗑 **Delete Number**\n\nSend full number to remove:")
    number = await client.listen(message.chat.id)
    
    result = await delete_otp_data(number.text)
    if result.deleted_count > 0:
        await message.reply_text(f"✅ Successfully deleted:\n`{number.text}`", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply_text("⚠️ **Number Not Found!**\nCheck database and try again")

@Client.on_message(filters.command("addbalance") & filters.user(OWNER_ID))
async def add_balance(client: Client, message: Message):
    args = message.text.split()
    if len(args) == 3:
        try:
            user_id = int(args[1])
            amount = float(args[2])
            user_data = await fetch_user_data(user_id)
            if user_data:
                new_balance = user_data['balance'] + amount
                await update_user_data(user_id, {"balance": new_balance})
                await message.reply_text(f"💰 **Balance Updated**\n\nUser: `{user_id}`\nAdded: `${amount}`\nNew Balance: `${new_balance}`", parse_mode=ParseMode.MARKDOWN)
                await client.send_message(user_id, f"💸 **Wallet Credited!**\n\nAmount: `${amount}`\nNew Balance: `${new_balance}`", parse_mode=ParseMode.MARKDOWN)
            else:
                await message.reply_text("⚠️ **User Not Found!**\nCheck ID and try again")
        except ValueError:
            await message.reply_text("❌ **Invalid Input!**\nUse numbers only")
    else:
        await message.reply_text("📝 **Usage:**\n`/addbalance [user_id] [amount]`")

@Client.on_message(filters.command("removebalance") & filters.user(OWNER_ID))
async def remove_balance(client: Client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = float(amount)
        
        user_data = await fetch_user_data(user_id)
        if user_data:
            new_balance = max(0, user_data['balance'] - amount)
            await update_user_data(user_id, {"balance": new_balance})
            await message.reply_text(f"💰 **Balance Updated**\n\nUser: `{user_id}`\nDeducted: `${amount}`\nNew Balance: `${new_balance}`", parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply_text("⚠️ **User Not Found!**\nCheck ID and try again")
    except ValueError:
        await message.reply_text("❌ **Invalid Format!**\nUse: `/removebalance [user_id] [amount]`")

@Client.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def show_stats(client: Client, message: Message):
    total_users, total_numbers, total_balance = await get_total_stats()
    stats_text = f"📊 **System Statistics**\n\n"
    stats_text += f"👥 Users: `{total_users}`\n"
    stats_text += f"📱 Numbers: `{total_numbers}`\n"
    stats_text += f"💰 Total Balance Of All Users: `${total_balance:.2f}`"
    await message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

from pyrogram import Client, filters
from pyrogram.types import Message
from config import SUDO_USERS
from OTP.database.database import fetch_all_user_ids

@Client.on_message(filters.command("broadcast") & filters.user(SUDO_USERS) & filters.reply)
async def broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ **Reply to a message to broadcast it!**")
        return

    user_ids = await fetch_all_user_ids()
    broadcast_message = message.reply_to_message

    success_count = 0
    failure_count = 0

    for user_id in user_ids:
        try:
            await broadcast_message.forward(chat_id=user_id)
            success_count += 1
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
            failure_count += 1

    await message.reply_text(f"✅ **Broadcast completed!**\n\n**Successful:** {success_count}\n**Failed:** {failure_count}")
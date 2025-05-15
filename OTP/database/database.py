from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client['Otp_Bot']
otp_db = db['otp_db']
users_db = db['users_db']
locked_numbers = set()

async def add_otp_data(number, session, price, is_old=False, year=None, twofa=None, country=None):
    data = {"number": number, "session": session, "price": price, "is_old": is_old, "twofa": twofa, "country": country}
    if is_old and year:
        data["year"] = year
    return await otp_db.insert_one(data)

async def fetch_otp_data(is_old=False, year=None):
    query = {"is_old": is_old}
    if year:
        query["year"] = year
    return await otp_db.find(query).to_list(length=None)

async def fetch_otp_by_all_country():
    return await otp_db.find({"country": {"$exists": True}}).to_list(length=None)

async def fetch_otp_number(number):
    query = {"number": number}
    return await otp_db.find_one(query)

async def count_otp_data(is_old=False, year=None):
    query = {"is_old": is_old}
    if year:
        query["year"] = year
    return await otp_db.count_documents(query)

async def get_unique_years():
    return await otp_db.distinct("year", {"is_old": True})

async def add_user_data(user_id, number_bought=0, balance=0, transaction_count=0, referrer=None):
    data = {
        "user_id": user_id,
        "number_bought": number_bought,
        "balance": balance,
        "transaction_count": transaction_count
    }
    if referrer is not None:
        data["referrer"] = referrer
    return await users_db.insert_one(data)

async def fetch_user_data(user_id):
    return await users_db.find_one({"user_id": user_id})

async def update_user_data(user_id, update_data):
    return await users_db.update_one({"user_id": user_id}, {"$set": update_data})

async def delete_otp_data(number):
    return await otp_db.delete_one({"number": number})

def lock_number(number):
    locked_numbers.add(number)

def unlock_number(number):
    locked_numbers.discard(number)

def is_number_locked(number):
    return number in locked_numbers

async def get_total_stats():
    total_users = await users_db.count_documents({})
    total_numbers = await otp_db.count_documents({})
    total_balance = sum([user['balance'] async for user in users_db.find()])
    return total_users, total_numbers, total_balance

async def count_referrals(referrer_id):
    return await users_db.count_documents({"referrer": referrer_id})

async def fetch_all_user_ids():
    users = await users_db.find({}, {"user_id": 1}).to_list(length=None)
    return [user["user_id"] for user in users]
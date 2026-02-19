from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI)
db = client['cybershield']

users_collection = db['users']
logs_collection = db['logs']
licenses_collection = db['licenses']
blocked_ips_collection = db['blocked_ips']

def get_user(username):
    return users_collection.find_one({'username': username})

def create_user(username, password_hash, role='user', license_key=None):
    user_data = {
        'username': username,
        'password_hash': password_hash,
        'role': role,
        'license_active': True,
        'license_key': license_key,
        'created_at': datetime.utcnow()
    }
    return users_collection.insert_one(user_data)

def verify_license(license_key):
    license_doc = licenses_collection.find_one({'license_key': license_key})
    if license_doc and license_doc.get('active') and license_doc.get('assigned_to') is None:
        return True
    return False

def assign_license(license_key, username):
    licenses_collection.update_one(
        {'license_key': license_key},
        {'$set': {'assigned_to': username}}
    )

def get_license_info(username):
    user = get_user(username)
    if user and user.get('license_key'):
        return licenses_collection.find_one({'license_key': user['license_key']})
    return None

def get_logs(limit=100):
    return list(logs_collection.find().sort('timestamp', -1).limit(limit))

def get_logs_count():
    return logs_collection.count_documents({})

def get_blocked_attacks_count():
    return logs_collection.count_documents({'action': 'blocked'})

def get_active_threats_count():
    return logs_collection.count_documents({'label': 'attack'})

def get_unique_attackers_count():
    return len(logs_collection.distinct('src_ip'))

def get_attack_distribution():
    pipeline = [
        {'$group': {'_id': '$label', 'count': {'$sum': 1}}}
    ]
    return list(logs_collection.aggregate(pipeline))

def get_attack_timeline():
    pipeline = [
        {'$group': {
            '_id': {
                '$dateToString': {'format': '%Y-%m-%d %H:00', 'date': '$timestamp'}
            },
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}},
        {'$limit': 24}
    ]
    return list(logs_collection.aggregate(pipeline))

def get_blocked_ips():
    return list(blocked_ips_collection.find().sort('blocked_at', -1))

def unblock_ip(ip):
    blocked_ips_collection.delete_one({'ip': ip})

def get_all_users():
    return list(users_collection.find())

def delete_user(username):
    users_collection.delete_one({'username': username})

def clear_logs():
    logs_collection.delete_many({})

def update_password(username, new_password_hash):
    users_collection.update_one(
        {'username': username},
        {'$set': {'password_hash': new_password_hash}}
    )
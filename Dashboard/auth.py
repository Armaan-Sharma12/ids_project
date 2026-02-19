import bcrypt
import db

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

def authenticate(username, password):
    user = db.get_user(username)
    if user and verify_password(password, user['password_hash']):
        return True, user['role']
    return False, None

def register_user(username, password, license_key):
    if db.get_user(username):
        return False, "Username already exists"
    
    if not db.verify_license(license_key):
        return False, "Invalid or already used license key"
    
    password_hash = hash_password(password)
    db.create_user(username, password_hash, role='user', license_key=license_key)
    db.assign_license(license_key, username)
    
    return True, "Account created successfully"
import db
import secrets
import string
from datetime import datetime, timedelta

def generate_license_key():
    prefix = "CS"
    year = datetime.utcnow().year
    
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    return f"{prefix}-{year}-{random_part}"

def create_license(days_valid=365):
    
    license_key = generate_license_key()
    
    expiry = datetime.utcnow() + timedelta(days=days_valid)
    
    db.licenses_collection.insert_one({
        "license_key": license_key,
        "active": True,
        "assigned_to": None,
        "created_at": datetime.utcnow(),
        "expiry": expiry
    })
    
    print("\n✅ License created successfully")
    print("License Key:", license_key)
    print("Expiry:", expiry)

if __name__ == "__main__":
    
    create_license()

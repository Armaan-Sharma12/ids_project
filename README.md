# CyberShield AI Defense Dashboard

Enterprise-grade cybersecurity monitoring dashboard built with Streamlit and MongoDB Atlas.

## Features

- **User Authentication**: Secure login/signup with license key validation
- **Real-time Monitoring**: Live security event tracking and visualization
- **Advanced Analytics**: Comprehensive threat analysis and reporting
- **IP Management**: View and manage blocked IP addresses
- **Admin Panel**: Full system administration capabilities
- **Dark Theme UI**: Professional cybersecurity SaaS interface

## Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Valid license keys in MongoDB

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure MongoDB connection:

Edit `db.py` and replace the MongoDB URI:
```python
MONGO_URI = "your_mongodb_atlas_connection_string"
```

Or set environment variable:
```bash
export MONGO_URI="your_mongodb_atlas_connection_string"
```

## MongoDB Setup

Create the following collections in your MongoDB Atlas database named `cybershield`:

### users
```json
{
  "username": "string",
  "password_hash": "bytes",
  "role": "admin|user",
  "license_active": true,
  "license_key": "string",
  "created_at": "datetime"
}
```

### logs
```json
{
  "timestamp": "datetime",
  "src_ip": "string",
  "label": "attack|normal",
  "confidence": 0.95,
  "action": "blocked|allowed",
  "reason": "string"
}
```

### licenses
```json
{
  "license_key": "string",
  "active": true,
  "expiry": "datetime",
  "assigned_to": "string|null"
}
```

### blocked_ips
```json
{
  "ip": "string",
  "reason": "string",
  "blocked_at": "datetime"
}
```

## Creating Initial Data

### Create admin user (Python):
```python
from auth import hash_password
from db import users_collection

admin_password = hash_password("your_admin_password")
users_collection.insert_one({
    "username": "admin",
    "password_hash": admin_password,
    "role": "admin",
    "license_active": True,
    "license_key": "ADMIN-LICENSE-KEY",
    "created_at": datetime.utcnow()
})
```

### Create license keys:
```python
from db import licenses_collection
from datetime import datetime, timedelta

licenses_collection.insert_one({
    "license_key": "CS-2024-XXXX-XXXX",
    "active": True,
    "expiry": datetime.utcnow() + timedelta(days=365),
    "assigned_to": None
})
```

## Running the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## Usage

### Public Pages (Before Login)
- **Home**: Landing page with features
- **Sign In**: Login with credentials
- **Sign Up**: Register with license key

### Dashboard Pages (After Login)
- **Dashboard Overview**: Real-time metrics and recent events
- **Analytics**: Advanced threat analysis and charts
- **Logs**: Comprehensive event log viewer
- **Alerts**: High-confidence threat alerts
- **Blocked IPs**: Manage blocked IP addresses
- **Firewall Control**: Monitor system status
- **License**: View license information
- **Profile**: Manage account settings

### Admin Only
- **Admin Panel**: User management, system stats, data management

## Project Structure

```
Dashboard/
│
├── dashboard.py          # Main application entry point
├── auth.py              # Authentication logic
├── db.py                # Database operations
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
│
├── assets/
│   └── style.css        # Dark theme styling
│
├── components/
│   ├── navbar.py        # Top navigation bar
│   ├── sidebar.py       # Side navigation menu
│   ├── charts.py        # Chart rendering functions
│   └── tables.py        # Table rendering functions
│
└── pages/
    ├── home.py              # Landing page
    ├── signin.py            # Login page
    ├── signup.py            # Registration page
    ├── dashboard_home.py    # Main dashboard
    ├── analytics.py         # Analytics page
    ├── logs.py              # Logs viewer
    ├── alerts.py            # Alerts page
    ├── blocked_ips.py       # IP management
    ├── firewall_control.py  # System control
    ├── license.py           # License info
    ├── profile.py           # User profile
    └── admin.py             # Admin panel
```

## Integration with Detection Engine

This dashboard is designed to work with a separate Python detection engine that:

1. Monitors network traffic
2. Classifies threats using AI models
3. Logs events to MongoDB Atlas
4. Optionally blocks malicious IPs

The dashboard reads from MongoDB to display:
- Security events
- Blocked IPs
- Threat statistics
- Real-time alerts

## Security Notes

- All passwords are hashed using bcrypt
- Session management via Streamlit session_state
- License validation on signup
- Role-based access control (admin/user)
- MongoDB connection should use authentication

## Customization

### Change Theme Colors
Edit `assets/style.css` and modify CSS variables:
```css
:root {
    --bg-primary: #0a0e27;
    --accent-blue: #3b82f6;
    /* ... */
}
```

### Add New Pages
1. Create page in `pages/` directory
2. Add to `page_map` in `dashboard.py`
3. Add navigation button in `sidebar.py`

## Troubleshooting

### MongoDB Connection Issues
- Verify connection string in `db.py`
- Check IP whitelist in MongoDB Atlas
- Ensure database user has proper permissions

### Authentication Issues
- Verify bcrypt is installed correctly
- Check user exists in database
- Ensure password_hash is stored as bytes

### Module Import Errors
- Ensure all `__init__.py` files exist
- Run from Dashboard directory
- Check Python path

## License

This is a monitoring dashboard only. Actual network packet capture and blocking requires additional security tools and proper authorization.

## Support

For issues or questions, contact your system administrator.
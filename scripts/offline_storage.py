import sqlite3
import os
from supabase import create_client

# Initialize database
conn = sqlite3.connect("offline_logs.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS alerts (timestamp TEXT, message TEXT, status TEXT)''')
conn.commit()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_alert(timestamp, message, status):
    """Stores alert locally if offline."""
    c.execute("INSERT INTO alerts VALUES (?, ?, ?)", (timestamp, message, status))
    conn.commit()

def sync_with_supabase():
    """Uploads offline data to Supabase when online."""
    c.execute("SELECT * FROM alerts")
    rows = c.fetchall()
    
    for row in rows:
        supabase.table("alerts").insert({
            "timestamp": row[0],
            "message": row[1],
            "status": row[2]
        }).execute()
    
    c.execute("DELETE FROM alerts")  # Clear offline logs
    conn.commit()

# Run sync on startup
sync_with_supabase()

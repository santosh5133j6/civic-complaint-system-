"""
Direct Supabase connection test - bypasses DNS issues
"""
import hashlib
import requests
import json

# Direct credentials (from your .env)
SUPABASE_URL = "https://rzivsjvkamufosxchkeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6aXZzanZrYW11Zm9zeGNia2VxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0MTU5MDAsImV4cCI6MjA4NDk5MTkwMH0.J7TV44Q9GilIU_kFYtdVudnIlcjmgTU-iZcSd4LoiJo"

def test_connection():
    """Test direct HTTP connection to Supabase"""
    print("Testing direct connection to Supabase...")
    print(f"URL: {SUPABASE_URL}")
    print("-" * 60)
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            timeout=10
        )
        print(f"✅ Connection successful! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test 2: Query admins table
    try:
        print("\nQuerying admins table...")
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admins",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            print(f"✅ Found {len(admins)} admin(s):")
            for admin in admins:
                print(f"  - Username: {admin['username']}")
                print(f"    Email: {admin['email']}")
                print(f"    Department: {admin['department']}")
                print(f"    Password hash: {admin['password_hash'][:20]}...")
        else:
            print(f"❌ Query failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False
    
    # Test 3: Verify password hash
    print("\n" + "=" * 60)
    print("Password verification test:")
    test_password = "123"
    expected_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"Password '123' should hash to:")
    print(f"  {expected_hash}")
    
    if admins:
        actual_hash = admins[0]['password_hash']
        print(f"Database has:")
        print(f"  {actual_hash}")
        if expected_hash == actual_hash:
            print("✅ Password hash MATCHES!")
        else:
            print("❌ Password hash MISMATCH!")
            print("\nFixing password hash...")
            fix_password_hash(expected_hash)
    
    return True

def fix_password_hash(correct_hash):
    """Update the password hash in database"""
    try:
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admins?username=eq.admin",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            json={"password_hash": correct_hash},
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            print("✅ Password hash updated successfully!")
        else:
            print(f"❌ Update failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Update error: {e}")

if __name__ == "__main__":
    test_connection()

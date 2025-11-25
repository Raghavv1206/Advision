# backend/simple_pg_test.py

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("Direct PostgreSQL 18 Connection Test")
print("=" * 70)

try:
    import psycopg2
    
    # Get credentials
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    
    print(f"\nAttempting connection to:")
    print(f"  Host: {db_host}:{db_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print(f"  Password: {'*' * len(db_password) if db_password else 'EMPTY'}")
    
    if not all([db_name, db_user, db_password]):
        print("\n❌ Missing credentials in .env file!")
        print("\nAdd these to your .env file:")
        print("POSTGRES_DB=advision_db")
        print("POSTGRES_USER=advision_user")
        print("POSTGRES_PASSWORD=your_password_here")
        print("POSTGRES_HOST=localhost")
        print("POSTGRES_PORT=5432")
        exit(1)
    
    # Try to connect
    print("\n🔌 Connecting...")
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        connect_timeout=5
    )
    
    print("✅ Connected successfully!")
    
    # Test query
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()[0]
    
    print(f"\n📦 PostgreSQL Version:")
    print(f"   {version}")
    
    # Check database
    cursor.execute('SELECT current_database();')
    current_db = cursor.fetchone()[0]
    print(f"\n✅ Connected to database: {current_db}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ PostgreSQL is working! The issue is in Django settings.")
    print("=" * 70)
    
except ImportError:
    print("\n❌ psycopg2 not installed!")
    print("Run: pip install psycopg2-binary")
    
except psycopg2.OperationalError as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Is PostgreSQL 18 running?")
    print("   Check: services.msc (Windows)")
    print("2. Did you create the database?")
    print("   Run: psql -U postgres")
    print("   Then: CREATE DATABASE advision_db;")
    print("3. Check your password in .env")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
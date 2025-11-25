# backend/test_postgres_connection.py - PostgreSQL 18

import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("=" * 70)
    print("Testing PostgreSQL 18 Connection")
    print("=" * 70)
    
    try:
        import psycopg2
        
        db_name = os.getenv('POSTGRES_DB')
        db_user = os.getenv('POSTGRES_USER')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = os.getenv('POSTGRES_HOST')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        
        print(f"\nConnecting to PostgreSQL 18:")
        print(f"  Database: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Host: {db_host}:{db_port}")
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        print("\n✅ Connection successful!")
        
        cursor = conn.cursor()
        
        # Get PostgreSQL version
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        # Check if it's PostgreSQL 18
        if 'PostgreSQL 18' in version:
            print("\n✅ PostgreSQL 18 Confirmed!")
        else:
            print(f"\n⚠️  Version detected: {version.split(',')[0]}")
        
        # Test a simple query
        cursor.execute('SELECT current_database(), current_user;')
        db, user = cursor.fetchone()
        print(f"\n📦 Connected to database: {db}")
        print(f"👤 Connected as user: {user}")
        
        # Check encoding
        cursor.execute("SHOW server_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"📝 Database encoding: {encoding}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ PostgreSQL 18 is ready for Django!")
        print("=" * 70)
        return True
        
    except ImportError:
        print("\n❌ psycopg2 not installed!")
        print("Install it: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("\nTroubleshooting for PostgreSQL 18:")
        print("1. Check if PostgreSQL 18 service is running")
        print("   Windows: services.msc → PostgreSQL 18 Server")
        print("2. Verify credentials in .env file")
        print("3. Ensure database 'advision_db' exists")
        print("4. Check pg_hba.conf for connection permissions")
        print("5. Verify firewall allows port 5432")
        return False

if __name__ == '__main__':
    test_connection()# backend/test_postgres_connection.py - PostgreSQL 18

import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("=" * 70)
    print("Testing PostgreSQL 18 Connection")
    print("=" * 70)
    
    try:
        import psycopg2
        
        db_name = os.getenv('POSTGRES_DB')
        db_user = os.getenv('POSTGRES_USER')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = os.getenv('POSTGRES_HOST')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        
        print(f"\nConnecting to PostgreSQL 18:")
        print(f"  Database: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Host: {db_host}:{db_port}")
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        print("\n✅ Connection successful!")
        
        cursor = conn.cursor()
        
        # Get PostgreSQL version
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        # Check if it's PostgreSQL 18
        if 'PostgreSQL 18' in version:
            print("\n✅ PostgreSQL 18 Confirmed!")
        else:
            print(f"\n⚠️  Version detected: {version.split(',')[0]}")
        
        # Test a simple query
        cursor.execute('SELECT current_database(), current_user;')
        db, user = cursor.fetchone()
        print(f"\n📦 Connected to database: {db}")
        print(f"👤 Connected as user: {user}")
        
        # Check encoding
        cursor.execute("SHOW server_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"📝 Database encoding: {encoding}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ PostgreSQL 18 is ready for Django!")
        print("=" * 70)
        return True
        
    except ImportError:
        print("\n❌ psycopg2 not installed!")
        print("Install it: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("\nTroubleshooting for PostgreSQL 18:")
        print("1. Check if PostgreSQL 18 service is running")
        print("   Windows: services.msc → PostgreSQL 18 Server")
        print("2. Verify credentials in .env file")
        print("3. Ensure database 'advision_db' exists")
        print("4. Check pg_hba.conf for connection permissions")
        print("5. Verify firewall allows port 5432")
        return False

if __name__ == '__main__':
    test_connection()
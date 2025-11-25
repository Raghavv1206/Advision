# backend/check_current_db.py

import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("Current Database Configuration Check")
print("=" * 70)

print("\n1. Environment Variables:")
print(f"   POSTGRES_DB: {os.getenv('POSTGRES_DB', 'NOT SET')}")
print(f"   POSTGRES_USER: {os.getenv('POSTGRES_USER', 'NOT SET')}")
print(f"   POSTGRES_PASSWORD: {'***' if os.getenv('POSTGRES_PASSWORD') else 'NOT SET'}")
print(f"   POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'NOT SET')}")
print(f"   POSTGRES_PORT: {os.getenv('POSTGRES_PORT', 'NOT SET')}")
print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings

print("\n2. Django Database Configuration:")
db_config = settings.DATABASES['default']
print(f"   ENGINE: {db_config.get('ENGINE')}")
print(f"   NAME: {db_config.get('NAME')}")
print(f"   USER: {db_config.get('USER', 'N/A')}")
print(f"   HOST: {db_config.get('HOST', 'N/A')}")
print(f"   PORT: {db_config.get('PORT', 'N/A')}")

if 'sqlite' in db_config.get('ENGINE', '').lower():
    print("\n❌ ERROR: Django is still configured for SQLite!")
    print("   You need to update settings.py to use PostgreSQL")
elif 'postgresql' in db_config.get('ENGINE', '').lower():
    print("\n✅ Django is configured for PostgreSQL")
else:
    print(f"\n⚠️  Unknown database engine: {db_config.get('ENGINE')}")

print("\n" + "=" * 70)
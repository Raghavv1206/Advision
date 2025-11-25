# backend/migrate_to_postgres.py

"""
Script to migrate data from SQLite to PostgreSQL
IMPORTANT: Run this BEFORE fully switching to PostgreSQL
"""

import os
import sys
import django

# Use SQLite settings temporarily for export
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_sqlite')
django.setup()

from django.core.management import call_command

def migrate_data():
    print("=" * 60)
    print("MIGRATION: SQLite → PostgreSQL")
    print("=" * 60)
    
    # Check if SQLite database exists
    sqlite_path = 'db.sqlite3'
    if not os.path.exists(sqlite_path):
        print(f"\n❌ SQLite database not found at: {sqlite_path}")
        print("   If you don't have existing data, skip this step.")
        print("   Just run: python manage.py migrate")
        return False
    
    # Step 1: Export data from SQLite
    print("\n📦 Step 1: Exporting data from SQLite...")
    print("   This may take a few minutes for large databases...")
    
    try:
        with open('data_backup.json', 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--exclude=contenttypes',
                '--exclude=auth.permission',
                '--exclude=sessions.session',
                '--indent=2',
                stdout=f
            )
        
        print("✅ Data exported to data_backup.json")
        
        # Get file size
        file_size = os.path.getsize('data_backup.json') / 1024  # KB
        print(f"   File size: {file_size:.2f} KB")
        
    except Exception as e:
        print(f"\n❌ Export failed: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ EXPORT COMPLETE!")
    print("=" * 60)
    
    print("\n📋 NEXT STEPS:")
    print("\n1. Ensure PostgreSQL is running:")
    print("   • Windows: Check Services or run 'docker-compose up -d postgres'")
    print("   • Mac/Linux: 'brew services start postgresql' or 'sudo service postgresql start'")
    
    print("\n2. Update your .env file with PostgreSQL credentials:")
    print("   POSTGRES_DB=advision_db")
    print("   POSTGRES_USER=advision_user")
    print("   POSTGRES_PASSWORD=your_secure_password")
    print("   POSTGRES_HOST=localhost")
    print("   POSTGRES_PORT=5432")
    
    print("\n3. Your settings.py should already be configured for PostgreSQL")
    
    print("\n4. Run migrations:")
    print("   python manage.py migrate")
    
    print("\n5. Load the backup data:")
    print("   python manage.py loaddata data_backup.json")
    
    print("\n6. Create a superuser:")
    print("   python manage.py createsuperuser")
    
    print("\n7. Verify the migration:")
    print("   python verify_postgres.py")
    
    print("\n" + "=" * 60)
    
    return True

if __name__ == '__main__':
    success = migrate_data()
    sys.exit(0 if success else 1)
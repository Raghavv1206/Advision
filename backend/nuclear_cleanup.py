# backend/nuclear_cleanup.py - Complete database wipe and fresh start
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import *
from django.db import connection

User = get_user_model()

print("=" * 70)
print("💣 NUCLEAR DATABASE CLEANUP - DELETING EVERYTHING")
print("=" * 70)

# Step 1: Delete ALL users (including superusers)
print("\n🗑️  Step 1: Deleting all users...")
user_count = User.objects.all().count()
User.objects.all().delete()
print(f"✅ Deleted {user_count} users")

# Step 2: Delete all core models
print("\n🗑️  Step 2: Deleting all campaign data...")
models_to_delete = [
    ('Predictions', Prediction),
    ('PredictiveModels', PredictiveModel),
    ('ABTestVariations', ABTestVariation),
    ('ABTests', ABTest),
    ('ReportSchedules', ReportSchedule),
    ('GeneratedReports', GeneratedReport),
    ('UserAPIKeys', UserAPIKey),
    ('SyncedCampaigns', SyncedCampaign),
    ('AdPlatformConnections', AdPlatformConnection),
    ('Comments', Comment),
    ('CampaignAnalyticsSummaries', CampaignAnalyticsSummary),
    ('DailyAnalytics', DailyAnalytics),
    ('ImageAssets', ImageAsset),
    ('AdContent', AdContent),
    ('Campaigns', Campaign),
]

for model_name, model in models_to_delete:
    count = model.objects.all().count()
    if count > 0:
        model.objects.all().delete()
        print(f"✅ Deleted {count} {model_name}")

# Step 3: Reset sequences (for auto-increment IDs)
print("\n🔄 Step 3: Resetting database sequences...")
with connection.cursor() as cursor:
    # This ensures clean slate for all tables
    cursor.execute("SELECT setval(pg_get_serial_sequence('core_user', 'id'), 1, false);")
print("✅ Sequences reset")

# Step 4: Verify everything is gone
print("\n🔍 Step 4: Verifying cleanup...")
remaining_users = User.objects.count()
remaining_campaigns = Campaign.objects.count()
remaining_ads = AdContent.objects.count()
remaining_images = ImageAsset.objects.count()

print(f"   Users: {remaining_users}")
print(f"   Campaigns: {remaining_campaigns}")
print(f"   Ads: {remaining_ads}")
print(f"   Images: {remaining_images}")

if remaining_users == 0 and remaining_campaigns == 0 and remaining_ads == 0 and remaining_images == 0:
    print("\n✅ DATABASE COMPLETELY CLEAN!")
else:
    print("\n⚠️  Warning: Some data might remain")

print("\n" + "=" * 70)
print("✅ CLEANUP COMPLETE - Ready for fresh data generation")
print("=" * 70)
print("\nNext steps:")
print("1. Run: python create_demo_data.py")
print("2. Run: python manage.py runserver")
print("3. Login and verify NO warnings appear")
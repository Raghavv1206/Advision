# backend/cleanup_and_setup.py - Complete cleanup and fresh setup
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import *

User = get_user_model()

print("=" * 70)
print("🧹 STEP 1: COMPLETE DATABASE CLEANUP")
print("=" * 70)

# Delete all demo users (this cascades to all related data)
demo_emails = ['demo@advision.com', 'admin@advision.com', 'test@advision.com']
deleted_users = User.objects.filter(email__in=demo_emails).delete()
print(f"✅ Deleted demo users: {deleted_users}")

# Double-check: Delete any orphaned data
print("\n🔍 Cleaning up any orphaned data...")
AdContent.objects.all().delete()
ImageAsset.objects.all().delete()
Comment.objects.all().delete()
DailyAnalytics.objects.all().delete()
CampaignAnalyticsSummary.objects.all().delete()
ABTestVariation.objects.all().delete()
ABTest.objects.all().delete()
Prediction.objects.all().delete()
PredictiveModel.objects.all().delete()
ReportSchedule.objects.all().delete()
Campaign.objects.all().delete()
UserAPIKey.objects.all().delete()

print("✅ All old data deleted!")

print("\n" + "=" * 70)
print("🚀 STEP 2: GENERATING FRESH DEMO DATA")
print("=" * 70)

# Now run the demo data creation with UTF-8 encoding
with open('create_demo_data.py', 'r', encoding='utf-8') as f:
    exec(f.read())
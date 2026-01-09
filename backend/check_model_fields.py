# backend/check_model_fields.py - Diagnose the timezone issue
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import AdContent, ImageAsset, Comment, Campaign
from django.utils import timezone
import inspect

print("=" * 70)
print("🔍 DIAGNOSING DATETIME FIELD CONFIGURATION")
print("=" * 70)

models_to_check = [
    ('AdContent', AdContent),
    ('ImageAsset', ImageAsset),
    ('Comment', Comment),
    ('Campaign', Campaign),
]

for model_name, model in models_to_check:
    print(f"\n📦 {model_name}:")
    
    # Check if created_at field exists
    if hasattr(model, '_meta'):
        try:
            field = model._meta.get_field('created_at')
            print(f"   Field type: {field.__class__.__name__}")
            print(f"   auto_now_add: {field.auto_now_add}")
            print(f"   auto_now: {field.auto_now}")
            print(f"   default: {field.default}")
            print(f"   null: {field.null}")
            print(f"   blank: {field.blank}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("🔍 CHECKING EXISTING DATA")
print("=" * 70)

# Check if any data exists
ad_count = AdContent.objects.count()
img_count = ImageAsset.objects.count()

print(f"\n📊 AdContent records: {ad_count}")
print(f"📊 ImageAsset records: {img_count}")

if ad_count > 0:
    recent_ad = AdContent.objects.order_by('-id').first()
    print(f"\n🔍 Most recent AdContent:")
    print(f"   ID: {recent_ad.id}")
    print(f"   created_at: {recent_ad.created_at}")
    print(f"   Is naive? {timezone.is_naive(recent_ad.created_at)}")
    print(f"   Timezone: {recent_ad.created_at.tzinfo if recent_ad.created_at else 'None'}")

if img_count > 0:
    recent_img = ImageAsset.objects.order_by('-id').first()
    print(f"\n🔍 Most recent ImageAsset:")
    print(f"   ID: {recent_img.id}")
    print(f"   created_at: {recent_img.created_at}")
    print(f"   Is naive? {timezone.is_naive(recent_img.created_at)}")
    print(f"   Timezone: {recent_img.created_at.tzinfo if recent_img.created_at else 'None'}")

print("\n" + "=" * 70)
print("💡 RECOMMENDATIONS")
print("=" * 70)

print("""
If auto_now_add is False or default is set to something other than 
django.utils.timezone.now, you need to update your models.py:

CORRECT:
    created_at = models.DateTimeField(auto_now_add=True)
    
INCORRECT:
    created_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=now)  # if 'now' is from timezone_utils
""")
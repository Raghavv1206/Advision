# backend/fix_existing_data.py - Convert all naive datetimes to timezone-aware
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.utils import timezone
from core.models import AdContent, ImageAsset, Comment, Campaign, User
from datetime import datetime

print("=" * 70)
print("🔧 FIXING EXISTING DATA - Converting Naive to Timezone-Aware")
print("=" * 70)

def fix_naive_datetimes(model, field_name):
    """Fix naive datetimes in a model's field"""
    total = model.objects.count()
    fixed = 0
    
    for obj in model.objects.all():
        field_value = getattr(obj, field_name)
        
        if field_value and timezone.is_naive(field_value):
            # Convert naive to aware
            aware_dt = timezone.make_aware(field_value)
            setattr(obj, field_name, aware_dt)
            obj.save(update_fields=[field_name])
            fixed += 1
    
    return total, fixed

# Fix all models with datetime fields
models_to_fix = [
    ('AdContent', AdContent, 'created_at'),
    ('ImageAsset', ImageAsset, 'created_at'),
    ('Comment', Comment, 'created_at'),
    ('Campaign', Campaign, 'created_at'),
    ('User', User, 'date_joined'),
]

print("\n🔍 Scanning and fixing models...\n")

for model_name, model, field in models_to_fix:
    total, fixed = fix_naive_datetimes(model, field)
    if fixed > 0:
        print(f"✅ {model_name}.{field}: Fixed {fixed}/{total} records")
    else:
        print(f"✓  {model_name}.{field}: All {total} records already correct")

print("\n" + "=" * 70)
print("✅ ALL DATA FIXED - Naive datetimes converted to timezone-aware")
print("=" * 70)
print("\nNext steps:")
print("1. Restart server: python manage.py runserver")
print("2. Test dashboard - NO warnings should appear")
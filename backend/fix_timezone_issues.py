# backend/fix_timezone_issues.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.utils import timezone
from core.models import AdContent, ImageAsset, Comment, Campaign

print("=" * 70)
print("Fixing Timezone Issues in Database")
print("=" * 70)

# Fix AdContent
print("\n1. Fixing AdContent timestamps...")
for ad in AdContent.objects.all():
    if ad.created_at and timezone.is_naive(ad.created_at):
        ad.created_at = timezone.make_aware(ad.created_at)
        ad.save(update_fields=['created_at'])
        print(f"   Fixed: {ad.id}")

# Fix ImageAsset
print("\n2. Fixing ImageAsset timestamps...")
for img in ImageAsset.objects.all():
    if img.created_at and timezone.is_naive(img.created_at):
        img.created_at = timezone.make_aware(img.created_at)
        img.save(update_fields=['created_at'])
        print(f"   Fixed: {img.id}")

# Fix Comment
print("\n3. Fixing Comment timestamps...")
for comment in Comment.objects.all():
    if comment.created_at and timezone.is_naive(comment.created_at):
        comment.created_at = timezone.make_aware(comment.created_at)
        comment.save(update_fields=['created_at'])
        print(f"   Fixed: {comment.id}")

# Fix Campaign
print("\n4. Fixing Campaign timestamps...")
for campaign in Campaign.objects.all():
    if campaign.created_at and timezone.is_naive(campaign.created_at):
        campaign.created_at = timezone.make_aware(campaign.created_at)
        campaign.save(update_fields=['created_at'])
        print(f"   Fixed: {campaign.id}")

print("\n" + "=" * 70)
print("✅ All timezone issues fixed!")
print("=" * 70)
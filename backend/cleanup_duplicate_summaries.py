# backend/cleanup_duplicate_summaries.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Campaign, CampaignAnalyticsSummary

print("=" * 70)
print("Cleaning Up Duplicate Analytics Summaries")
print("=" * 70)

# Find campaigns without summaries
campaigns_without_summary = []
for campaign in Campaign.objects.all():
    try:
        summary = campaign.analytics_summary
    except CampaignAnalyticsSummary.DoesNotExist:
        campaigns_without_summary.append(campaign)

print(f"\nCampaigns without summary: {len(campaigns_without_summary)}")

# Create missing summaries
for campaign in campaigns_without_summary:
    summary, created = CampaignAnalyticsSummary.objects.get_or_create(campaign=campaign)
    if created:
        summary.update_metrics()
        print(f"✅ Created summary for: {campaign.title}")

# Check for campaigns with multiple summaries (shouldn't happen but just in case)
from django.db.models import Count
duplicates = Campaign.objects.annotate(
    summary_count=Count('analytics_summary')
).filter(summary_count__gt=1)

if duplicates.exists():
    print(f"\n⚠️  Found {duplicates.count()} campaigns with duplicate summaries")
    for campaign in duplicates:
        summaries = CampaignAnalyticsSummary.objects.filter(campaign=campaign)
        # Keep the first one, delete the rest
        summaries_to_delete = summaries[1:]
        for summary in summaries_to_delete:
            summary.delete()
            print(f"   Deleted duplicate for: {campaign.title}")

print("\n" + "=" * 70)
print("✅ Cleanup complete!")
print("=" * 70)
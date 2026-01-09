# backend/core/management/commands/update_analytics_summaries.py
from django.core.management.base import BaseCommand
from core.models import Campaign, CampaignAnalyticsSummary

class Command(BaseCommand):
    help = 'Update analytics summaries for all campaigns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update all summaries even if they exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        
        campaigns = Campaign.objects.all()
        total = campaigns.count()
        updated = 0
        created = 0
        
        self.stdout.write(f"Processing {total} campaigns...")
        
        for campaign in campaigns:
            try:
                summary, was_created = CampaignAnalyticsSummary.objects.get_or_create(
                    campaign=campaign
                )
                
                if was_created:
                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created summary for: {campaign.title}")
                    )
                
                if was_created or force or summary.performance_score == 0:
                    summary.update_metrics()
                    summary.save()
                    updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Updated {campaign.title}: Score = {summary.performance_score}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⏭️  Skipped {campaign.title}: Score = {summary.performance_score}"
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed {campaign.title}: {e}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Done! Created: {created}, Updated: {updated}, Total: {total}"
            )
        )
        
        # Show top 5 campaigns by score
        self.stdout.write("\n📊 Top 5 Campaigns by Performance:")
        top_campaigns = CampaignAnalyticsSummary.objects.select_related(
            'campaign'
        ).order_by('-performance_score')[:5]
        
        for i, summary in enumerate(top_campaigns, 1):
            self.stdout.write(
                f"{i}. {summary.campaign.title}: {summary.performance_score}/100"
            )
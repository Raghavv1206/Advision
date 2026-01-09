# backend/core/tasks.py
from celery import shared_task
from .models import Campaign, CampaignAnalyticsSummary
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_all_campaign_summaries():
    """
    Periodic task to update all campaign analytics summaries.
    Run this daily or hourly depending on your needs.
    """
    campaigns = Campaign.objects.filter(is_active=True)
    updated_count = 0
    
    for campaign in campaigns:
        try:
            summary, created = CampaignAnalyticsSummary.objects.get_or_create(
                campaign=campaign
            )
            summary.update_metrics()
            summary.save()
            updated_count += 1
            
        except Exception as e:
            logger.error(f"Failed to update summary for {campaign.title}: {e}")
    
    logger.info(f"✅ Updated {updated_count} campaign summaries")
    return f"Updated {updated_count} campaigns"

@shared_task
def update_campaign_summary(campaign_id):
    """
    Update a specific campaign's analytics summary.
    Can be called after bulk analytics imports.
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        summary, created = CampaignAnalyticsSummary.objects.get_or_create(
            campaign=campaign
        )
        summary.update_metrics()
        summary.save()
        
        logger.info(f"✅ Updated summary for {campaign.title}: Score = {summary.performance_score}")
        return True
        
    except Campaign.DoesNotExist:
        logger.error(f"Campaign {campaign_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to update campaign {campaign_id}: {e}")
        return False
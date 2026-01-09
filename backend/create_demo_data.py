# create_demo_data.py - Run this to setup complete demo data
# Usage: python create_demo_data.py

# backend/create_demo_data.py - COMPLETE WITH ALL FEATURES - TIMEZONE FIXED
import os
import django
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import (
    Campaign, AdContent, ImageAsset, Comment,
    DailyAnalytics, CampaignAnalyticsSummary,
    UserAPIKey, ABTest, ABTestVariation,
    PredictiveModel, Prediction, ReportSchedule
)
# CRITICAL FIX: Import ALL timezone utilities including datetime_ago
from core.utils.timezone_utils import now, days_ago, datetime_ago, datetime_from_now
from datetime import timedelta

User = get_user_model()

print("🎬 Setting up AdVision Demo Environment with ALL FEATURES...")
print("=" * 70)

# ============================================================================
# 1. CREATE DEMO USERS
# ============================================================================
print("\n👤 Creating demo users...")

demo_users = [
    {'email': 'demo@advision.com', 'password': 'demo123', 'role': 'admin'},
    {'email': 'admin@advision.com', 'password': 'admin123', 'role': 'admin'},
    {'email': 'test@advision.com', 'password': 'test123', 'role': 'editor'},
]

for user_data in demo_users:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={'role': user_data['role']}
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"✅ Created user: {user_data['email']} / {user_data['password']}")
    else:
        print(f"ℹ️  User exists: {user_data['email']}")

demo_user = User.objects.get(email='demo@advision.com')

# ============================================================================
# 2. CREATE MOCK API KEYS
# ============================================================================
print("\n🔑 Creating verified mock API keys...")

api_keys_data = [
    {
        'api_type': 'google_ads',
        'api_name': 'My Google Ads Account',
        'account_id': 'demo-google-ads-123',
        'developer_token': 'demo-dev-token-xxx'
    },
    {
        'api_type': 'facebook_ads',
        'api_name': 'Main Facebook Business',
        'account_id': 'act_demo_456'
    },
    {
        'api_type': 'instagram_ads',
        'api_name': 'Instagram Business Account',
        'account_id': 'ig_demo_789'
    },
    {
        'api_type': 'linkedin_ads',
        'api_name': 'LinkedIn Campaign Manager',
        'account_id': 'li_demo_101'
    }
]

for key_data in api_keys_data:
    api_key, created = UserAPIKey.objects.get_or_create(
        user=demo_user,
        api_type=key_data['api_type'],
        api_name=key_data['api_name'],
        defaults={
            'account_id': key_data['account_id'],
            'developer_token': key_data.get('developer_token', ''),
            'verification_status': 'verified',
            'is_active': True,
            'last_verified': now()
        }
    )
    
    if created:
        api_key.encrypt_key(f'demo_{key_data["api_type"]}_key_12345')
        if key_data['api_type'] in ['facebook_ads', 'instagram_ads', 'linkedin_ads']:
            api_key.encrypt_secret(f'demo_{key_data["api_type"]}_secret_67890')
        api_key.save()
        print(f"✅ Created API key: {key_data['api_name']} (verified)")

# ============================================================================
# 3. CREATE DIVERSE DEMO CAMPAIGNS
# ============================================================================
print("\n📊 Creating demo campaigns with realistic performance data...")

campaigns_data = [
    {
        'title': 'Summer Sale 2024 - Fashion Collection',
        'description': 'Promote summer fashion collection with 30% discount',
        'platform': 'instagram',
        'budget': 5000,
        'days_ago': 45,
        'performance_level': 'high'
    },
    {
        'title': 'New Product Launch - Eco Water Bottles',
        'description': 'Launch revolutionary eco-friendly water bottles',
        'platform': 'facebook',
        'budget': 8000,
        'days_ago': 38,
        'performance_level': 'medium'
    },
    {
        'title': 'Brand Awareness - Millennial Targeting',
        'description': 'Increase brand visibility among millennials 25-35',
        'platform': 'youtube',
        'budget': 10000,
        'days_ago': 30,
        'performance_level': 'high'
    },
    {
        'title': 'Holiday Special - Black Friday Deals',
        'description': 'Black Friday early access deals and promotions',
        'platform': 'tiktok',
        'budget': 6000,
        'days_ago': 25,
        'performance_level': 'low'
    },
    {
        'title': 'LinkedIn B2B Campaign',
        'description': 'Target business professionals for enterprise solutions',
        'platform': 'linkedin',
        'budget': 7500,
        'days_ago': 20,
        'performance_level': 'medium'
    },
    {
        'title': 'Spring Collection Preview',
        'description': 'Early access to new spring collection',
        'platform': 'instagram',
        'budget': 4500,
        'days_ago': 15,
        'performance_level': 'high'
    },
    {
        'title': 'Tech Product Demo Campaign',
        'description': 'Showcase product features and benefits',
        'platform': 'youtube',
        'budget': 9000,
        'days_ago': 10,
        'performance_level': 'medium'
    }
]

today = now().date()
campaigns = []

for camp_data in campaigns_data:
    start_date = days_ago(camp_data['days_ago'])
    end_date = today + timedelta(days=30)
    
    campaign, created = Campaign.objects.get_or_create(
        user=demo_user,
        title=camp_data['title'],
        defaults={
            'description': camp_data['description'],
            'platform': camp_data['platform'],
            'budget': camp_data['budget'],
            'start_date': start_date,
            'end_date': end_date,
            'is_active': True
        }
    )
    
    campaign.performance_level = camp_data['performance_level']
    campaigns.append(campaign)
    
    if created:
        print(f"✅ Created campaign: {camp_data['title']} ({camp_data['performance_level']} performer)")

# ============================================================================
# 4. CREATE VARIED AD CONTENT - NO MANUAL created_at
# ============================================================================
print("\n✍️  Creating diverse ad content...")

ad_content_templates = {
    'instagram': [
        "🌊 Dive into Summer Savings! Get 30% OFF on all beachwear. Limited time! #SummerSale #BeachReady",
        "Summer vibes only! 🏖️ Refresh your wardrobe with our hottest collection. Link in bio! #FashionDeals",
        "☀️ Sun's out, deals are out! Exclusive summer sale - 30% OFF everything. #ShopNow"
    ],
    'facebook': [
        "Introducing the future of hydration 💧 Our eco-bottles keep drinks cold for 24hrs. Pre-order now!",
        "🌱 Sustainable. Stylish. Superior. Meet the water bottle that does it all.",
        "Say goodbye to single-use plastics! Premium stainless steel bottles built to last."
    ],
    'youtube': [
        "Join thousands who trust our brand. Premium quality. Affordable prices. Exceptional service.",
        "Why choose us? Award-winning products, 5-star service, 100,000+ happy customers.",
        "Transform your lifestyle with our innovative solutions. Watch real testimonials today."
    ],
    'tiktok': [
        "🔥 Black Friday came early! Shop now before it's gone. Swipe up! #BlackFriday #Deals",
        "POV: You found the best Black Friday deals 😱 Limited stock! #Shopping #Sales",
        "This Black Friday deal is INSANE! 🤯 Watch till the end. #BestDeals"
    ],
    'linkedin': [
        "Empower your team with enterprise-grade solutions. Join Fortune 500 companies.",
        "ROI that speaks for itself. 40% productivity gains in first quarter. Read case studies.",
        "Professional tools for professional results. Trusted by industry leaders worldwide."
    ]
}

for campaign in campaigns:
    platform = campaign.platform
    templates = ad_content_templates.get(platform, ad_content_templates['instagram'])
    
    num_ads = random.randint(3, 5)
    for i in range(num_ads):
        text = templates[i % len(templates)]
        tone = ['persuasive', 'witty', 'casual', 'formal'][i % 4]
        
        if campaign.performance_level == 'high':
            views = random.randint(15000, 50000)
            clicks = int(views * random.uniform(0.04, 0.08))
        elif campaign.performance_level == 'medium':
            views = random.randint(8000, 25000)
            clicks = int(views * random.uniform(0.025, 0.04))
        else:
            views = random.randint(3000, 12000)
            clicks = int(views * random.uniform(0.01, 0.025))
        
        conversions = int(clicks * random.uniform(0.05, 0.15))
        
        # DON'T set created_at - let Django auto-create it
        ad, created = AdContent.objects.get_or_create(
            campaign=campaign,
            text=text,
            defaults={
                'tone': tone,
                'platform': platform,
                'views': views,
                'clicks': clicks,
                'conversions': conversions
            }
        )
        
        if created:
            print(f"  ✅ Added ad for {campaign.title[:30]}... (CTR: {clicks/views*100:.2f}%)")

# ============================================================================
# 5. GENERATE REALISTIC ANALYTICS (FOR LINEAR REGRESSION)
# ============================================================================
print("\n📈 Generating analytics data for ML models...")

for campaign in campaigns:
    campaign_age = (today - campaign.start_date).days
    days_to_generate = min(45, campaign_age + 1)
    
    platform_multipliers = {
        'instagram': 600, 'facebook': 700, 'youtube': 900,
        'linkedin': 350, 'tiktok': 1200
    }
    
    base_impressions = platform_multipliers.get(campaign.platform, 500)
    
    if campaign.performance_level == 'high':
        base_impressions = int(base_impressions * 1.5)
        base_ctr = 0.045
        conversion_mult = 1.3
    elif campaign.performance_level == 'medium':
        base_ctr = 0.03
        conversion_mult = 1.0
    else:
        base_impressions = int(base_impressions * 0.7)
        base_ctr = 0.018
        conversion_mult = 0.7
    
    daily_budget = float(campaign.budget) / max(days_to_generate, 1)
    
    for day_offset in range(days_to_generate):
        analytics_date = today - timedelta(days=days_to_generate - day_offset - 1)
        
        if analytics_date > today or analytics_date < campaign.start_date:
            continue
        
        # Create predictable trends for linear regression
        if day_offset < days_to_generate * 0.3:
            growth_factor = 0.6 + (day_offset / (days_to_generate * 0.3)) * 0.4
        elif day_offset < days_to_generate * 0.7:
            growth_factor = 1.0 + random.uniform(-0.1, 0.2)
        else:
            if campaign.performance_level == 'high':
                growth_factor = 1.1 + random.uniform(-0.1, 0.1)
            elif campaign.performance_level == 'low':
                growth_factor = 0.8 + random.uniform(-0.15, 0.05)
            else:
                growth_factor = 0.95 + random.uniform(-0.1, 0.1)
        
        day_of_week = analytics_date.weekday()
        if day_of_week in [4, 5]:
            day_multiplier = 1.15
        elif day_of_week in [0, 1]:
            day_multiplier = 1.05
        else:
            day_multiplier = 1.0
        
        randomness = random.uniform(0.85, 1.15)
        
        impressions = int(base_impressions * growth_factor * day_multiplier * randomness)
        ctr_variance = random.uniform(-0.01, 0.01)
        actual_ctr = max(0.01, base_ctr + ctr_variance)
        clicks = int(impressions * actual_ctr)
        
        conversion_rate = random.uniform(0.05, 0.15) * conversion_mult
        conversions = int(clicks * conversion_rate)
        
        spend = round(daily_budget * random.uniform(0.85, 1.15), 2)
        
        DailyAnalytics.objects.update_or_create(
            campaign=campaign,
            date=analytics_date,
            defaults={
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend
            }
        )
    
    summary, _ = CampaignAnalyticsSummary.objects.get_or_create(campaign=campaign)
    summary.update_metrics()
    
    print(f"  ✅ {campaign.title[:35]}...")
    print(f"     {summary.total_impressions:,} impressions | Score: {summary.performance_score}/100")

# ============================================================================
# 6. CREATE PREDICTIVE MODELS (LINEAR REGRESSION)
# ============================================================================
print("\n🤖 Creating predictive ML models...")

trainable_campaigns = [c for c in campaigns if (today - c.start_date).days >= 14]

for campaign in trainable_campaigns[:3]:
    try:
        from core.services.predictive_analytics import PredictiveAnalyticsService
        
        result = PredictiveAnalyticsService.train_performance_model(str(campaign.id))
        
        if result.get('success'):
            print(f"  ✅ Trained model for: {campaign.title[:35]}...")
            print(f"     Accuracy: {result['accuracy']*100:.1f}% | Samples: {result['samples']}")
            
            pred_result = PredictiveAnalyticsService.predict_next_week(str(campaign.id))
            if pred_result.get('success'):
                print(f"     Generated 7-day predictions (confidence: {pred_result['model_accuracy']:.1f}%)")
        else:
            print(f"  ⚠️  {campaign.title[:30]}: {result.get('message', 'Not enough data')}")
    except Exception as e:
        print(f"  ⚠️  Error training model for {campaign.title[:30]}: {str(e)}")

# ============================================================================
# 7. CREATE A/B TESTS - FIXED TIMEZONE
# ============================================================================
print("\n🧪 Creating A/B tests...")

test_campaign = campaigns[0]
ab_test, created = ABTest.objects.get_or_create(
    campaign=test_campaign,
    name='Headline Test - Summer Sale',
    defaults={
        'description': 'Testing two headlines for performance',
        'status': 'running',
        'success_metric': 'ctr',
        'min_sample_size': 1000,
        'start_date': datetime_ago(days=7)  # FIXED: Use datetime_ago instead of now() - timedelta
    }
)

if created:
    variation_a = ABTestVariation.objects.create(
        ab_test=ab_test,
        name='A',
        impressions=8500,
        clicks=340,
        conversions=42,
        spend=250
    )
    
    variation_b = ABTestVariation.objects.create(
        ab_test=ab_test,
        name='B',
        impressions=8500,
        clicks=468,
        conversions=61,
        spend=250
    )
    
    print(f"✅ Created A/B test: {ab_test.name}")
    print(f"   Variation A: {variation_a.ctr}% CTR")
    print(f"   Variation B: {variation_b.ctr}% CTR (WINNER +37.6%)")

# ============================================================================
# 8. CREATE REPORT SCHEDULES - FIXED TIMEZONE
# ============================================================================
print("\n📅 Creating automated report schedules...")

report_schedules = [
    {
        'name': 'Weekly Performance Report',
        'frequency': 'weekly',
        'format': 'email',
        'email_recipients': ['demo@advision.com', 'team@advision.com']
    },
    {
        'name': 'Monthly Executive Summary',
        'frequency': 'monthly',
        'format': 'pdf',
        'email_recipients': ['admin@advision.com']
    }
]

for sched_data in report_schedules:
    schedule, created = ReportSchedule.objects.get_or_create(
        user=demo_user,
        name=sched_data['name'],
        defaults={
            'frequency': sched_data['frequency'],
            'format': sched_data['format'],
            'email_recipients': sched_data['email_recipients'],
            'is_active': True,
            'next_run': datetime_from_now(days=1)  # FIXED: Use datetime_from_now instead of now() + timedelta
        }
    )
    
    if created:
        schedule.include_campaigns.set(campaigns[:3])
        print(f"✅ Created report: {sched_data['name']} ({sched_data['frequency']})")

# ============================================================================
# 9. ADD TEAM COMMENTS - NO MANUAL created_at
# ============================================================================
print("\n💬 Adding team collaboration comments...")

comments_data = [
    ("Summer Sale crushing it! ML predicts 15% growth next week. Scale budget by 25%.", campaigns[0]),
    ("Instagram engagement phenomenal. A/B test shows Variation B wins +37.6%.", campaigns[0]),
    ("Black Friday needs work. CTR below 2%. Running predictive analysis.", campaigns[3]),
    ("B2B campaign stable. Model accuracy 87%. Consider video content.", campaigns[4]),
    ("YouTube high performer. Predicted conversions: 450+ next week.", campaigns[2]),
]

for message, campaign in comments_data:
    # DON'T set created_at manually - let Django auto-create it
    comment, created = Comment.objects.get_or_create(
        campaign=campaign,
        user=demo_user,
        defaults={'message': message}
    )
    if created:
        print(f"  ✅ Added comment to {campaign.title[:40]}...")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("🎉 COMPLETE DEMO SETUP - ALL FEATURES!")
print("=" * 70)

print("\n📋 DEMO CREDENTIALS:")
print("-" * 70)
for user_data in demo_users:
    print(f"Email: {user_data['email']:<30} Password: {user_data['password']}")
print("-" * 70)

print("\n📊 DEMO DATA SUMMARY:")
total_campaigns = Campaign.objects.filter(user=demo_user).count()
total_ads = AdContent.objects.filter(campaign__user=demo_user).count()
total_analytics = DailyAnalytics.objects.filter(campaign__user=demo_user).count()
total_api_keys = UserAPIKey.objects.filter(user=demo_user).count()
total_predictions = Prediction.objects.filter(model__user=demo_user).count()
total_models = PredictiveModel.objects.filter(user=demo_user, is_active=True).count()
total_ab_tests = ABTest.objects.filter(campaign__user=demo_user).count()
total_schedules = ReportSchedule.objects.filter(user=demo_user).count()

print(f"✅ {total_campaigns} Campaigns (varied performance)")
print(f"✅ {total_ads} Ad variations")
print(f"✅ {total_analytics} Days of analytics")
print(f"✅ {total_api_keys} Verified API keys")
print(f"✅ {total_models} Trained ML models")
print(f"✅ {total_predictions} AI predictions")
print(f"✅ {total_ab_tests} Active A/B tests")
print(f"✅ {total_schedules} Report schedules")
print(f"✅ {len(comments_data)} Team comments")

print("\n🤖 MACHINE LEARNING FEATURES:")
print(f"   📊 Predictive Analytics: {total_models} models trained")
print(f"   🎯 Next-week predictions ready for {total_models} campaigns")
print(f"   📈 Linear regression with {total_analytics} data points")
print(f"   🧪 A/B testing with statistical significance")
print(f"   💡 Budget optimization recommendations")

print("\n💡 ALL FEATURES AVAILABLE:")
print("   1. ✅ Dashboard - Real-time metrics")
print("   2. ✅ Campaign Analytics - 45 days history")
print("   3. ✅ Audience Insights - Engagement patterns")
print("   4. ✅ Weekly Reports - AI recommendations")
print("   5. ✅ A/B Testing - Statistical analysis")
print("   6. ✅ API Keys - All verified")
print("   7. ✅ Predictive Analytics - ML models trained")
print("   8. ✅ Budget Optimization - ROAS & ROI")
print("   9. ✅ Report Scheduling - Automated delivery")
print("   10. ✅ Team Collaboration - Comments")

print("\n🎯 TEST SCENARIOS:")
print("   📌 Predictive: '/api/predictive/predict/?campaign_id=<ID>'")
print("   📌 Budget: '/api/predictive/budget/'")
print("   📌 A/B Test: '/api/ab-tests/<ID>/analyze/'")
print("   📌 Train Model: '/api/predictive/train/' (POST)")

print("\n🚀 READY FOR FULL DEMO!")
print("=" * 70)
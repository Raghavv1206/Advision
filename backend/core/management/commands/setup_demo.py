# backend/core/management/commands/setup_demo.py
from django.core.management.base import BaseCommand
import os
import sys

class Command(BaseCommand):
    help = 'Setup complete demo environment with all features'

    def handle(self, *args, **options):
        """Execute the create_demo_data.py script"""
        
        # Get the path to create_demo_data.py (it's in backend root)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        script_path = os.path.join(backend_root, 'create_demo_data.py')
        
        # Check if file exists
        if not os.path.exists(script_path):
            self.stdout.write(self.style.ERROR(f'❌ Script not found at: {script_path}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'📂 Found script at: {script_path}'))
        self.stdout.write(self.style.SUCCESS('🚀 Executing demo setup...\n'))
        
        # Read and execute the script
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Filter out ONLY the Django setup lines, keep all imports
            lines = script_content.split('\n')
            filtered_lines = []
            skip_mode = False
            
            for line in lines:
                stripped = line.strip()
                
                # Skip these specific Django initialization lines
                if "os.environ.setdefault('DJANGO_SETTINGS_MODULE'" in line:
                    continue
                if stripped == 'django.setup()':
                    continue
                    
                filtered_lines.append(line)
            
            filtered_content = '\n'.join(filtered_lines)
            
            # Create execution namespace with all necessary imports
            exec_globals = {
                '__name__': '__main__',
                '__builtins__': __builtins__,
            }
            
            # Execute the script
            exec(filtered_content, exec_globals)
            
            self.stdout.write('\n' + '=' * 70)
            self.stdout.write(self.style.SUCCESS('✅ DEMO SETUP COMPLETED SUCCESSFULLY!'))
            self.stdout.write('=' * 70)
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ Could not find: {script_path}'))
            self.stdout.write(self.style.WARNING('💡 Make sure create_demo_data.py is in the backend root directory'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error executing script: {str(e)}'))
            self.stdout.write('\n💡 TIP: Make sure migrations are up to date:')
            self.stdout.write('   python manage.py makemigrations')
            self.stdout.write('   python manage.py migrate\n')
            import traceback
            traceback.print_exc()

        # ============================================================================
        # 1. CREATE DEMO USERS
        # ============================================================================
        self.stdout.write('\n👤 Creating demo users...')

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
                self.stdout.write(self.style.SUCCESS(f"✅ Created user: {user_data['email']} / {user_data['password']}"))
            else:
                self.stdout.write(f"ℹ️  User exists: {user_data['email']}")

        demo_user = User.objects.get(email='demo@advision.com')

        # ============================================================================
        # 2. CREATE MOCK API KEYS
        # ============================================================================
        self.stdout.write('\n🔑 Creating verified mock API keys...')

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
                if key_data['api_type'] in ['facebook_ads', 'instagram_ads']:
                    api_key.encrypt_secret(f'demo_{key_data["api_type"]}_secret_67890')
                api_key.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Created API key: {key_data['api_name']} (verified)"))

        # ============================================================================
        # 3. CREATE DIVERSE DEMO CAMPAIGNS
        # ============================================================================
        self.stdout.write('\n📊 Creating demo campaigns with realistic performance data...')

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
                self.stdout.write(self.style.SUCCESS(f"✅ Created campaign: {camp_data['title']} ({camp_data['performance_level']} performer)"))

        # ============================================================================
        # 4. CREATE AD CONTENT
        # ============================================================================
        self.stdout.write('\n✍️  Creating diverse ad content...')

        ad_content_templates = {
            'instagram': [
                "🌊 Dive into Summer Savings! Get 30% OFF on all beachwear. Limited time! #SummerSale #BeachReady",
                "Summer vibes only! 🏖️ Refresh your wardrobe with our hottest collection. Link in bio! #FashionDeals",
            ],
            'facebook': [
                "Introducing the future of hydration 💧 Our eco-bottles keep drinks cold for 24hrs. Pre-order now!",
                "🌱 Sustainable. Stylish. Superior. Meet the water bottle that does it all.",
            ],
            'youtube': [
                "Join thousands who trust our brand. Premium quality. Affordable prices. Exceptional service.",
                "Why choose us? Award-winning products, 5-star service, 100,000+ happy customers.",
            ],
            'tiktok': [
                "🔥 Black Friday came early! Shop now before it's gone. Swipe up! #BlackFriday #Deals",
                "POV: You found the best Black Friday deals 😱 Limited stock! #Shopping #Sales",
            ],
        }

        for campaign in campaigns:
            platform = campaign.platform
            templates = ad_content_templates.get(platform, ad_content_templates['instagram'])
            
            for i, text in enumerate(templates):
                tone = ['persuasive', 'witty', 'casual'][i % 3]
                
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
                
                AdContent.objects.get_or_create(
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

        # ============================================================================
        # 5. GENERATE ANALYTICS
        # ============================================================================
        self.stdout.write('\n📈 Generating analytics data...')

        for campaign in campaigns:
            campaign_age = (today - campaign.start_date).days
            days_to_generate = min(45, campaign_age + 1)
            
            platform_multipliers = {
                'instagram': 600, 'facebook': 700, 'youtube': 900, 'tiktok': 1200
            }
            
            base_impressions = platform_multipliers.get(campaign.platform, 500)
            
            if campaign.performance_level == 'high':
                base_impressions = int(base_impressions * 1.5)
                base_ctr = 0.045
            elif campaign.performance_level == 'medium':
                base_ctr = 0.03
            else:
                base_impressions = int(base_impressions * 0.7)
                base_ctr = 0.018
            
            daily_budget = float(campaign.budget) / max(days_to_generate, 1)
            
            for day_offset in range(days_to_generate):
                analytics_date = today - timedelta(days=days_to_generate - day_offset - 1)
                
                if analytics_date > today or analytics_date < campaign.start_date:
                    continue
                
                growth_factor = 0.6 + (day_offset / days_to_generate) * 0.6
                randomness = random.uniform(0.85, 1.15)
                
                impressions = int(base_impressions * growth_factor * randomness)
                clicks = int(impressions * base_ctr * random.uniform(0.9, 1.1))
                conversions = int(clicks * random.uniform(0.05, 0.15))
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
            
            self.stdout.write(f"  ✅ {campaign.title[:35]}... Score: {summary.performance_score}/100")

        # ============================================================================
        # 6. CREATE A/B TEST
        # ============================================================================
        self.stdout.write('\n🧪 Creating A/B test...')

        test_campaign = campaigns[0]
        ab_test, created = ABTest.objects.get_or_create(
            campaign=test_campaign,
            name='Headline Test - Summer Sale',
            defaults={
                'description': 'Testing two headlines for performance',
                'status': 'running',
                'success_metric': 'ctr',
                'min_sample_size': 1000,
                'start_date': now() - timedelta(days=7)
            }
        )

        if created:
            ABTestVariation.objects.create(
                ab_test=ab_test,
                name='A',
                impressions=8500,
                clicks=340,
                conversions=42,
                spend=250
            )
            
            ABTestVariation.objects.create(
                ab_test=ab_test,
                name='B',
                impressions=8500,
                clicks=468,
                conversions=61,
                spend=250
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Created A/B test with variations'))

        # ============================================================================
        # SUMMARY
        # ============================================================================
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('🎉 DEMO SETUP COMPLETE!'))
        self.stdout.write('=' * 70)

        self.stdout.write('\n📋 DEMO CREDENTIALS:')
        self.stdout.write('-' * 70)
        for user_data in demo_users:
            self.stdout.write(f"Email: {user_data['email']:<30} Password: {user_data['password']}")
        self.stdout.write('-' * 70)

        total_campaigns = Campaign.objects.filter(user=demo_user).count()
        total_ads = AdContent.objects.filter(campaign__user=demo_user).count()
        total_analytics = DailyAnalytics.objects.filter(campaign__user=demo_user).count()

        self.stdout.write(f"\n✅ {total_campaigns} Campaigns created")
        self.stdout.write(f"✅ {total_ads} Ad variations")
        self.stdout.write(f"✅ {total_analytics} Days of analytics")
        self.stdout.write(f"✅ 3 Verified API keys")
        self.stdout.write(f"✅ 1 Active A/B test")
        
        self.stdout.write('\n🚀 READY FOR DEMO!')
        self.stdout.write('=' * 70)
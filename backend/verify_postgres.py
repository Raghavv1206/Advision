# backend/verify_postgres.py - PostgreSQL 18 Compatible

"""
Verification script for PostgreSQL 18 migration
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from core.models import (
    Campaign, AdContent, ImageAsset, Comment,
    DailyAnalytics, CampaignAnalyticsSummary,
    AdPlatformConnection, SyncedCampaign,
    ABTest, ABTestVariation,
    PredictiveModel, Prediction,
    ReportSchedule, GeneratedReport,
    UserAPIKey
)

User = get_user_model()

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_section(title):
    """Print a section header"""
    print(f"\n📊 {title}")
    print("-" * 70)

def verify_database_connection():
    """Verify PostgreSQL 18 connection"""
    print_header("VERIFICATION: PostgreSQL 18 Migration")
    
    try:
        with connection.cursor() as cursor:
            # Get PostgreSQL version
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            
            # Verify it's PostgreSQL 18
            if 'PostgreSQL 18' in db_version:
                version_status = "✅ PostgreSQL 18 Detected"
            else:
                version_status = f"⚠️  Version: {db_version.split(',')[0]}"
            
            # Get database name
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            
            # Get connection info
            cursor.execute("""
                SELECT 
                    inet_server_addr() as server_ip,
                    inet_server_port() as server_port,
                    current_user as connected_user;
            """)
            server_info = cursor.fetchone()
            
            # Check PostgreSQL 18 specific features
            cursor.execute("""
                SELECT setting 
                FROM pg_settings 
                WHERE name = 'server_version_num';
            """)
            version_num = cursor.fetchone()[0]
            
            print(f"\n{version_status}")
            print(f"\n📦 Database Information:")
            print(f"   • Database: {db_name}")
            print(f"   • User: {server_info[2]}")
            print(f"   • Host: {server_info[0] or 'localhost'}")
            print(f"   • Port: {server_info[1] or '5432'}")
            print(f"   • Version Number: {version_num}")
            print(f"\n🔧 PostgreSQL Version:")
            print(f"   {db_version[:100]}")
            
            # Check encoding (important for PostgreSQL 18)
            cursor.execute("SHOW server_encoding;")
            encoding = cursor.fetchone()[0]
            print(f"\n📝 Database Encoding: {encoding}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Database connection failed: {str(e)}")
        print("\nTroubleshooting for PostgreSQL 18:")
        print("1. Ensure PostgreSQL 18 service is running")
        print("2. Check pg_hba.conf for connection permissions")
        print("3. Verify .env credentials match database")
        return False

def verify_tables():
    """Verify all tables exist in PostgreSQL 18"""
    print_section("Database Tables (PostgreSQL 18)")
    
    try:
        with connection.cursor() as cursor:
            # PostgreSQL 18 compatible table query
            cursor.execute("""
                SELECT 
                    c.relname as tablename,
                    n.nspname as schemaname,
                    pg_size_pretty(pg_total_relation_size(c.oid)) as size
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = 'public'
                AND c.relkind = 'r'
                ORDER BY c.relname;
            """)
            tables = cursor.fetchall()
            
            print(f"   Found {len(tables)} tables:\n")
            
            core_tables = [
                'core_user',
                'core_campaign',
                'core_adcontent',
                'core_imageasset',
                'core_comment',
                'core_dailyanalytics',
                'core_campaignanalyticssummary',
                'core_userapikey',
                'core_abtest',
                'core_abtestvariation',
            ]
            
            existing_tables = [(t[0], t[2]) for t in tables]
            table_names = [t[0] for t in existing_tables]
            
            for table in core_tables:
                if table in table_names:
                    size = next(t[1] for t in existing_tables if t[0] == table)
                    print(f"   ✅ {table:<45} {size:>10}")
                else:
                    print(f"   ❌ {table:<45} MISSING")
            
            # Show additional tables
            other_tables = [(t[0], t[1]) for t in existing_tables 
                          if t[0] not in core_tables 
                          and not t[0].startswith('django_') 
                          and not t[0].startswith('auth_')]
            
            if other_tables:
                print(f"\n   📋 Additional tables ({len(other_tables)}):")
                for table, size in other_tables[:10]:
                    print(f"      • {table:<40} {size:>10}")
                if len(other_tables) > 10:
                    print(f"      ... and {len(other_tables) - 10} more")
            
            return True
            
    except Exception as e:
        print(f"\n   ❌ Error checking tables: {str(e)}")
        return False

def verify_postgresql18_features():
    """Check PostgreSQL 18 specific features"""
    print_section("PostgreSQL 18 Features Check")
    
    try:
        with connection.cursor() as cursor:
            # Check for PostgreSQL 18 improvements
            features = []
            
            # 1. Check parallel query support
            cursor.execute("SHOW max_parallel_workers_per_gather;")
            parallel_workers = cursor.fetchone()[0]
            features.append(('Parallel Query Support', parallel_workers != '0', parallel_workers))
            
            # 2. Check JIT compilation
            cursor.execute("SHOW jit;")
            jit_enabled = cursor.fetchone()[0]
            features.append(('JIT Compilation', jit_enabled == 'on', jit_enabled))
            
            # 3. Check shared buffers
            cursor.execute("SHOW shared_buffers;")
            shared_buffers = cursor.fetchone()[0]
            features.append(('Shared Buffers', True, shared_buffers))
            
            # 4. Check work memory
            cursor.execute("SHOW work_mem;")
            work_mem = cursor.fetchone()[0]
            features.append(('Work Memory', True, work_mem))
            
            # 5. Check maintenance work memory
            cursor.execute("SHOW maintenance_work_mem;")
            maintenance_mem = cursor.fetchone()[0]
            features.append(('Maintenance Work Mem', True, maintenance_mem))
            
            print()
            for feature, status, value in features:
                status_icon = "✅" if status else "⚠️"
                print(f"   {status_icon} {feature:<30} {value}")
            
            return True
            
    except Exception as e:
        print(f"\n   ❌ Error checking PostgreSQL 18 features: {str(e)}")
        return False

def verify_data():
    """Verify data migration"""
    print_section("Data Verification")
    
    try:
        models_to_check = [
            ('Users', User),
            ('Campaigns', Campaign),
            ('Ad Content', AdContent),
            ('Images', ImageAsset),
            ('Comments', Comment),
            ('Daily Analytics', DailyAnalytics),
            ('Analytics Summaries', CampaignAnalyticsSummary),
            ('API Keys', UserAPIKey),
            ('A/B Tests', ABTest),
            ('A/B Test Variations', ABTestVariation),
            ('Platform Connections', AdPlatformConnection),
            ('Synced Campaigns', SyncedCampaign),
            ('Predictive Models', PredictiveModel),
            ('Predictions', Prediction),
            ('Report Schedules', ReportSchedule),
            ('Generated Reports', GeneratedReport),
        ]
        
        total_records = 0
        
        print()
        for name, model in models_to_check:
            try:
                count = model.objects.count()
                total_records += count
                status = "✅" if count > 0 else "⚪"
                print(f"   {status} {name:<25} {count:>6} records")
            except Exception as e:
                print(f"   ❌ {name:<25} Error: {str(e)[:30]}")
        
        print(f"\n   📊 Total Records: {total_records:,}")
        
        return True
        
    except Exception as e:
        print(f"\n   ❌ Error verifying data: {str(e)}")
        return False

def verify_indexes():
    """Verify database indexes (PostgreSQL 18)"""
    print_section("Database Indexes")
    
    try:
        with connection.cursor() as cursor:
            # PostgreSQL 18 compatible index query
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = 'public'
                AND tablename LIKE 'core_%'
                ORDER BY tablename, indexname;
            """)
            indexes = cursor.fetchall()
            
            print(f"   Found {len(indexes)} indexes on core tables\n")
            
            # Group by table
            from collections import defaultdict
            indexes_by_table = defaultdict(list)
            
            for schema, table, index_name, index_def in indexes:
                indexes_by_table[table].append(index_name)
            
            for table, index_list in sorted(indexes_by_table.items()):
                print(f"   📋 {table}: {len(index_list)} indexes")
                for idx in index_list[:3]:
                    print(f"      • {idx}")
                if len(index_list) > 3:
                    print(f"      ... and {len(index_list) - 3} more")
            
            return True
            
    except Exception as e:
        print(f"\n   ❌ Error checking indexes: {str(e)}")
        return False

def check_data_integrity():
    """Check data integrity"""
    print_section("Data Integrity Check")
    
    try:
        checks = []
        
        # Check 1: Campaigns with users
        try:
            campaigns_without_users = Campaign.objects.filter(user__isnull=True).count()
            checks.append(('Campaigns without users', campaigns_without_users == 0, campaigns_without_users))
        except:
            checks.append(('Campaigns without users', False, 'Error'))
        
        # Check 2: Ad content with campaigns
        try:
            ads_without_campaigns = AdContent.objects.filter(campaign__isnull=True).count()
            checks.append(('Ads without campaigns', ads_without_campaigns == 0, ads_without_campaigns))
        except:
            checks.append(('Ads without campaigns', False, 'Error'))
        
        # Check 3: Images with campaigns
        try:
            images_without_campaigns = ImageAsset.objects.filter(campaign__isnull=True).count()
            checks.append(('Images without campaigns', images_without_campaigns == 0, images_without_campaigns))
        except:
            checks.append(('Images without campaigns', False, 'Error'))
        
        # Check 4: Analytics summaries
        try:
            campaigns_count = Campaign.objects.count()
            summaries_count = CampaignAnalyticsSummary.objects.count()
            checks.append(('Analytics summaries', campaigns_count == summaries_count, f"{summaries_count}/{campaigns_count}"))
        except:
            checks.append(('Analytics summaries', False, 'Error'))
        
        print()
        for check_name, passed, value in checks:
            status = "✅" if passed else "⚠️"
            print(f"   {status} {check_name:<40} {value}")
        
        return all(check[1] for check in checks)
        
    except Exception as e:
        print(f"\n   ❌ Error checking data integrity: {str(e)}")
        return False

def get_database_size():
    """Get database size information"""
    print_section("Database Size")
    
    try:
        with connection.cursor() as cursor:
            # Database size
            cursor.execute("""
                SELECT 
                    pg_size_pretty(pg_database_size(current_database())) as db_size,
                    pg_database_size(current_database()) as db_size_bytes;
            """)
            db_size, db_size_bytes = cursor.fetchone()
            
            print(f"   📦 Total Database Size: {db_size}")
            
            # Table sizes
            cursor.execute("""
                SELECT 
                    schemaname||'.'||tablename as full_name,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
                    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                FROM pg_tables
                WHERE schemaname = 'public'
                AND tablename LIKE 'core_%'
                ORDER BY size_bytes DESC
                LIMIT 10;
            """)
            tables = cursor.fetchall()
            
            print(f"\n   📊 Top 10 Largest Tables:\n")
            for table, size, size_bytes in tables:
                print(f"      {table:<40} {size:>10}")
            
            return True
            
    except Exception as e:
        print(f"\n   ❌ Error getting database size: {str(e)}")
        return False

def test_database_performance():
    """Test database performance on PostgreSQL 18"""
    print_section("Performance Test (PostgreSQL 18)")
    
    try:
        import time
        
        # Test 1: Simple query
        start = time.time()
        User.objects.all().count()
        simple_query_time = (time.time() - start) * 1000
        
        # Test 2: Join query
        start = time.time()
        list(Campaign.objects.select_related('user').prefetch_related('ad_content')[:10])
        join_query_time = (time.time() - start) * 1000
        
        # Test 3: Aggregate query
        start = time.time()
        from django.db.models import Sum, Avg
        Campaign.objects.aggregate(
            total_budget=Sum('budget'),
            avg_budget=Avg('budget')
        )
        aggregate_query_time = (time.time() - start) * 1000
        
        print(f"\n   ⚡ Query Performance:")
        print(f"      Simple query:     {simple_query_time:>8.2f} ms")
        print(f"      Join query:       {join_query_time:>8.2f} ms")
        print(f"      Aggregate query:  {aggregate_query_time:>8.2f} ms")
        
        # Performance assessment
        max_time = max(simple_query_time, join_query_time, aggregate_query_time)
        if max_time < 100:
            print(f"\n   ✅ Performance: Excellent (PostgreSQL 18 optimized)")
        elif max_time < 500:
            print(f"\n   ✅ Performance: Good")
        else:
            print(f"\n   ⚠️  Performance: Consider adding indexes or tuning PostgreSQL 18")
        
        return True
        
    except Exception as e:
        print(f"\n   ❌ Error testing performance: {str(e)}")
        return False

def print_summary(results):
    """Print verification summary"""
    print_header("VERIFICATION SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    
    print(f"\n   Total Checks: {total_checks}")
    print(f"   Passed: {passed_checks}")
    print(f"   Failed: {total_checks - passed_checks}")
    print(f"\n   Success Rate: {(passed_checks/total_checks)*100:.1f}%")
    
    if passed_checks == total_checks:
        print("\n   🎉 ALL CHECKS PASSED!")
        print("   Your PostgreSQL 18 migration is complete and verified.")
    else:
        print("\n   ⚠️  SOME CHECKS FAILED")
        print("   Please review the errors above.")
        print("\n   Failed checks:")
        for check, passed in results.items():
            if not passed:
                print(f"      ❌ {check}")
    
    print("\n" + "=" * 70)

def main():
    """Run all verification checks"""
    
    results = {}
    
    # Run all verification checks
    results['Database Connection'] = verify_database_connection()
    
    if results['Database Connection']:
        results['PostgreSQL 18 Features'] = verify_postgresql18_features()
        results['Tables'] = verify_tables()
        results['Data'] = verify_data()
        results['Indexes'] = verify_indexes()
        results['Data Integrity'] = check_data_integrity()
        results['Database Size'] = get_database_size()
        results['Performance'] = test_database_performance()
    
    # Print summary
    print_summary(results)
    
    # PostgreSQL 18 specific recommendations
    print("\n💡 PostgreSQL 18 OPTIMIZATION TIPS:")
    print("   1. Enable JIT compilation for complex queries")
    print("   2. Tune shared_buffers to 25% of RAM")
    print("   3. Use EXPLAIN ANALYZE for slow queries")
    print("   4. Enable parallel queries for better performance")
    print("   5. Regular VACUUM and ANALYZE operations")
    
    print("\n📝 PostgreSQL 18 Backup Commands:")
    print("   Export: pg_dump -U advision_user -Fc advision_db > backup.dump")
    print("   Import: pg_restore -U advision_user -d advision_db backup.dump")
    print("   SQL Export: pg_dump -U advision_user advision_db > backup.sql")
    
    return all(results.values())

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
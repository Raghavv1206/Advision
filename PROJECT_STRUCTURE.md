# AdVision Project - Directory Structure

```
advision-project/
├── docker-compose.yml
├── .env
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── create_demo_data.py
│   │
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── views_advanced.py
│   │   ├── views_api_keys.py
│   │   ├── views_oauth.py
│   │   ├── views_predictive.py
│   │   ├── views_sync.py
│   │   ├── adapters.py
│   │   ├── managers.py
│   │   │
│   │   ├── management/
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── clean_duplicates.py
│   │   │       ├── generate_analytics.py
│   │   │       └── setup_demo.py
│   │   │
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_adcontent_clicks_adcontent_conversions_and_more.py
│   │   │   ├── 0003_abtest_adplatformconnection_reportschedule_and_more.py
│   │   │   └── 0004_userapikey.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── ab_testing.py
│   │       ├── ad_platforms.py
│   │       └── predictive_analytics.py
│   │
│   └── media/
│       └── generated_images/
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── eslint.config.js
    ├── index.html
    ├── README.md
    │
    ├── public/
    │
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx
    │   ├── index.css
    │   │
    │   ├── api/
    │   │   └── client.js
    │   │
    │   ├── assets/
    │   │
    │   ├── components/
    │   │   ├── GoogleLoginButton.jsx
    │   │   ├── ProtectedRoute.jsx
    │   │   ├── SyncCampaignsButton.jsx
    │   │   └── UnicornBackground.jsx
    │   │
    │   ├── layouts/
    │   │   └── AppLayout.jsx
    │   │
    │   └── pages/
    │       ├── ABTestingPage.jsx
    │       ├── AnalyticsPage.jsx
    │       ├── APIKeysPage.jsx
    │       ├── AudienceInsightsPage.jsx
    │       ├── CampaignDetailPage.jsx
    │       ├── CampaignsPage.jsx
    │       ├── ContentGeneratorPage.jsx
    │       ├── ContentLibraryPage.jsx
    │       ├── DashboardPage.jsx
    │       ├── HomePage.jsx
    │       ├── LoginPage.jsx
    │       ├── ProfilePage.jsx
    │       ├── RegisterPage.jsx
    │       └── WeeklyReportPage.jsx
```

## Project Summary

**Backend:** Django REST Framework API
- Main app: `core/` (models, serializers, views, services)
- Database: SQLite (db.sqlite3)
- Services: A/B Testing, Ad Platforms, Predictive Analytics
- Management Commands: Demo setup, duplicate cleaning, analytics generation

**Frontend:** React with Vite
- Build tool: Vite
- Styling: Tailwind CSS
- Components: Google Login, Protected Routes, Campaign Sync
- Pages: Dashboard, Analytics, Campaigns, Content Generator, A/B Testing, etc.

**Infrastructure:**
- Docker Compose setup for containerization
- Environment configuration via .env files

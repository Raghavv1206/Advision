# backend/core/views_oauth.py - UPDATED WITH ENVIRONMENT VARIABLES (BASED ON WORKING CODE)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp
import requests
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class GoogleOAuthView(APIView):
    """Custom Google OAuth handler using environment variables"""
    permission_classes = [permissions.AllowAny]  # CRITICAL: Must allow unauthenticated access
    authentication_classes = []  # CRITICAL: Disable authentication for this endpoint
    
    def post(self, request):
        code = request.data.get('code')
        
        # Get redirect_uri from request (frontend will send it)
        redirect_uri = request.data.get('redirect_uri')
        
        # Fallback to environment variable if not provided
        if not redirect_uri:
            redirect_uri = getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', None)
        
        # Final fallback: build from FRONTEND_URL
        if not redirect_uri:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
            # @react-oauth/google uses the origin directly, not /auth/google/callback
            redirect_uri = frontend_url
        
        logger.info(f"🔐 Google OAuth: Received code: {code[:20] if code else 'None'}...")
        logger.info(f"🔐 Redirect URI from request.data: {request.data.get('redirect_uri')}")
        logger.info(f"🔐 GOOGLE_OAUTH_REDIRECT_URI setting: {getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', 'NOT SET')}")
        logger.info(f"🔐 FRONTEND_URL setting: {getattr(settings, 'FRONTEND_URL', 'NOT SET')}")
        logger.info(f"🔐 Final redirect_uri being used: {redirect_uri}")
        
        if not code:
            return Response(
                {'error': 'Authorization code is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if credentials are configured
        client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', None)
        client_secret = getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', None)
        
        if not client_id or not client_secret:
            logger.error("❌ Google OAuth credentials not configured")
            return Response(
                {'error': 'Google OAuth is not properly configured. Please add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env file.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            # Step 1: Exchange code for access token
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            logger.info(f"📡 Exchanging code for token...")
            token_response = requests.post(token_url, data=token_data, timeout=10)
            
            if token_response.status_code != 200:
                error_detail = token_response.json()
                logger.error(f"❌ Token exchange failed: {error_detail}")
                return Response(
                    {
                        'error': 'Failed to exchange code for token',
                        'details': error_detail
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token_json = token_response.json()
            access_token = token_json.get('access_token')
            logger.info(f"✅ Got access token")
            
            # Step 2: Get user info from Google
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            
            logger.info(f"📡 Fetching user info from Google...")
            user_info_response = requests.get(user_info_url, headers=headers, timeout=10)
            
            if user_info_response.status_code != 200:
                logger.error(f"❌ Failed to get user info: {user_info_response.text}")
                return Response(
                    {'error': 'Failed to get user info from Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_info = user_info_response.json()
            email = user_info.get('email')
            google_id = user_info.get('id')
            name = user_info.get('name', '')
            
            logger.info(f"✅ Got user info: {email}")
            
            if not email:
                return Response(
                    {'error': 'Email not provided by Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Step 3: Get or create user
            user, user_created = User.objects.get_or_create(
                email=email,
                defaults={
                    'role': 'viewer',
                    'is_active': True
                }
            )
            
            if user_created:
                logger.info(f"✅ Created new user: {email}")
            else:
                logger.info(f"✅ Found existing user: {email}")
            
            # Step 4: Create or update EmailAddress
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                defaults={
                    'verified': True,
                    'primary': True
                }
            )
            
            if created:
                logger.info(f"✅ Created EmailAddress for {email}")
            
            # Step 5: Get or create SocialApp for Google
            try:
                social_app = SocialApp.objects.get(provider='google')
                logger.info(f"✅ Found existing Google SocialApp")
            except SocialApp.DoesNotExist:
                logger.info(f"📝 Creating Google SocialApp...")
                from django.contrib.sites.models import Site
                social_app = SocialApp.objects.create(
                    provider='google',
                    name='Google',
                    client_id=client_id,
                    secret=client_secret
                )
                # Add the current site
                site = Site.objects.get_current()
                social_app.sites.add(site)
                logger.info(f"✅ Created Google SocialApp")
            
            # Step 6: Create or update SocialAccount
            social_account, created = SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': google_id,
                    'extra_data': user_info
                }
            )
            
            if created:
                logger.info(f"✅ Created SocialAccount for {email}")
            else:
                # Update extra_data if account exists
                social_account.extra_data = user_info
                social_account.save()
                logger.info(f"✅ Updated SocialAccount for {email}")
            
            # Step 7: Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"✅ Generated JWT tokens for {email}")
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_200_OK)
            
        except requests.RequestException as e:
            logger.error(f"❌ Network error: {str(e)}")
            return Response(
                {'error': f'Network error: {str(e)}'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"❌ Authentication failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Authentication failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
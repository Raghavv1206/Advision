# backend/core/views_oauth.py - GOOGLE ONLY
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp
import requests

User = get_user_model()

class GoogleOAuthView(APIView):
    """Custom Google OAuth handler"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'Authorization code is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Step 1: Exchange code for access token
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'code': code,
                'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': 'http://localhost:5173',
                'grant_type': 'authorization_code'
            }
            
            token_response = requests.post(token_url, data=token_data, timeout=10)
            
            if token_response.status_code != 200:
                return Response(
                    {'error': 'Failed to exchange code for token', 'details': token_response.text}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token_json = token_response.json()
            access_token = token_json.get('access_token')
            
            # Step 2: Get user info from Google
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_info_response = requests.get(user_info_url, headers=headers, timeout=10)
            
            if user_info_response.status_code != 200:
                return Response(
                    {'error': 'Failed to get user info from Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_info = user_info_response.json()
            email = user_info.get('email')
            google_id = user_info.get('id')
            
            if not email:
                return Response(
                    {'error': 'Email not provided by Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Step 3: Get or create user
            user, user_created = User.objects.get_or_create(
                email=email,
                defaults={'role': 'viewer'}
            )
            
            # Step 4: Create or update EmailAddress
            EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                defaults={
                    'verified': True,
                    'primary': True
                }
            )
            
            # Step 5: Create or update SocialAccount
            try:
                social_app = SocialApp.objects.get(provider='google')
            except SocialApp.DoesNotExist:
                social_app = SocialApp.objects.create(
                    provider='google',
                    name='Google',
                    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
                    secret=settings.GOOGLE_OAUTH_CLIENT_SECRET
                )
                social_app.sites.add(1)
            
            SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': google_id,
                    'extra_data': user_info
                }
            )
            
            # Step 6: Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
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
            return Response(
                {'error': f'Network error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'Authentication failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
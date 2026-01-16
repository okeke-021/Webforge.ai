from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
import secrets


class GitHubLoginView(APIView):
    """
    Initiate GitHub OAuth flow
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        state = secrets.token_urlsafe(32)
        request.session['oauth_state'] = state
        
        github_auth_url = (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={settings.GITHUB_CLIENT_ID}&"
            f"redirect_uri={settings.GITHUB_CALLBACK_URL}&"
            f"scope=user:email,repo&"
            f"state={state}"
        )
        
        return redirect(github_auth_url)


class GitHubCallbackView(APIView):
    """
    Handle GitHub OAuth callback
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        
        # Verify state
        session_state = request.session.get('oauth_state')
        if not state or state != session_state:
            return redirect(f"{settings.CORS_ALLOWED_ORIGINS[0]}/?error=invalid_state")
        
        # Exchange code for access token
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': settings.GITHUB_CLIENT_ID,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code,
                'redirect_uri': settings.GITHUB_CALLBACK_URL
            },
            headers={'Accept': 'application/json'}
        )
        
        if token_response.status_code != 200:
            return redirect(f"{settings.CORS_ALLOWED_ORIGINS[0]}/?error=token_exchange_failed")
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            return redirect(f"{settings.CORS_ALLOWED_ORIGINS[0]}/?error=no_access_token")
        
        # Get user info from GitHub
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if user_response.status_code != 200:
            return redirect(f"{settings.CORS_ALLOWED_ORIGINS[0]}/?error=user_fetch_failed")
        
        github_user = user_response.json()
        
        # Get user email
        email_response = requests.get(
            'https://api.github.com/user/emails',
            headers={'Authorization': f'token {access_token}'}
        )
        
        emails = email_response.json() if email_response.status_code == 200 else []
        primary_email = next(
            (email['email'] for email in emails if email['primary']),
            github_user.get('email')
        )
        
        # Create or get user
        user, created = User.objects.get_or_create(
            username=github_user['login'],
            defaults={
                'email': primary_email or '',
                'first_name': github_user.get('name', '').split()[0] if github_user.get('name') else ''
            }
        )
        
        # Store GitHub token in session (encrypted)
        request.session['github_token'] = access_token
        request.session['github_username'] = github_user['login']
        
        # Login user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Redirect to frontend
        return redirect(settings.CORS_ALLOWED_ORIGINS[0])


class LogoutView(APIView):
    """
    Logout user
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


class MeView(APIView):
    """
    Get current user info
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get or create usage
        from apps.generator.models import UserUsage
        usage, _ = UserUsage.objects.get_or_create(user=user)
        
        # Get subscription (from profile or default to free)
        subscription = getattr(user, 'subscription', 'free')
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'subscription': subscription,
            'usage': {
                'monthlyGenerations': usage.monthly_generations,
                'todayRequests': usage.today_requests,
                'totalProjects': usage.total_projects
            },
            'github_connected': bool(request.session.get('github_token'))
        })

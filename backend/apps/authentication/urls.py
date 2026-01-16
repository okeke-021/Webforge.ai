from django.urls import path
from .views import GitHubLoginView, GitHubCallbackView, LogoutView, MeView

urlpatterns = [
    path('github/login/', GitHubLoginView.as_view(), name='github-login'),
    path('github/callback/', GitHubCallbackView.as_view(), name='github-callback'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]

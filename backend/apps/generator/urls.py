from django.urls import path
from .views import (
    GenerateProjectView,
    ProjectDetailView,
    ProjectListView,
    ProjectLogsView,
    DownloadProjectView,
    UsageStatsView,
    DebugRepositoryView,
    DebugSessionDetailView,
    DebugSessionListView,
    ApplyFixesView
)

urlpatterns = [
    # Project generation
    path('generate/', GenerateProjectView.as_view(), name='generate-project'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<uuid:project_id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<uuid:project_id>/logs/', ProjectLogsView.as_view(), name='project-logs'),
    path('projects/<uuid:project_id>/download/', DownloadProjectView.as_view(), name='project-download'),
    
    # Debugging
    path('debug/', DebugRepositoryView.as_view(), name='debug-repository'),
    path('debug/sessions/', DebugSessionListView.as_view(), name='debug-session-list'),
    path('debug/<uuid:session_id>/', DebugSessionDetailView.as_view(), name='debug-session-detail'),
    path('debug/<uuid:session_id>/apply-fixes/', ApplyFixesView.as_view(), name='apply-fixes'),
    
    # Usage stats
    path('usage/', UsageStatsView.as_view(), name='usage-stats'),
]

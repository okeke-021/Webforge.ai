from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Project, DebugSession, CodeIssue, GenerationLog, UserUsage
from .serializers import ProjectSerializer, ProjectCreateSerializer, DebugSessionSerializer
from .tasks import generate_project_task, debug_repository_task
from ai_engine.code_debugger import CodeDebugger
import logging

logger = logging.getLogger(__name__)


class GenerateProjectView(APIView):
    """API endpoint to initiate project generation"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user = request.user
            usage, _ = UserUsage.objects.get_or_create(user=user)
            
            subscription = getattr(user, 'subscription', 'free')
            
            if not usage.can_generate(subscription):
                return Response({
                    'error': 'Generation limit reached',
                    'message': 'You have reached your monthly generation limit. Please upgrade your plan.',
                    'limit_reached': True
                }, status=status.HTTP_403_FORBIDDEN)
            
            if not usage.can_make_request(subscription):
                return Response({
                    'error': 'Rate limit exceeded',
                    'message': 'You have made too many requests today. Please try again tomorrow.',
                    'rate_limited': True
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            serializer = ProjectCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            project = Project.objects.create(
                user=user,
                name=serializer.validated_data.get('name', 'Untitled Project'),
                description=serializer.validated_data['description'],
                features=serializer.validated_data.get('features', []),
                tech_stack=serializer.validated_data.get('tech_stack', {}),
                style_preferences=serializer.validated_data.get('style_preferences', {}),
                status='pending'
            )
            
            GenerationLog.objects.create(
                project=project,
                log_type='info',
                message='Project generation started'
            )
            
            usage.monthly_generations += 1
            usage.today_requests += 1
            usage.total_projects += 1
            usage.last_generation = timezone.now()
            usage.save()
            
            generate_project_task.delay(str(project.id))
            
            return Response(
                ProjectSerializer(project).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Project generation failed: {str(e)}")
            return Response({
                'error': 'Generation failed',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DebugRepositoryView(APIView):
    """
    Debug an existing GitHub repository
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user = request.user
            usage, _ = UserUsage.objects.get_or_create(user=user)
            
            subscription = getattr(user, 'subscription', 'free')
            
            # Check if user has access to debugging
            if not usage.can_debug(subscription):
                return Response({
                    'error': 'Feature not available',
                    'message': 'Debug feature is only available for Enterprise plan subscribers.',
                    'upgrade_required': True
                }, status=status.HTTP_403_FORBIDDEN)
            
            repo_url = request.data.get('repo_url')
            if not repo_url:
                return Response({
                    'error': 'Repository URL required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract repo name
            repo_name = repo_url.rstrip('/').split('/')[-1]
            
            # Create debug session
            debug_session = DebugSession.objects.create(
                user=user,
                repo_url=repo_url,
                repo_name=repo_name,
                status='pending'
            )
            
            usage.monthly_debugs += 1
            usage.total_debug_sessions += 1
            usage.last_debug = timezone.now()
            usage.save()
            
            # Start debugging task
            debug_repository_task.delay(str(debug_session.id))
            
            return Response(
                DebugSessionSerializer(debug_session).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Debug initialization failed: {str(e)}")
            return Response({
                'error': 'Debug failed',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DebugSessionDetailView(APIView):
    """
    Get debug session details
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        try:
            debug_session = DebugSession.objects.get(id=session_id, user=request.user)
            return Response(DebugSessionSerializer(debug_session).data)
        except DebugSession.DoesNotExist:
            return Response({
                'error': 'Debug session not found'
            }, status=status.HTTP_404_NOT_FOUND)


class DebugSessionListView(APIView):
    """
    List all debug sessions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sessions = DebugSession.objects.filter(user=request.user)
        serializer = DebugSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class ApplyFixesView(APIView):
    """
    Apply fixes and create pull request
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        try:
            debug_session = DebugSession.objects.get(id=session_id, user=request.user)
            
            if debug_session.status != 'completed':
                return Response({
                    'error': 'Debug session not completed'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get GitHub token from session
            github_token = request.session.get('github_token')
            if not github_token:
                return Response({
                    'error': 'GitHub authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create pull request with fixes
            debugger = CodeDebugger()
            
            pr_url = debugger.create_pull_request(
                repo_url=debug_session.repo_url,
                github_token=github_token,
                fixed_files=debug_session.fixed_files,
                issues=debug_session.issues
            )
            
            debug_session.pull_request_url = pr_url
            debug_session.save()
            
            return Response({
                'pull_request_url': pr_url,
                'message': 'Pull request created successfully'
            })
            
        except DebugSession.DoesNotExist:
            return Response({
                'error': 'Debug session not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to apply fixes: {str(e)}")
            return Response({
                'error': 'Failed to create pull request',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetailView(APIView):
    """Get, update, or delete a specific project"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, user=request.user)
            return Response(ProjectSerializer(project).data)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, user=request.user)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)


class ProjectListView(APIView):
    """List all projects for authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        projects = Project.objects.filter(user=request.user)
        
        status_filter = request.query_params.get('status')
        if status_filter:
            projects = projects.filter(status=status_filter)
        
        search = request.query_params.get('search')
        if search:
            projects = projects.filter(name__icontains=search)
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectLogsView(APIView):
    """Get generation logs for a project"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, user=request.user)
            logs = project.logs.all()
            
            return Response([{
                'timestamp': log.timestamp.isoformat(),
                'type': log.log_type,
                'message': log.message,
                'details': log.details
            } for log in logs])
            
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)


class DownloadProjectView(APIView):
    """Download project as ZIP file"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            from django.http import HttpResponse
            import zipfile
            import io
            
            project = Project.objects.get(id=project_id, user=request.user)
            
            if not project.generated_files:
                return Response({
                    'error': 'Project files not available'
                }, status=status.HTTP_404_NOT_FOUND)
            
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for filepath, content in project.generated_files.items():
                    zip_file.writestr(filepath, content)
            
            zip_buffer.seek(0)
            
            response = HttpResponse(zip_buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{project.name}.zip"'
            
            return response
            
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)


class UsageStatsView(APIView):
    """Get usage statistics for authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        usage, _ = UserUsage.objects.get_or_create(user=user)
        
        subscription = getattr(user, 'subscription', 'free')
        
        limits = {
            'free': {'generations': 3, 'dailyRequests': 5, 'debugs': 0},
            'pro': {'generations': 10, 'dailyRequests': 20, 'debugs': 0},
            'enterprise': {'generations': 20, 'dailyRequests': 50, 'debugs': 999}
        }
        
        limit = limits.get(subscription, limits['free'])
        
        return Response({
            'subscription': subscription,
            'usage': {
                'monthlyGenerations': usage.monthly_generations,
                'monthlyDebugs': usage.monthly_debugs,
                'todayRequests': usage.today_requests,
                'totalProjects': usage.total_projects,
                'successfulProjects': usage.successful_projects,
                'failedProjects': usage.failed_projects,
                'totalDebugSessions': usage.total_debug_sessions,
                'successfulDebugs': usage.successful_debugs
            },
            'limits': limit,
            'remaining': {
                'generations': max(0, limit['generations'] - usage.monthly_generations),
                'debugs': 'unlimited' if subscription == 'enterprise' else 0,
                'requests': max(0, limit['dailyRequests'] - usage.today_requests)
            }
        })

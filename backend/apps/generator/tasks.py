from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Project, DebugSession, CodeIssue, GenerationLog, UserUsage
from ai_engine.gemini_planner import GeminiPlanner
from ai_engine.code_generator import CodeGenerator
from ai_engine.quality_validator import QualityValidator
from ai_engine.packager import Packager
from ai_engine.code_debugger import CodeDebugger
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_project_task(project_id):
    """
    Celery task to generate project asynchronously
    """
    try:
        project = Project.objects.get(id=project_id)
        channel_layer = get_channel_layer()
        
        def send_update(status, progress, message, msg_type='info'):
            """Helper to send WebSocket updates"""
            project.status = status
            project.progress = progress
            project.save()
            
            GenerationLog.objects.create(
                project=project,
                log_type=msg_type,
                message=message
            )
            
            async_to_sync(channel_layer.group_send)(
                f'project_{project_id}',
                {
                    'type': 'generation_status',
                    'status': status,
                    'progress': progress,
                    'message': message,
                    'msg_type': msg_type
                }
            )
        
        # Step 1: Analyzing Requirements (0-20%)
        send_update('analyzing', 10, 'Starting requirement analysis...', 'info')
        
        planner = GeminiPlanner()
        specs = planner.analyze_requirements(
            description=project.description,
            features=project.features,
            tech_stack=project.tech_stack,
            style_preferences=project.style_preferences
        )
        
        project.specifications = specs
        project.save()
        
        send_update('analyzing', 20, 'Requirements analyzed successfully', 'success')
        
        # Step 2: Planning Architecture (20-40%)
        send_update('planning', 25, 'Planning project architecture...', 'info')
        send_update('planning', 35, f"Creating {len(specs.get('file_structure', []))} files", 'info')
        send_update('planning', 40, 'Architecture planning complete', 'success')
        
        # Step 3: Generating Code (40-70%)
        send_update('generating', 45, 'Starting code generation...', 'info')
        
        generator = CodeGenerator()
        files = generator.generate_project_files(specs)
        
        project.generated_files = files
        project.save()
        
        send_update('generating', 60, f"Generated {len(files)} files", 'info')
        send_update('generating', 70, 'Code generation complete', 'success')
        
        # Step 4: Validating Code (70-85%)
        send_update('validating', 72, 'Running code quality checks...', 'info')
        
        validator = QualityValidator()
        validation_results = validator.validate_project(files)
        
        if not validation_results['overall_valid']:
            send_update('validating', 75, f"Found {len(validation_results['issues'])} issues", 'warning')
        else:
            send_update('validating', 80, 'All quality checks passed', 'success')
        
        send_update('validating', 85, 'Validation complete', 'success')
        
        # Step 5: Packaging (85-95%)
        send_update('packaging', 87, 'Creating project package...', 'info')
        
        packager = Packager()
        
        # Create GitHub repository if requested
        github_url = None
        try:
            send_update('packaging', 90, 'Creating GitHub repository...', 'info')
            github_url = packager.create_github_repo(
                project_name=specs['project_name'],
                files=files,
                user=project.user
            )
            project.github_repo_url = github_url
            project.save()
            send_update('packaging', 93, f"Repository created: {github_url}", 'success')
        except Exception as e:
            logger.warning(f"GitHub repo creation failed: {str(e)}")
            send_update('packaging', 93, 'Skipping GitHub (optional)', 'warning')
        
        send_update('packaging', 95, 'Packaging complete', 'success')
        
        # Step 6: Completed (95-100%)
        project.status = 'completed'
        project.progress = 100
        project.completed_at = timezone.now()
        project.save()
        
        # Update user usage stats
        usage = UserUsage.objects.get(user=project.user)
        usage.successful_projects += 1
        usage.save()
        
        async_to_sync(channel_layer.group_send)(
            f'project_{project_id}',
            {
                'type': 'generation_complete',
                'project_id': str(project.id),
                'github_url': github_url,
                'files_count': len(files),
                'duration': project.duration
            }
        )
        
        logger.info(f"Project {project_id} generated successfully")
        
    except Exception as e:
        logger.error(f"Project generation failed for {project_id}: {str(e)}")
        
        try:
            project = Project.objects.get(id=project_id)
            project.status = 'failed'
            project.error_message = str(e)
            project.save()
            
            # Update user usage stats
            usage = UserUsage.objects.get(user=project.user)
            usage.failed_projects += 1
            usage.save()
            
            GenerationLog.objects.create(
                project=project,
                log_type='error',
                message=f'Generation failed: {str(e)}'
            )
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'project_{project_id}',
                {
                    'type': 'generation_error',
                    'error': str(e)
                }
            )
        except Exception as inner_e:
            logger.error(f"Error handling failure: {str(inner_e)}")


@shared_task
def debug_repository_task(session_id):
    """
    Celery task to debug repository asynchronously
    """
    try:
        debug_session = DebugSession.objects.get(id=session_id)
        channel_layer = get_channel_layer()
        
        def send_update(status, progress, message):
            """Helper to send WebSocket updates"""
            debug_session.status = status
            debug_session.progress = progress
            debug_session.save()
            
            async_to_sync(channel_layer.group_send)(
                f'debug_{session_id}',
                {
                    'type': 'debug_status',
                    'status': status,
                    'progress': progress,
                    'message': message
                }
            )
        
        # Get GitHub token from user session
        from django.contrib.sessions.models import Session
        github_token = None
        for session in Session.objects.all():
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(debug_session.user.id):
                github_token = data.get('github_token')
                break
        
        if not github_token:
            raise ValueError("GitHub authentication required")
        
        # Step 1: Analyzing Repository (0-40%)
        send_update('analyzing', 10, 'Fetching repository files...')
        
        debugger = CodeDebugger()
        analysis_results = debugger.analyze_repository(
            repo_url=debug_session.repo_url,
            github_token=github_token
        )
        
        send_update('analyzing', 40, f"Analyzed {analysis_results['total_files_analyzed']} files")
        
        # Save analysis results
        debug_session.total_files_analyzed = analysis_results['total_files_analyzed']
        debug_session.total_issues_found = analysis_results['total_issues_found']
        debug_session.issues = analysis_results['issues']
        debug_session.severity_breakdown = analysis_results['severity_breakdown']
        debug_session.save()
        
        # Save individual issues
        for issue in analysis_results['issues']:
            CodeIssue.objects.create(
                debug_session=debug_session,
                file_path=issue['file'],
                line_number=issue.get('line'),
                issue_type=issue['type'],
                severity=issue['severity'],
                description=issue['description'],
                code_snippet=issue.get('code_snippet', ''),
                suggestion=issue['suggestion'],
                fixed_code=issue.get('fixed_code', '')
            )
        
        # Step 2: Generating Fixes (40-80%)
        send_update('fixing', 50, 'Generating fixes for detected issues...')
        
        # Get repository files
        from github import Github
        g = Github(github_token)
        parts = debug_session.repo_url.rstrip('/').split('/')
        owner, repo_name = parts[-2], parts[-1]
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        repo_files = debugger._get_all_files(repo)
        
        fixed_files = debugger.generate_fixes(analysis_results['issues'], repo_files)
        
        debug_session.fixed_files = fixed_files
        debug_session.save()
        
        send_update('fixing', 80, f"Generated fixes for {len(fixed_files)} files")
        
        # Mark issues as fixed
        CodeIssue.objects.filter(
            debug_session=debug_session,
            file_path__in=fixed_files.keys()
        ).update(is_fixed=True)
        
        # Step 3: Completed (80-100%)
        debug_session.status = 'completed'
        debug_session.progress = 100
        debug_session.completed_at = timezone.now()
        debug_session.save()
        
        # Update user usage stats
        usage = UserUsage.objects.get(user=debug_session.user)
        usage.successful_debugs += 1
        usage.save()
        
        async_to_sync(channel_layer.group_send)(
            f'debug_{session_id}',
            {
                'type': 'debug_complete',
                'session_id': str(debug_session.id),
                'total_issues': analysis_results['total_issues_found'],
                'fixed_files': len(fixed_files)
            }
        )
        
        logger.info(f"Debug session {session_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Debug failed for {session_id}: {str(e)}")
        
        try:
            debug_session = DebugSession.objects.get(id=session_id)
            debug_session.status = 'failed'
            debug_session.error_message = str(e)
            debug_session.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'debug_{session_id}',
                {
                    'type': 'debug_error',
                    'error': str(e)
                }
            )
        except Exception as inner_e:
            logger.error(f"Error handling debug failure: {str(inner_e)}")


@shared_task
def cleanup_old_projects():
    """
    Celery task to clean up old failed/abandoned projects
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    
    old_projects = Project.objects.filter(
        status__in=['failed', 'pending'],
        created_at__lt=cutoff_date
    )
    
    count = old_projects.count()
    old_projects.delete()
    
    logger.info(f"Cleaned up {count} old projects")
    return count

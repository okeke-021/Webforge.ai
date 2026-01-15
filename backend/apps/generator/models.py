from django.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analyzing', 'Analyzing Requirements'),
        ('planning', 'Planning Architecture'),
        ('generating', 'Generating Code'),
        ('validating', 'Validating Code'),
        ('packaging', 'Packaging Files'),
        ('completed', 'Completed'),
        ('draft', 'Draft - Awaiting User Review'),  # NEW
        ('refining', 'Refining Features'),  # NEW
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    features = models.JSONField(default=list)
    tech_stack = models.JSONField(default=dict)
    style_preferences = models.JSONField(default=dict)
    
    specifications = models.JSONField(null=True, blank=True)
    generated_files = models.JSONField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)
    
    # NEW: Track refinement iterations
    is_draft = models.BooleanField(default=True)
    iteration_count = models.IntegerField(default=1)
    
    github_repo_url = models.URLField(null=True, blank=True)
    preview_url = models.URLField(null=True, blank=True)
    
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)  # NEW
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_draft']),  # NEW
        ]
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    @property
    def duration(self):
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None


class ProjectRefinement(models.Model):
    """
    Tracks iterative refinements to a project
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='refinements')
    
    iteration_number = models.IntegerField()
    
    # What user requested
    requested_features = models.JSONField(default=list)
    requested_changes = models.TextField()
    change_type = models.CharField(max_length=50, choices=[
        ('add_feature', 'Add Feature'),
        ('modify_feature', 'Modify Feature'),
        ('remove_feature', 'Remove Feature'),
        ('change_style', 'Change Style'),
        ('fix_issue', 'Fix Issue'),
        ('other', 'Other')
    ])
    
    # Results
    previous_files = models.JSONField(null=True, blank=True)
    updated_files = models.JSONField(null=True, blank=True)
    files_changed = models.JSONField(default=list)  # List of changed file paths
    
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['iteration_number']
    
    def __str__(self):
        return f"{self.project.name} - Iteration {self.iteration_number}"


class DebugSession(models.Model):
    """
    Tracks debugging sessions for existing repositories
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analyzing', 'Analyzing Code'),
        ('fixing', 'Generating Fixes'),
        ('creating_pr', 'Creating Pull Request'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debug_sessions')
    
    repo_url = models.URLField()
    repo_name = models.CharField(max_length=200)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)
    
    # Analysis results
    total_files_analyzed = models.IntegerField(default=0)
    total_issues_found = models.IntegerField(default=0)
    issues = models.JSONField(default=list)
    severity_breakdown = models.JSONField(default=dict)
    
    # Fixes
    fixed_files = models.JSONField(null=True, blank=True)
    pull_request_url = models.URLField(null=True, blank=True)
    
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Debug: {self.repo_name} - {self.user.username}"


class CodeIssue(models.Model):
    """
    Individual code issues detected during debugging
    """
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    TYPE_CHOICES = [
        ('syntax', 'Syntax Error'),
        ('logic', 'Logic Bug'),
        ('security', 'Security Vulnerability'),
        ('performance', 'Performance Issue'),
        ('style', 'Code Style'),
    ]
    
    debug_session = models.ForeignKey(DebugSession, on_delete=models.CASCADE, related_name='detected_issues')
    
    file_path = models.CharField(max_length=500)
    line_number = models.IntegerField(null=True, blank=True)
    
    issue_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    description = models.TextField()
    code_snippet = models.TextField(null=True, blank=True)
    suggestion = models.TextField()
    fixed_code = models.TextField(null=True, blank=True)
    
    is_fixed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-severity', 'file_path', 'line_number']
    
    def __str__(self):
        return f"{self.severity} - {self.file_path}:{self.line_number}"


class GenerationLog(models.Model):
    LOG_TYPES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES, default='info')
    message = models.TextField()
    details = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.project.name} - {self.log_type} - {self.timestamp}"


class UserUsage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usage')
    
    monthly_generations = models.IntegerField(default=0)
    monthly_generations_reset = models.DateTimeField(auto_now_add=True)
    
    monthly_refinements = models.IntegerField(default=0)  # NEW
    monthly_refinements_reset = models.DateTimeField(auto_now_add=True)  # NEW
    
    monthly_debugs = models.IntegerField(default=0)
    monthly_debugs_reset = models.DateTimeField(auto_now_add=True)
    
    today_requests = models.IntegerField(default=0)
    today_requests_reset = models.DateField(auto_now_add=True)
    
    total_projects = models.IntegerField(default=0)
    successful_projects = models.IntegerField(default=0)
    failed_projects = models.IntegerField(default=0)
    
    total_debug_sessions = models.IntegerField(default=0)
    successful_debugs = models.IntegerField(default=0)
    
    total_refinements = models.IntegerField(default=0)  # NEW
    
    last_generation = models.DateTimeField(null=True, blank=True)
    last_debug = models.DateTimeField(null=True, blank=True)
    last_refinement = models.DateTimeField(null=True, blank=True)  # NEW
    
    def __str__(self):
        return f"Usage for {self.user.username}"
    
    def can_generate(self, subscription_tier='free'):
        limits = {
            'free': 3,
            'pro': 10,
            'enterprise': 20
        }
        
        limit = limits.get(subscription_tier, limits['free'])
        return self.monthly_generations < limit
    
    def can_refine(self, subscription_tier='free'):
        """Check if user can refine projects"""
        limits = {
            'free': 5,  # 5 refinements per month
            'pro': 20,  # 20 refinements per month
            'enterprise': 999  # Unlimited
        }
        
        limit = limits.get(subscription_tier, limits['free'])
        return self.monthly_refinements < limit
    
    def can_debug(self, subscription_tier='free'):
        """Check if user can debug (Enterprise only)"""
        if subscription_tier != 'enterprise':
            return False
        
        # Enterprise: unlimited debugging
        return True
    
    def can_make_request(self, subscription_tier='free'):
        limits = {
            'free': 5,
            'pro': 20,
            'enterprise': 50
        }
        
        limit = limits.get(subscription_tier, limits['free'])
        return self.today_requests < limit

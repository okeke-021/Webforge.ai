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
    
    github_repo_url = models.URLField(null=True, blank=True)
    preview_url = models.URLField(null=True, blank=True)
    
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
        return f"{self.name} - {self.user.username}"
    
    @property
    def duration(self):
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None


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
    
    today_requests = models.IntegerField(default=0)
    today_requests_reset = models.DateField(auto_now_add=True)
    
    total_projects = models.IntegerField(default=0)
    successful_projects = models.IntegerField(default=0)
    failed_projects = models.IntegerField(default=0)
    
    last_generation = models.DateTimeField(null=True, blank=True)
    
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
    
    def can_make_request(self, subscription_tier='free'):
        limits = {
            'free': 5,
            'pro': 20,
            'enterprise': 50
        }
        
        limit = limits.get(subscription_tier, limits['free'])
        return self.today_requests < limit

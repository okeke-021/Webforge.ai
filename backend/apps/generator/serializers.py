from rest_framework import serializers
from .models import Project, DebugSession, CodeIssue, GenerationLog


class ProjectCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a new project
    """
    name = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(min_length=50, max_length=2000)
    features = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    tech_stack = serializers.DictField(required=False, default=dict)
    style_preferences = serializers.DictField(required=False, default=dict)
    
    def validate_description(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError(
                "Description must be at least 50 characters long"
            )
        return value.strip()
    
    def validate_tech_stack(self, value):
        required_fields = ['frontend', 'backend', 'database']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(
                    f"Tech stack must include {field}"
                )
        return value


class GenerationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for generation logs
    """
    class Meta:
        model = GenerationLog
        fields = ['timestamp', 'log_type', 'message', 'details']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for project details
    """
    logs = GenerationLogSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'features',
            'tech_stack',
            'style_preferences',
            'specifications',
            'generated_files',
            'status',
            'progress',
            'github_repo_url',
            'preview_url',
            'error_message',
            'created_at',
            'updated_at',
            'completed_at',
            'duration',
            'logs'
        ]
        read_only_fields = [
            'id',
            'specifications',
            'generated_files',
            'status',
            'progress',
            'github_repo_url',
            'preview_url',
            'error_message',
            'created_at',
            'updated_at',
            'completed_at'
        ]
    
    def get_duration(self, obj):
        return obj.duration


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for project lists
    """
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'status',
            'progress',
            'created_at',
            'tech_stack'
        ]


class CodeIssueSerializer(serializers.ModelSerializer):
    """
    Serializer for code issues
    """
    class Meta:
        model = CodeIssue
        fields = [
            'id',
            'file_path',
            'line_number',
            'issue_type',
            'severity',
            'description',
            'code_snippet',
            'suggestion',
            'fixed_code',
            'is_fixed',
            'created_at'
        ]


class DebugSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for debug sessions
    """
    detected_issues = CodeIssueSerializer(many=True, read_only=True)
    
    class Meta:
        model = DebugSession
        fields = [
            'id',
            'repo_url',
            'repo_name',
            'status',
            'progress',
            'total_files_analyzed',
            'total_issues_found',
            'issues',
            'severity_breakdown',
            'fixed_files',
            'pull_request_url',
            'error_message',
            'created_at',
            'updated_at',
            'completed_at',
            'detected_issues'
        ]
        read_only_fields = [
            'id',
            'repo_name',
            'status',
            'progress',
            'total_files_analyzed',
            'total_issues_found',
            'issues',
            'severity_breakdown',
            'fixed_files',
            'pull_request_url',
            'error_message',
            'created_at',
            'updated_at',
            'completed_at'
        ]

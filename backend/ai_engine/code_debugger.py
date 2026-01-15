"""
AI-Powered Code Debugger
Analyzes existing code, detects bugs, and suggests fixes
"""

import google.generativeai as genai
from django.conf import settings
from github import Github
from typing import Dict, List, Any
import json
import re

genai.configure(api_key=settings.GEMINI_API_KEY)


class CodeDebugger:
    """
    Analyzes code from GitHub repositories and suggests fixes
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyze_repository(self, repo_url: str, github_token: str) -> Dict[str, Any]:
        """
        Analyze entire repository for bugs and issues
        
        Args:
            repo_url: GitHub repository URL
            github_token: GitHub access token
            
        Returns:
            Analysis results with detected issues
        """
        
        g = Github(github_token)
        
        # Extract owner and repo name from URL
        parts = repo_url.rstrip('/').split('/')
        owner, repo_name = parts[-2], parts[-1]
        
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        # Get all files
        contents = self._get_all_files(repo)
        
        # Analyze each file
        all_issues = []
        for file_path, file_content in contents.items():
            if self._should_analyze(file_path):
                issues = self._analyze_file(file_path, file_content)
                if issues:
                    all_issues.extend(issues)
        
        return {
            'repository': repo_url,
            'total_files_analyzed': len(contents),
            'total_issues_found': len(all_issues),
            'issues': all_issues,
            'severity_breakdown': self._categorize_severity(all_issues)
        }
    
    def analyze_file(self, file_path: str, file_content: str) -> List[Dict[str, Any]]:
        """
        Analyze a single file for bugs
        
        Args:
            file_path: Path to the file
            file_content: Content of the file
            
        Returns:
            List of detected issues
        """
        
        return self._analyze_file(file_path, file_content)
    
    def _analyze_file(self, file_path: str, file_content: str) -> List[Dict[str, Any]]:
        """Analyze file using Gemini"""
        
        prompt = f"""Analyze this code file for bugs, errors, and code quality issues.

FILE: {file_path}

CODE:
```
{file_content}
```

Identify:
1. Syntax errors
2. Logic bugs
3. Security vulnerabilities
4. Performance issues
5. Code smells
6. Best practice violations

For EACH issue found, provide:
- Line number (approximate)
- Issue type (syntax/logic/security/performance/style)
- Severity (critical/high/medium/low)
- Description
- Suggested fix

Return ONLY a JSON array of issues:
[
  {{
    "line": 42,
    "type": "security",
    "severity": "high",
    "description": "SQL injection vulnerability",
    "suggestion": "Use parameterized queries instead of string concatenation",
    "code_snippet": "the problematic code",
    "fixed_code": "the corrected code"
  }}
]

If no issues found, return empty array: []"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,
                    'max_output_tokens': 4096,
                }
            )
            
            issues_text = response.text.strip()
            
            # Clean markdown formatting
            if issues_text.startswith('```json'):
                issues_text = issues_text[7:]
            if issues_text.endswith('```'):
                issues_text = issues_text[:-3]
            issues_text = issues_text.strip()
            
            issues = json.loads(issues_text)
            
            # Add file path to each issue
            for issue in issues:
                issue['file'] = file_path
            
            return issues
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse issues for {file_path}: {str(e)}")
            return []
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")
            return []
    
    def generate_fixes(self, issues: List[Dict[str, Any]], 
                      repo_files: Dict[str, str]) -> Dict[str, str]:
        """
        Generate fixed versions of files with issues
        
        Args:
            issues: List of detected issues
            repo_files: Original file contents
            
        Returns:
            Dictionary mapping file paths to fixed contents
        """
        
        fixed_files = {}
        
        # Group issues by file
        issues_by_file = {}
        for issue in issues:
            file_path = issue['file']
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        # Fix each file
        for file_path, file_issues in issues_by_file.items():
            if file_path not in repo_files:
                continue
            
            original_content = repo_files[file_path]
            fixed_content = self._fix_file(file_path, original_content, file_issues)
            
            if fixed_content and fixed_content != original_content:
                fixed_files[file_path] = fixed_content
        
        return fixed_files
    
    def _fix_file(self, file_path: str, content: str, 
                  issues: List[Dict[str, Any]]) -> str:
        """Fix a single file based on detected issues"""
        
        issues_text = json.dumps(issues, indent=2)
        
        prompt = f"""Fix the following code file based on the detected issues.

FILE: {file_path}

ORIGINAL CODE:
```
{content}
```

ISSUES TO FIX:
{issues_text}

Generate the COMPLETE fixed version of the file with all issues resolved.
Return ONLY the fixed code, no explanations or markdown formatting."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.2,
                    'max_output_tokens': 8192,
                }
            )
            
            fixed_code = response.text.strip()
            
            # Remove markdown code blocks if present
            if fixed_code.startswith('```'):
                lines = fixed_code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                fixed_code = '\n'.join(lines)
            
            return fixed_code
            
        except Exception as e:
            print(f"Error fixing {file_path}: {str(e)}")
            return content
    
    def create_pull_request(self, repo_url: str, github_token: str,
                           fixed_files: Dict[str, str], 
                           issues: List[Dict[str, Any]]) -> str:
        """
        Create a pull request with fixes
        
        Args:
            repo_url: GitHub repository URL
            github_token: GitHub access token
            fixed_files: Dictionary of fixed file contents
            issues: List of issues that were fixed
            
        Returns:
            Pull request URL
        """
        
        g = Github(github_token)
        
        # Extract owner and repo name
        parts = repo_url.rstrip('/').split('/')
        owner, repo_name = parts[-2], parts[-1]
        
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        # Get default branch
        default_branch = repo.default_branch
        base_sha = repo.get_branch(default_branch).commit.sha
        
        # Create new branch
        branch_name = f"webforge-ai-fixes-{base_sha[:7]}"
        try:
            repo.create_git_ref(f"refs/heads/{branch_name}", base_sha)
        except:
            # Branch might already exist
            pass
        
        # Commit fixes
        commit_message = self._generate_commit_message(issues)
        
        for file_path, new_content in fixed_files.items():
            try:
                # Get file to update
                contents = repo.get_contents(file_path, ref=branch_name)
                repo.update_file(
                    path=file_path,
                    message=f"Fix issues in {file_path}",
                    content=new_content,
                    sha=contents.sha,
                    branch=branch_name
                )
            except:
                # File might not exist yet
                repo.create_file(
                    path=file_path,
                    message=f"Add fixed {file_path}",
                    content=new_content,
                    branch=branch_name
                )
        
        # Create pull request
        pr_body = self._generate_pr_body(issues)
        pr = repo.create_pull(
            title="🤖 WebForge.ai: Automated Bug Fixes",
            body=pr_body,
            head=branch_name,
            base=default_branch
        )
        
        return pr.html_url
    
    def _get_all_files(self, repo) -> Dict[str, str]:
        """Recursively get all files from repository"""
        
        files = {}
        
        def get_tree_files(path=""):
            contents = repo.get_contents(path)
            
            for content in contents:
                if content.type == "dir":
                    get_tree_files(content.path)
                else:
                    try:
                        file_content = content.decoded_content.decode('utf-8')
                        files[content.path] = file_content
                    except:
                        # Skip binary files
                        pass
        
        get_tree_files()
        return files
    
    def _should_analyze(self, file_path: str) -> bool:
        """Check if file should be analyzed"""
        
        # File extensions to analyze
        analyzable_extensions = [
            '.js', '.jsx', '.ts', '.tsx',
            '.py', '.vue', '.html', '.css',
            '.java', '.go', '.rb', '.php'
        ]
        
        # Skip patterns
        skip_patterns = [
            'node_modules/', 'venv/', '.git/', 'dist/', 'build/',
            '__pycache__/', '.next/', 'coverage/', 'package-lock.json',
            'yarn.lock', '.min.js', '.min.css'
        ]
        
        # Check if should skip
        for pattern in skip_patterns:
            if pattern in file_path:
                return False
        
        # Check extension
        return any(file_path.endswith(ext) for ext in analyzable_extensions)
    
    def _categorize_severity(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize issues by severity"""
        
        severity_count = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for issue in issues:
            severity = issue.get('severity', 'medium').lower()
            if severity in severity_count:
                severity_count[severity] += 1
        
        return severity_count
    
    def _generate_commit_message(self, issues: List[Dict[str, Any]]) -> str:
        """Generate commit message"""
        
        critical_count = sum(1 for i in issues if i.get('severity') == 'critical')
        high_count = sum(1 for i in issues if i.get('severity') == 'high')
        
        return f"Fix {len(issues)} issues ({critical_count} critical, {high_count} high priority)"
    
    def _generate_pr_body(self, issues: List[Dict[str, Any]]) -> str:
        """Generate pull request body"""
        
        body = ["## 🤖 Automated Bug Fixes by WebForge.ai\n"]
        body.append(f"This PR fixes **{len(issues)} issues** detected in your codebase.\n")
        
        # Group by severity
        critical = [i for i in issues if i.get('severity') == 'critical']
        high = [i for i in issues if i.get('severity') == 'high']
        medium = [i for i in issues if i.get('severity') == 'medium']
        low = [i for i in issues if i.get('severity') == 'low']
        
        if critical:
            body.append(f"### 🔴 Critical Issues ({len(critical)})\n")
            for issue in critical[:5]:
                body.append(f"- **{issue['file']}:{issue.get('line', '?')}** - {issue['description']}\n")
        
        if high:
            body.append(f"\n### 🟠 High Priority Issues ({len(high)})\n")
            for issue in high[:5]:
                body.append(f"- **{issue['file']}:{issue.get('line', '?')}** - {issue['description']}\n")
        
        if medium:
            body.append(f"\n### 🟡 Medium Priority Issues ({len(medium)})\n")
            for issue in medium[:5]:
                body.append(f"- **{issue['file']}:{issue.get('line', '?')}** - {issue['description']}\n")
        
        body.append("\n---\n")
        body.append("*Generated by [WebForge.ai](https://webforge.ai) - AI-Powered Code Analysis & Debugging*")
        
        return ''.join(body)

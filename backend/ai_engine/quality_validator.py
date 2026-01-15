"""
Quality Validator for Generated Code
Validates syntax, security, and code quality
"""

import subprocess
import tempfile
import os
from typing import Dict, List, Any
import ast
import json

class QualityValidator:
    """
    Validates generated code for quality, security, and correctness
    """
    
    def __init__(self):
        self.validation_results = {
            'syntax_valid': True,
            'security_issues': [],
            'quality_issues': [],
            'passed': False,
            'errors': []
        }
    
    def validate_project(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate all project files
        
        Args:
            files: Dictionary mapping file paths to file contents
            
        Returns:
            Validation results
        """
        
        results = {
            'overall_valid': True,
            'files_validated': 0,
            'files_passed': 0,
            'issues': []
        }
        
        for filepath, content in files.items():
            file_result = self._validate_file(filepath, content)
            
            results['files_validated'] += 1
            
            if file_result['passed']:
                results['files_passed'] += 1
            else:
                results['overall_valid'] = False
                results['issues'].append({
                    'file': filepath,
                    'issues': file_result['issues']
                })
        
        return results
    
    def _validate_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """Validate a single file"""
        
        result = {
            'passed': True,
            'issues': []
        }
        
        file_ext = os.path.splitext(filepath)[1]
        
        if file_ext == '.py':
            result.update(self._validate_python(content))
        elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
            result.update(self._validate_javascript(content))
        elif file_ext == '.vue':
            result.update(self._validate_vue(content))
        
        return result
    
    def _validate_python(self, code: str) -> Dict[str, Any]:
        """Validate Python code"""
        
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'message': str(e),
                'line': e.lineno
            })
        
        security_issues = self._check_python_security(code)
        issues.extend(security_issues)
        
        quality_issues = self._check_python_quality(code)
        issues.extend(quality_issues)
        
        return {
            'passed': len([i for i in issues if i['type'] == 'syntax_error']) == 0,
            'issues': issues
        }
    
    def _validate_javascript(self, code: str) -> Dict[str, Any]:
        """Validate JavaScript/TypeScript code"""
        
        issues = []
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            result = subprocess.run(
                ['node', '--check', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                issues.append({
                    'type': 'syntax_error',
                    'message': result.stderr
                })
            
            os.unlink(temp_path)
            
        except subprocess.TimeoutExpired:
            issues.append({
                'type': 'validation_timeout',
                'message': 'Validation timed out'
            })
        except Exception as e:
            issues.append({
                'type': 'validation_error',
                'message': str(e)
            })
        
        security_issues = self._check_javascript_security(code)
        issues.extend(security_issues)
        
        return {
            'passed': len([i for i in issues if i['type'] == 'syntax_error']) == 0,
            'issues': issues
        }
    
    def _validate_vue(self, code: str) -> Dict[str, Any]:
        """Validate Vue component"""
        
        issues = []
        
        if '<template>' not in code:
            issues.append({
                'type': 'structure_error',
                'message': 'Missing <template> section'
            })
        
        if '<script' not in code:
            issues.append({
                'type': 'structure_error',
                'message': 'Missing <script> section'
            })
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _check_python_security(self, code: str) -> List[Dict[str, Any]]:
        """Check Python code for security issues"""
        
        issues = []
        
        dangerous_patterns = [
            ('eval(', 'Use of eval() is dangerous'),
            ('exec(', 'Use of exec() is dangerous'),
            ('__import__', 'Dynamic imports can be dangerous'),
            ('pickle.loads', 'Pickle deserialization can be dangerous'),
            ('os.system(', 'Use subprocess instead of os.system'),
        ]
        
        for pattern, message in dangerous_patterns:
            if pattern in code:
                issues.append({
                    'type': 'security_warning',
                    'message': message,
                    'severity': 'high'
                })
        
        if 'password' in code.lower() and '=' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'password' in line.lower() and '=' in line and not line.strip().startswith('#'):
                    if '"' in line or "'" in line:
                        issues.append({
                            'type': 'security_warning',
                            'message': 'Possible hardcoded password',
                            'line': i,
                            'severity': 'critical'
                        })
        
        return issues
    
    def _check_javascript_security(self, code: str) -> List[Dict[str, Any]]:
        """Check JavaScript code for security issues"""
        
        issues = []
        
        dangerous_patterns = [
            ('eval(', 'Use of eval() is dangerous'),
            ('innerHTML =', 'innerHTML can lead to XSS, use textContent'),
            ('dangerouslySetInnerHTML', 'Ensure content is sanitized'),
            ('document.write(', 'document.write() is deprecated and unsafe'),
        ]
        
        for pattern, message in dangerous_patterns:
            if pattern in code:
                issues.append({
                    'type': 'security_warning',
                    'message': message,
                    'severity': 'high'
                })
        
        return issues
    
    def _check_python_quality(self, code: str) -> List[Dict[str, Any]]:
        """Check Python code quality"""
        
        issues = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    'type': 'quality_warning',
                    'message': f'Line {i} exceeds 120 characters',
                    'severity': 'low'
                })
        
        if 'try:' in code and 'except:' in code:
            if 'except Exception' not in code and 'except BaseException' not in code:
                bare_except_count = code.count('except:')
                if bare_except_count > 0:
                    issues.append({
                        'type': 'quality_warning',
                        'message': 'Bare except clause found, specify exception type',
                        'severity': 'medium'
                    })
        
        return issues
    
    def run_security_scan(self, project_path: str) -> Dict[str, Any]:
        """
        Run Bandit security scanner on Python files
        
        Args:
            project_path: Path to project directory
            
        Returns:
            Security scan results
        """
        
        try:
            result = subprocess.run(
                ['bandit', '-r', project_path, '-f', 'json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                scan_results = json.loads(result.stdout)
                return {
                    'passed': len(scan_results.get('results', [])) == 0,
                    'issues': scan_results.get('results', []),
                    'metrics': scan_results.get('metrics', {})
                }
            
        except subprocess.TimeoutExpired:
            return {
                'passed': False,
                'error': 'Security scan timed out'
            }
        except Exception as e:
            return {
                'passed': False,
                'error': str(e)
            }
        
        return {'passed': True, 'issues': []}
    
    def run_linting(self, filepath: str) -> Dict[str, Any]:
        """
        Run linting on file
        
        Args:
            filepath: Path to file
            
        Returns:
            Linting results
        """
        
        file_ext = os.path.splitext(filepath)[1]
        
        if file_ext == '.py':
            return self._run_pylint(filepath)
        elif file_ext in ['.js', '.jsx']:
            return self._run_eslint(filepath)
        
        return {'passed': True, 'issues': []}
    
    def _run_pylint(self, filepath: str) -> Dict[str, Any]:
        """Run Pylint on Python file"""
        
        try:
            result = subprocess.run(
                ['pylint', filepath, '--output-format=json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                issues = json.loads(result.stdout)
                return {
                    'passed': len([i for i in issues if i['type'] == 'error']) == 0,
                    'issues': issues
                }
                
        except Exception as e:
            return {'passed': True, 'error': str(e)}
        
        return {'passed': True, 'issues': []}
    
    def _run_eslint(self, filepath: str) -> Dict[str, Any]:
        """Run ESLint on JavaScript file"""
        
        try:
            result = subprocess.run(
                ['eslint', filepath, '--format=json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                results = json.loads(result.stdout)
                all_issues = []
                for file_result in results:
                    all_issues.extend(file_result.get('messages', []))
                
                return {
                    'passed': len([i for i in all_issues if i['severity'] == 2]) == 0,
                    'issues': all_issues
                }
                
        except Exception as e:
            return {'passed': True, 'error': str(e)}
        
        return {'passed': True, 'issues': []}
    
    def generate_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate human-readable validation report"""
        
        report_lines = [
            "=== Code Quality Validation Report ===",
            "",
            f"Files Validated: {validation_results['files_validated']}",
            f"Files Passed: {validation_results['files_passed']}",
            f"Overall Status: {'✓ PASSED' if validation_results['overall_valid'] else '✗ FAILED'}",
            ""
        ]
        
        if validation_results['issues']:
            report_lines.append("Issues Found:")
            report_lines.append("")
            
            for issue_group in validation_results['issues']:
                report_lines.append(f"File: {issue_group['file']}")
                
                for issue in issue_group['issues']:
                    severity = issue.get('severity', 'medium')
                    icon = '🔴' if severity == 'critical' else '🟡' if severity == 'high' else '🟢'
                    report_lines.append(f"  {icon} [{issue['type']}] {issue['message']}")
                
                report_lines.append("")
        
        return '\n'.join(report_lines)

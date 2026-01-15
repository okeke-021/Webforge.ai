"""
Project Refinement Engine
Handles iterative improvements to generated projects
"""

import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Any
import json

genai.configure(api_key=settings.GEMINI_API_KEY)


class ProjectRefiner:
    """
    Refines existing projects based on user feedback
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def refine_project(self, 
                      current_files: Dict[str, str],
                      current_specs: Dict[str, Any],
                      requested_features: List[str],
                      requested_changes: str) -> Dict[str, Any]:
        """
        Refine project with new features or changes
        
        Args:
            current_files: Current project files
            current_specs: Current project specifications
            requested_features: List of new features to add
            requested_changes: Description of changes
            
        Returns:
            Dictionary with updated files and specifications
        """
        
        # Analyze what needs to change
        analysis = self._analyze_changes(
            current_specs,
            requested_features,
            requested_changes
        )
        
        # Generate updated files
        updated_files = self._generate_updated_files(
            current_files,
            analysis,
            requested_features
        )
        
        # Update specifications
        updated_specs = self._update_specifications(
            current_specs,
            analysis,
            requested_features
        )
        
        return {
            'updated_files': updated_files,
            'updated_specs': updated_specs,
            'files_changed': list(updated_files.keys()),
            'analysis': analysis
        }
    
    def _analyze_changes(self,
                        current_specs: Dict[str, Any],
                        requested_features: List[str],
                        requested_changes: str) -> Dict[str, Any]:
        """Analyze what needs to be changed"""
        
        prompt = f"""Analyze the requested changes to this project.

CURRENT PROJECT:
{json.dumps(current_specs, indent=2)}

REQUESTED FEATURES:
{json.dumps(requested_features, indent=2)}

USER REQUEST:
{requested_changes}

Determine:
1. Which files need to be modified
2. Which new files need to be created
3. Which features need to be added to existing components
4. What dependencies need to be added

Return ONLY JSON:
{{
  "files_to_modify": ["path/to/file1.js", "path/to/file2.py"],
  "files_to_create": ["path/to/newfile.js"],
  "features_to_add": [
    {{
      "feature": "authentication",
      "components_affected": ["Login.vue", "api/auth.py"],
      "new_dependencies": ["bcrypt", "jsonwebtoken"]
    }}
  ],
  "complexity": "low|medium|high",
  "estimated_changes": "Brief description"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'max_output_tokens': 2048,
                }
            )
            
            analysis_text = response.text.strip()
            
            # Clean JSON
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            
            return json.loads(analysis_text.strip())
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")
            return {
                'files_to_modify': [],
                'files_to_create': [],
                'features_to_add': [],
                'complexity': 'unknown',
                'estimated_changes': 'Unable to analyze'
            }
    
    def _generate_updated_files(self,
                                current_files: Dict[str, str],
                                analysis: Dict[str, Any],
                                requested_features: List[str]) -> Dict[str, str]:
        """Generate updated versions of files"""
        
        updated_files = {}
        
        # Modify existing files
        for file_path in analysis.get('files_to_modify', []):
            if file_path in current_files:
                updated_content = self._update_file(
                    file_path,
                    current_files[file_path],
                    analysis,
                    requested_features
                )
                if updated_content:
                    updated_files[file_path] = updated_content
        
        # Create new files
        for file_path in analysis.get('files_to_create', []):
            new_content = self._create_new_file(
                file_path,
                analysis,
                requested_features
            )
            if new_content:
                updated_files[file_path] = new_content
        
        return updated_files
    
    def _update_file(self,
                    file_path: str,
                    current_content: str,
                    analysis: Dict[str, Any],
                    requested_features: List[str]) -> str:
        """Update an existing file with new features"""
        
        relevant_features = [
            f for f in analysis.get('features_to_add', [])
            if file_path in f.get('components_affected', [])
        ]
        
        prompt = f"""Update this file to add the requested features.

FILE: {file_path}

CURRENT CODE:
```
{current_content}
```

FEATURES TO ADD:
{json.dumps(relevant_features, indent=2)}

REQUESTED FEATURES:
{json.dumps(requested_features, indent=2)}

Requirements:
1. Preserve all existing functionality
2. Add new features seamlessly
3. Follow existing code style
4. Add necessary imports
5. Include error handling
6. Add comments for new code

Return ONLY the complete updated file code, no explanations."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.4,
                    'max_output_tokens': 8192,
                }
            )
            
            updated_code = response.text.strip()
            
            # Remove markdown formatting
            if updated_code.startswith('```'):
                lines = updated_code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                updated_code = '\n'.join(lines)
            
            return updated_code
            
        except Exception as e:
            print(f"Failed to update {file_path}: {str(e)}")
            return current_content
    
    def _create_new_file(self,
                        file_path: str,
                        analysis: Dict[str, Any],
                        requested_features: List[str]) -> str:
        """Create a new file for added features"""
        
        prompt = f"""Create a new file for the requested features.

FILE PATH: {file_path}

REQUESTED FEATURES:
{json.dumps(requested_features, indent=2)}

ANALYSIS:
{json.dumps(analysis, indent=2)}

Generate complete, production-ready code for this file.
Include:
1. All necessary imports
2. Proper structure
3. Error handling
4. Comments
5. Best practices

Return ONLY the file code, no explanations."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.4,
                    'max_output_tokens': 4096,
                }
            )
            
            code = response.text.strip()
            
            # Remove markdown formatting
            if code.startswith('```'):
                lines = code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                code = '\n'.join(lines)
            
            return code
            
        except Exception as e:
            print(f"Failed to create {file_path}: {str(e)}")
            return ""
    
    def _update_specifications(self,
                              current_specs: Dict[str, Any],
                              analysis: Dict[str, Any],
                              requested_features: List[str]) -> Dict[str, Any]:
        """Update project specifications with new features"""
        
        updated_specs = current_specs.copy()
        
        # Add new features to specs
        if 'features_breakdown' not in updated_specs:
            updated_specs['features_breakdown'] = []
        
        for feature in requested_features:
            if not any(f.get('feature') == feature for f in updated_specs['features_breakdown']):
                updated_specs['features_breakdown'].append({
                    'feature': feature,
                    'components_required': [],
                    'complexity': analysis.get('complexity', 'medium')
                })
        
        # Update file structure
        if 'file_structure' not in updated_specs:
            updated_specs['file_structure'] = []
        
        for new_file in analysis.get('files_to_create', []):
            if not any(f.get('path') == new_file for f in updated_specs['file_structure']):
                updated_specs['file_structure'].append({
                    'path': new_file,
                    'type': self._infer_file_type(new_file),
                    'purpose': f"Added for {', '.join(requested_features)}"
                })
        
        return updated_specs
    
    def _infer_file_type(self, file_path: str) -> str:
        """Infer file type from path"""
        
        if 'component' in file_path.lower() or file_path.endswith('.vue'):
            return 'component'
        elif 'api' in file_path.lower() or 'views' in file_path.lower():
            return 'api'
        elif 'model' in file_path.lower():
            return 'model'
        elif 'config' in file_path.lower():
            return 'config'
        elif 'test' in file_path.lower():
            return 'test'
        else:
            return 'other'
    
    def suggest_features(self, current_specs: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest additional features that would complement the project"""
        
        prompt = f"""Based on this project, suggest 5 complementary features that would enhance it.

PROJECT:
{json.dumps(current_specs, indent=2)}

Suggest features that:
1. Are commonly needed with these existing features
2. Would improve user experience
3. Are technically feasible to add
4. Follow modern best practices

Return ONLY JSON array:
[
  {{
    "feature": "Feature name",
    "description": "What it does",
    "benefit": "Why it's useful",
    "complexity": "low|medium|high"
  }}
]"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'max_output_tokens': 2048,
                }
            )
            
            suggestions_text = response.text.strip()
            
            # Clean JSON
            if suggestions_text.startswith('```json'):
                suggestions_text = suggestions_text[7:]
            if suggestions_text.endswith('```'):
                suggestions_text = suggestions_text[:-3]
            
            return json.loads(suggestions_text.strip())
            
        except Exception as e:
            print(f"Failed to suggest features: {str(e)}")
            return []

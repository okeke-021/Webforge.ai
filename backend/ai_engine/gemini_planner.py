import json
import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Any

genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiPlanner:
    """
    Analyzes user requirements using Google Gemini Flash 2.5
    and creates detailed technical specifications
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def analyze_requirements(self, description: str, features: List[str], 
                           tech_stack: Dict[str, str], 
                           style_preferences: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze user requirements and generate technical specifications
        """
        
        prompt = self._build_analysis_prompt(description, features, tech_stack, style_preferences)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192,
                }
            )
            
            specs = self._parse_specifications(response.text)
            return specs
            
        except Exception as e:
            raise Exception(f"Gemini analysis failed: {str(e)}")
    
    def _build_analysis_prompt(self, description: str, features: List[str],
                               tech_stack: Dict[str, str], 
                               style_preferences: Dict[str, str]) -> str:
        """Build comprehensive prompt for Gemini"""
        
        return f"""You are an expert software architect. Analyze the following web application requirements and create detailed technical specifications.

USER DESCRIPTION:
{description}

REQUESTED FEATURES:
{json.dumps(features, indent=2)}

TECH STACK:
{json.dumps(tech_stack, indent=2)}

STYLE PREFERENCES:
{json.dumps(style_preferences, indent=2)}

Generate a comprehensive technical specification in JSON format with the following structure:

{{
  "project_name": "kebab-case-name",
  "description": "Brief project description",
  "architecture": {{
    "frontend": {{
      "framework": "selected framework",
      "key_libraries": ["library1", "library2"],
      "components": [
        {{
          "name": "ComponentName",
          "purpose": "what it does",
          "dependencies": ["dep1", "dep2"]
        }}
      ]
    }},
    "backend": {{
      "framework": "selected framework",
      "key_libraries": ["library1", "library2"],
      "api_endpoints": [
        {{
          "method": "GET/POST/etc",
          "path": "/api/endpoint",
          "purpose": "what it does",
          "auth_required": true/false
        }}
      ],
      "models": [
        {{
          "name": "ModelName",
          "fields": [{{"name": "field", "type": "type"}}],
          "relationships": []
        }}
      ]
    }},
    "database": {{
      "type": "postgresql/mongodb/etc",
      "tables": [
        {{
          "name": "table_name",
          "columns": [{{"name": "col", "type": "type", "constraints": []}}],
          "indexes": []
        }}
      ]
    }}
  }},
  "file_structure": [
    {{
      "path": "relative/path/to/file",
      "type": "component/api/model/config/test",
      "purpose": "file purpose",
      "dependencies": []
    }}
  ],
  "features_breakdown": [
    {{
      "feature": "feature name",
      "components_required": ["Component1", "Component2"],
      "api_endpoints_required": ["/api/endpoint1"],
      "complexity": "low/medium/high"
    }}
  ],
  "security_considerations": [
    "security point 1",
    "security point 2"
  ],
  "deployment_requirements": {{
    "environment_variables": ["VAR1", "VAR2"],
    "services": ["service1", "service2"],
    "build_steps": ["step1", "step2"]
  }}
}}

Provide only valid JSON, no markdown formatting."""

    def _parse_specifications(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured specifications"""
        
        try:
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            specs = json.loads(cleaned)
            
            self._validate_specifications(specs)
            
            return specs
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Gemini response: {str(e)}")
    
    def _validate_specifications(self, specs: Dict[str, Any]) -> None:
        """Validate that specifications contain required fields"""
        
        required_fields = ['project_name', 'architecture', 'file_structure']
        
        for field in required_fields:
            if field not in specs:
                raise ValueError(f"Missing required field: {field}")
        
        if 'frontend' not in specs['architecture']:
            raise ValueError("Missing frontend architecture")
        
        if 'backend' not in specs['architecture']:
            raise ValueError("Missing backend architecture")
    
    def refine_component(self, component_name: str, specs: Dict[str, Any]) -> Dict[str, Any]:
        """Refine specific component details"""
        
        prompt = f"""Given the following technical specifications, provide detailed implementation 
guidance for the {component_name} component.

SPECIFICATIONS:
{json.dumps(specs, indent=2)}

Provide implementation details including:
1. Exact code structure
2. Required imports
3. Props/state management
4. Event handlers
5. Styling approach
6. Edge cases to handle

Return as JSON with 'implementation_details' key."""

        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}

import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Any
import json
from .pattern_retriever import PatternRetriever

genai.configure(api_key=settings.GEMINI_API_KEY)

class CodeGenerator:
    """
    Generates complete code files from specifications and patterns
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.pattern_retriever = PatternRetriever()
    
    def generate_project_files(self, specs: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate all project files from specifications
        
        Returns:
            Dictionary mapping file paths to file contents
        """
        
        files = {}
        
        frontend_framework = specs['architecture']['frontend']['framework']
        backend_framework = specs['architecture']['backend']['framework']
        
        for file_spec in specs['file_structure']:
            try:
                content = self._generate_file(file_spec, specs, frontend_framework, backend_framework)
                files[file_spec['path']] = content
            except Exception as e:
                print(f"Error generating {file_spec['path']}: {str(e)}")
                files[file_spec['path']] = f"// Error generating file: {str(e)}"
        
        files.update(self._generate_config_files(specs, frontend_framework, backend_framework))
        files.update(self._generate_documentation(specs))
        
        return files
    
    def _generate_file(self, file_spec: Dict[str, Any], specs: Dict[str, Any],
                      frontend_framework: str, backend_framework: str) -> str:
        """Generate content for a single file"""
        
        file_type = file_spec['type']
        framework = frontend_framework if 'frontend' in file_spec['path'] else backend_framework
        
        relevant_patterns = self.pattern_retriever.search_patterns(
            query=f"{file_spec['purpose']} {file_type}",
            framework=framework,
            pattern_type=file_type,
            top_k=3
        )
        
        prompt = self._build_file_generation_prompt(file_spec, specs, relevant_patterns, framework)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.4,
                    'max_output_tokens': 4096,
                }
            )
            
            content = self._extract_code(response.text)
            return content
            
        except Exception as e:
            raise Exception(f"Failed to generate {file_spec['path']}: {str(e)}")
    
    def _build_file_generation_prompt(self, file_spec: Dict[str, Any], 
                                     specs: Dict[str, Any],
                                     patterns: List[Dict[str, Any]],
                                     framework: str) -> str:
        """Build prompt for file generation"""
        
        patterns_text = "\n\n".join([
            f"EXAMPLE {i+1}:\n{p['code']}" 
            for i, p in enumerate(patterns)
        ]) if patterns else "No examples available"
        
        return f"""Generate production-ready code for the following file:

FILE PATH: {file_spec['path']}
FILE TYPE: {file_spec['type']}
PURPOSE: {file_spec['purpose']}
FRAMEWORK: {framework}
DEPENDENCIES: {', '.join(file_spec.get('dependencies', []))}

PROJECT SPECIFICATIONS:
{json.dumps(specs, indent=2)}

REFERENCE PATTERNS:
{patterns_text}

Generate complete, production-ready code following best practices:
1. Include all necessary imports
2. Add proper error handling
3. Include comments for complex logic
4. Follow framework conventions
5. Implement security best practices
6. Make code maintainable and testable

Return ONLY the code, no markdown formatting or explanations."""

    def _extract_code(self, response_text: str) -> str:
        """Extract code from Gemini response"""
        
        cleaned = response_text.strip()
        
        if cleaned.startswith('```'):
            lines = cleaned.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            cleaned = '\n'.join(lines)
        
        return cleaned
    
    def _generate_config_files(self, specs: Dict[str, Any], 
                              frontend_framework: str,
                              backend_framework: str) -> Dict[str, str]:
        """Generate configuration files"""
        
        configs = {}
        
        if frontend_framework == 'react':
            configs['frontend/package.json'] = self._generate_react_package_json(specs)
            configs['frontend/vite.config.js'] = self._generate_vite_config()
        elif frontend_framework == 'vue':
            configs['frontend/package.json'] = self._generate_vue_package_json(specs)
            configs['frontend/vite.config.js'] = self._generate_vite_config()
        
        if backend_framework == 'django':
            configs['backend/requirements.txt'] = self._generate_django_requirements(specs)
        elif backend_framework == 'nodejs':
            configs['backend/package.json'] = self._generate_node_package_json(specs)
        
        configs['.env.example'] = self._generate_env_template(specs)
        configs['.gitignore'] = self._generate_gitignore()
        configs['docker-compose.yml'] = self._generate_docker_compose(specs)
        
        return configs
    
    def _generate_documentation(self, specs: Dict[str, Any]) -> Dict[str, str]:
        """Generate project documentation"""
        
        docs = {}
        
        docs['README.md'] = self._generate_readme(specs)
        docs['docs/SETUP.md'] = self._generate_setup_guide(specs)
        docs['docs/API.md'] = self._generate_api_docs(specs)
        
        return docs
    
    def _generate_react_package_json(self, specs: Dict[str, Any]) -> str:
        """Generate package.json for React projects"""
        
        package = {
            "name": specs['project_name'],
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.22.0",
                "axios": "^1.6.7"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.2.1",
                "vite": "^5.1.6",
                "eslint": "^8.57.0",
                "eslint-plugin-react": "^7.33.2"
            }
        }
        
        return json.dumps(package, indent=2)
    
    def _generate_vue_package_json(self, specs: Dict[str, Any]) -> str:
        """Generate package.json for Vue projects"""
        
        package = {
            "name": specs['project_name'],
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "vue": "^3.4.21",
                "vue-router": "^4.3.0",
                "axios": "^1.6.7"
            },
            "devDependencies": {
                "@vitejs/plugin-vue": "^5.0.4",
                "vite": "^5.1.6"
            }
        }
        
        return json.dumps(package, indent=2)
    
    def _generate_vite_config(self) -> str:
        """Generate vite.config.js"""
        return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})"""

    def _generate_django_requirements(self, specs: Dict[str, Any]) -> str:
        """Generate requirements.txt for Django"""
        return """Django==4.2.11
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
gunicorn==21.2.0"""

    def _generate_node_package_json(self, specs: Dict[str, Any]) -> str:
        """Generate package.json for Node.js backend"""
        
        package = {
            "name": f"{specs['project_name']}-backend",
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.3",
                "cors": "^2.8.5",
                "dotenv": "^16.4.5"
            },
            "devDependencies": {
                "nodemon": "^3.1.0"
            }
        }
        
        return json.dumps(package, indent=2)
    
    def _generate_env_template(self, specs: Dict[str, Any]) -> str:
        """Generate .env.example"""
        
        env_vars = specs.get('deployment_requirements', {}).get('environment_variables', [])
        
        lines = ["# Environment Variables", ""]
        for var in env_vars:
            lines.append(f"{var}=")
        
        return '\n'.join(lines)
    
    def _generate_gitignore(self) -> str:
        """Generate .gitignore"""
        return """node_modules/
dist/
.env
*.log
.DS_Store
__pycache__/
*.pyc
.venv/
venv/
*.sqlite3"""

    def _generate_docker_compose(self, specs: Dict[str, Any]) -> str:
        """Generate docker-compose.yml"""
        return """version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:"""

    def _generate_readme(self, specs: Dict[str, Any]) -> str:
        """Generate README.md"""
        
        return f"""# {specs['project_name']}

{specs['description']}

## Features

{chr(10).join(['- ' + f['feature'] for f in specs.get('features_breakdown', [])])}

## Tech Stack

- Frontend: {specs['architecture']['frontend']['framework']}
- Backend: {specs['architecture']['backend']['framework']}
- Database: {specs['architecture']['database']['type']}

## Setup

See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

## API Documentation

See [docs/API.md](docs/API.md) for API endpoints documentation.

## Generated by WebForge.ai

This project was generated using WebForge.ai - AI-powered web app generator.
"""

    def _generate_setup_guide(self, specs: Dict[str, Any]) -> str:
        """Generate SETUP.md"""
        
        return f"""# Setup Guide

## Prerequisites

- Node.js 18+
- Python 3.11+ (if using Django)
- PostgreSQL 15+

## Installation

1. Clone the repository
2. Copy .env.example to .env and fill in values
3. Install dependencies:
   - Frontend: `cd frontend && npm install`
   - Backend: `cd backend && pip install -r requirements.txt`
4. Run migrations (if applicable)
5. Start development servers

## Build Steps

{chr(10).join(['- ' + step for step in specs.get('deployment_requirements', {}).get('build_steps', [])])}
"""

    def _generate_api_docs(self, specs: Dict[str, Any]) -> str:
        """Generate API.md"""
        
        endpoints = specs['architecture']['backend'].get('api_endpoints', [])
        
        lines = ["# API Documentation\n"]
        
        for ep in endpoints:
            lines.append(f"## {ep['method']} {ep['path']}\n")
            lines.append(f"{ep['purpose']}\n")
            lines.append(f"**Auth Required:** {'Yes' if ep.get('auth_required') else 'No'}\n")
        
        return '\n'.join(lines)

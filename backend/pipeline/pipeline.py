"""
Pattern Database Pipeline
Scrapes, validates, and indexes code patterns for retrieval
"""

import os
import json
from typing import List, Dict, Any
from datasets import load_dataset
from ai_engine.pattern_retriever import PatternRetriever
import requests
from bs4 import BeautifulSoup
import re

class PatternPipeline:
    """
    Pipeline for collecting and processing code patterns
    """
    
    def __init__(self):
        self.retriever = PatternRetriever()
        self.patterns = []
    
    def initialize_database(self):
        """Initialize pattern database with curated patterns"""
        
        print("Initializing pattern database...")
        
        self.load_official_templates()
        self.load_huggingface_datasets()
        self.load_framework_examples()
        
        print(f"Total patterns collected: {len(self.patterns)}")
        
        print("Adding patterns to ChromaDB...")
        self.retriever.batch_add_patterns(self.patterns)
        
        print("Pattern database initialized successfully!")
    
    def load_official_templates(self):
        """Load official framework templates"""
        
        print("Loading official framework templates...")
        
        templates = [
            # React patterns
            {
                'code': self._get_react_component_template(),
                'metadata': {
                    'framework': 'react',
                    'type': 'component',
                    'name': 'functional_component',
                    'description': 'React functional component with hooks'
                }
            },
            {
                'code': self._get_react_form_template(),
                'metadata': {
                    'framework': 'react',
                    'type': 'component',
                    'name': 'form_component',
                    'description': 'React form component with validation'
                }
            },
            # Vue patterns
            {
                'code': self._get_vue_component_template(),
                'metadata': {
                    'framework': 'vue',
                    'type': 'component',
                    'name': 'composition_api',
                    'description': 'Vue 3 component with Composition API'
                }
            },
            # Django patterns
            {
                'code': self._get_django_model_template(),
                'metadata': {
                    'framework': 'django',
                    'type': 'model',
                    'name': 'base_model',
                    'description': 'Django model with common fields'
                }
            },
            {
                'code': self._get_django_api_view_template(),
                'metadata': {
                    'framework': 'django',
                    'type': 'api',
                    'name': 'rest_api_view',
                    'description': 'Django REST Framework APIView'
                }
            },
            # Node.js patterns
            {
                'code': self._get_express_route_template(),
                'metadata': {
                    'framework': 'nodejs',
                    'type': 'api',
                    'name': 'express_route',
                    'description': 'Express.js route handler'
                }
            },
        ]
        
        self.patterns.extend(templates)
        print(f"Loaded {len(templates)} official templates")
    
    def load_huggingface_datasets(self):
        """Load code patterns from HuggingFace datasets"""
        
        print("Loading HuggingFace datasets...")
        
        try:
            # Load CodeAlpaca for instruction understanding
            print("Loading CodeAlpaca dataset...")
            alpaca = load_dataset("HuggingFaceH4/CodeAlpaca_20K", split="train[:100]")
            
            for item in alpaca:
                if 'output' in item and len(item['output']) > 50:
                    framework = self._detect_framework(item['output'])
                    if framework:
                        self.patterns.append({
                            'code': item['output'],
                            'metadata': {
                                'framework': framework,
                                'type': 'snippet',
                                'name': 'alpaca_pattern',
                                'description': item.get('instruction', '')[:200],
                                'source': 'CodeAlpaca'
                            }
                        })
            
            print(f"Loaded patterns from CodeAlpaca")
            
        except Exception as e:
            print(f"Error loading HuggingFace datasets: {str(e)}")
    
    def load_framework_examples(self):
        """Load examples from framework documentation"""
        
        print("Loading framework examples...")
        
        # React examples
        react_examples = [
            self._get_react_router_example(),
            self._get_react_state_management_example(),
        ]
        
        for code in react_examples:
            self.patterns.append({
                'code': code,
                'metadata': {
                    'framework': 'react',
                    'type': 'example',
                    'name': 'framework_example',
                    'source': 'official_docs'
                }
            })
        
        # Vue examples
        vue_examples = [
            self._get_vue_router_example(),
            self._get_vue_store_example(),
        ]
        
        for code in vue_examples:
            self.patterns.append({
                'code': code,
                'metadata': {
                    'framework': 'vue',
                    'type': 'example',
                    'name': 'framework_example',
                    'source': 'official_docs'
                }
            })
        
        print(f"Loaded framework examples")
    
    def _detect_framework(self, code: str) -> str:
        """Detect framework from code"""
        
        code_lower = code.lower()
        
        if 'import react' in code_lower or 'from react' in code_lower:
            return 'react'
        if 'import vue' in code_lower or '<template>' in code_lower:
            return 'vue'
        if 'from django' in code_lower or 'import django' in code_lower:
            return 'django'
        if 'const express' in code_lower or 'require(\'express\')' in code_lower:
            return 'nodejs'
        
        return None
    
    # Template methods
    def _get_react_component_template(self) -> str:
        return """import React, { useState, useEffect } from 'react';

function ComponentName({ prop1, prop2 }) {
  const [state, setState] = useState(initialValue);

  useEffect(() => {
    // Side effects here
    return () => {
      // Cleanup
    };
  }, [dependencies]);

  const handleEvent = (event) => {
    // Event handler
  };

  return (
    <div className="component-container">
      <h1>{prop1}</h1>
      <button onClick={handleEvent}>Action</button>
    </div>
  );
}

export default ComponentName;"""

    def _get_react_form_template(self) -> str:
        return """import React, { useState } from 'react';

function FormComponent() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    return newErrors;
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length === 0) {
      // Submit form
    } else {
      setErrors(newErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
      />
      {errors.email && <span>{errors.email}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}

export default FormComponent;"""

    def _get_vue_component_template(self) -> str:
        return """<template>
  <div class="component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">{{ buttonText }}</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  title: String,
  buttonText: String
})

const emit = defineEmits(['action'])

const count = ref(0)

const doubleCount = computed(() => count.value * 2)

const handleClick = () => {
  count.value++
  emit('action', count.value)
}

onMounted(() => {
  console.log('Component mounted')
})
</script>

<style scoped>
.component {
  padding: 20px;
}
</style>"""

    def _get_django_model_template(self) -> str:
        return """from django.db import models
from django.contrib.auth.models import User
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class ModelName(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return self.title"""

    def _get_django_api_view_template(self) -> str:
        return """from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ModelName
from .serializers import ModelSerializer

class ModelViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = ModelName.objects.filter(user=request.user)
        serializer = ModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

    def _get_express_route_template(self) -> str:
        return """const express = require('express');
const router = express.Router();

// GET endpoint
router.get('/items', async (req, res) => {
  try {
    const items = await Item.find();
    res.json(items);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST endpoint
router.post('/items', async (req, res) => {
  try {
    const item = new Item(req.body);
    await item.save();
    res.status(201).json(item);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;"""

    def _get_react_router_example(self) -> str:
        return """import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}"""

    def _get_react_state_management_example(self) -> str:
        return """import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

export default useStore;"""

    def _get_vue_router_example(self) -> str:
        return """import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router"""

    def _get_vue_store_example(self) -> str:
        return """import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  getters: {
    doubleCount: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    }
  }
})"""

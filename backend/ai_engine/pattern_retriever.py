import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json

class PatternRetriever:
    """
    Retrieves relevant code patterns from ChromaDB vector store
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            self.collection = self.client.get_collection("code_patterns")
        except:
            self.collection = self.client.create_collection(
                name="code_patterns",
                metadata={"description": "Web development code patterns"}
            )
    
    def search_patterns(self, query: str, framework: str, 
                       pattern_type: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant code patterns
        
        Args:
            query: Natural language query describing needed pattern
            framework: Target framework (react, vue, django, etc)
            pattern_type: Type of pattern (component, api, config, etc)
            top_k: Number of results to return
        """
        
        query_embedding = self.encoder.encode([query]).tolist()[0]
        
        where_filter = {"framework": framework}
        if pattern_type:
            where_filter["type"] = pattern_type
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            where=where_filter,
            n_results=top_k
        )
        
        patterns = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                patterns.append({
                    'code': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
        
        return patterns
    
    def search_component_patterns(self, component_name: str, framework: str, 
                                 features: List[str] = None) -> List[Dict[str, Any]]:
        """Search for specific component patterns"""
        
        query = f"{component_name} component"
        if features:
            query += f" with {', '.join(features)}"
        
        return self.search_patterns(
            query=query,
            framework=framework,
            pattern_type='component',
            top_k=3
        )
    
    def search_api_patterns(self, endpoint_type: str, framework: str) -> List[Dict[str, Any]]:
        """Search for API endpoint patterns"""
        
        query = f"{endpoint_type} API endpoint"
        
        return self.search_patterns(
            query=query,
            framework=framework,
            pattern_type='api',
            top_k=3
        )
    
    def search_config_patterns(self, config_type: str, framework: str) -> List[Dict[str, Any]]:
        """Search for configuration patterns"""
        
        query = f"{config_type} configuration"
        
        return self.search_patterns(
            query=query,
            framework=framework,
            pattern_type='config',
            top_k=2
        )
    
    def add_pattern(self, code: str, metadata: Dict[str, Any]) -> str:
        """
        Add a new code pattern to the database
        
        Args:
            code: The code content
            metadata: Pattern metadata (framework, type, name, etc)
        """
        
        embedding = self.encoder.encode([code]).tolist()[0]
        
        pattern_id = f"{metadata.get('framework', 'unknown')}_{metadata.get('type', 'unknown')}_{metadata.get('name', 'pattern')}"
        
        self.collection.add(
            embeddings=[embedding],
            documents=[code],
            metadatas=[metadata],
            ids=[pattern_id]
        )
        
        return pattern_id
    
    def batch_add_patterns(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Add multiple patterns at once"""
        
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for pattern in patterns:
            code = pattern['code']
            metadata = pattern['metadata']
            
            embedding = self.encoder.encode([code]).tolist()[0]
            pattern_id = f"{metadata.get('framework', 'unknown')}_{metadata.get('type', 'unknown')}_{metadata.get('name', 'pattern')}_{len(ids)}"
            
            embeddings.append(embedding)
            documents.append(code)
            metadatas.append(metadata)
            ids.append(pattern_id)
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def get_framework_patterns(self, framework: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all patterns for a specific framework"""
        
        results = self.collection.get(
            where={"framework": framework},
            limit=limit
        )
        
        patterns = []
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                patterns.append({
                    'code': doc,
                    'metadata': results['metadatas'][i] if results['metadatas'] else {},
                    'id': results['ids'][i] if results['ids'] else None
                })
        
        return patterns
    
    def delete_pattern(self, pattern_id: str) -> None:
        """Delete a pattern by ID"""
        self.collection.delete(ids=[pattern_id])
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        
        count = self.collection.count()
        
        return {
            'total_patterns': count,
            'collection_name': self.collection.name
        }

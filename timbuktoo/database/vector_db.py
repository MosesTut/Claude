"""Vector database operations using ChromaDB"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class VectorDatabase:
    """Manages vector embeddings and semantic search"""

    def __init__(self, persist_directory: str = "./data/vector_db"):
        """Initialize ChromaDB client and embedding model"""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Use sentence-transformers for embeddings
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="city_knowledge_vectors",
            metadata={"description": "Timbuktoo city knowledge base"}
        )

    def add_entity(
        self,
        entity_id: str,
        city_id: str,
        entity_type: str,
        title: str,
        content: str,
        tags: List[str] = None,
        vibe: List[str] = None,
        price_tier: str = None,
        seasonality: List[str] = None,
        time_of_day: List[str] = None,
        duration_minutes: int = None,
        geo_lat: float = None,
        geo_lon: float = None,
        trust_tier: int = 1,
        source: str = None,
        last_verified: str = None
    ) -> str:
        """Add entity to vector database"""

        vector_id = str(uuid.uuid4())

        # Create embedding
        embedding = self.embedding_model.encode(content).tolist()

        # Prepare metadata
        metadata = {
            "entity_id": entity_id,
            "city_id": city_id,
            "entity_type": entity_type,
            "title": title,
            "tags": ",".join(tags or []),
            "vibe": ",".join(vibe or []),
            "price_tier": price_tier or "",
            "seasonality": ",".join(seasonality or []),
            "time_of_day": ",".join(time_of_day or []),
            "duration_minutes": str(duration_minutes or 0),
            "geo_lat": str(geo_lat or 0.0),
            "geo_lon": str(geo_lon or 0.0),
            "trust_tier": str(trust_tier),
            "source": source or "",
            "last_verified": last_verified or ""
        }

        # Add to collection
        self.collection.add(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )

        return vector_id

    def search(
        self,
        query: str,
        city_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        vibes: Optional[List[str]] = None,
        price_tiers: Optional[List[str]] = None,
        n_results: int = 35,
        min_trust_tier: int = 1
    ) -> List[Dict[str, Any]]:
        """Semantic search with filters"""

        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Build where filter
        where_filter = {}
        if city_id:
            where_filter["city_id"] = city_id
        if entity_type:
            where_filter["entity_type"] = entity_type

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if where_filter else None
        )

        # Process results
        processed_results = []
        if results and results.get('ids') and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                metadata = results['metadatas'][0][i]

                # Apply additional filters
                if int(metadata.get('trust_tier', 0)) < min_trust_tier:
                    continue

                if price_tiers:
                    if metadata.get('price_tier') not in price_tiers:
                        continue

                if vibes:
                    entity_vibes = metadata.get('vibe', '').split(',')
                    if not any(v in entity_vibes for v in vibes):
                        continue

                processed_results.append({
                    'vector_id': results['ids'][0][i],
                    'entity_id': metadata.get('entity_id'),
                    'city_id': metadata.get('city_id'),
                    'entity_type': metadata.get('entity_type'),
                    'title': metadata.get('title'),
                    'content': results['documents'][0][i],
                    'tags': metadata.get('tags', '').split(',') if metadata.get('tags') else [],
                    'vibe': metadata.get('vibe', '').split(',') if metadata.get('vibe') else [],
                    'price_tier': metadata.get('price_tier'),
                    'distance': results['distances'][0][i] if 'distances' in results else None,
                    'trust_tier': int(metadata.get('trust_tier', 1))
                })

        return processed_results

    def get_by_city(self, city_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all entities for a city"""
        return self.search(query="", city_id=city_id, n_results=limit)

    def delete_entity(self, vector_id: str):
        """Delete entity from vector database"""
        self.collection.delete(ids=[vector_id])

    def reset(self):
        """Reset the entire collection (use with caution)"""
        self.client.delete_collection("city_knowledge_vectors")
        self.collection = self.client.create_collection(
            name="city_knowledge_vectors",
            metadata={"description": "Timbuktoo city knowledge base"}
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        count = self.collection.count()
        return {
            "total_vectors": count,
            "collection_name": self.collection.name,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "persist_directory": self.persist_directory
        }


# Singleton instance
_vector_db_instance = None

def get_vector_db() -> VectorDatabase:
    """Get or create vector database instance"""
    global _vector_db_instance
    if _vector_db_instance is None:
        persist_dir = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
        _vector_db_instance = VectorDatabase(persist_directory=persist_dir)
    return _vector_db_instance

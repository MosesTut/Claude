"""Tenant-aware vector database with namespace isolation"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..utils.logger import get_logger

logger = get_logger(__name__)


class TenantVectorDatabase:
    """Multi-tenant vector database with namespace isolation"""

    def __init__(self, persist_directory: str = "./data/vector_db"):
        """Initialize ChromaDB client with multi-tenant support"""
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

        # Collection per tenant namespace
        self.collections = {}

    def get_collection(self, tenant_id: str):
        """Get or create collection for tenant"""
        if tenant_id not in self.collections:
            collection_name = f"tenant_{tenant_id.replace('-', '_')}_vectors"

            try:
                self.collections[tenant_id] = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={
                        "description": f"Vector knowledge for tenant {tenant_id}",
                        "tenant_id": tenant_id
                    }
                )
                logger.info(f"Collection created/retrieved for tenant {tenant_id}")
            except Exception as e:
                logger.error(f"Failed to get collection for tenant {tenant_id}: {str(e)}")
                raise

        return self.collections[tenant_id]

    def add_entity(
        self,
        tenant_id: str,
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
        """Add entity to tenant's vector collection"""

        collection = self.get_collection(tenant_id)
        vector_id = str(uuid.uuid4())

        # Create embedding
        embedding = self.embedding_model.encode(content).tolist()

        # Prepare metadata
        metadata = {
            "tenant_id": tenant_id,
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
        collection.add(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )

        logger.info(
            f"Entity added to tenant {tenant_id} vector DB",
            extra={"entity_id": entity_id, "vector_id": vector_id}
        )

        return vector_id

    def search(
        self,
        tenant_id: str,
        query: str,
        city_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        vibes: Optional[List[str]] = None,
        price_tiers: Optional[List[str]] = None,
        n_results: int = 35,
        min_trust_tier: int = 1
    ) -> List[Dict[str, Any]]:
        """Semantic search within tenant's namespace"""

        collection = self.get_collection(tenant_id)

        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Build where filter
        where_filter = {"tenant_id": tenant_id}
        if city_id:
            where_filter["city_id"] = city_id
        if entity_type:
            where_filter["entity_type"] = entity_type

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if len(where_filter) > 1 else {"tenant_id": tenant_id}
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

        logger.info(f"Vector search for tenant {tenant_id}: {len(processed_results)} results")
        return processed_results

    def get_by_city(self, tenant_id: str, city_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all entities for a city within tenant's namespace"""
        return self.search(query="", tenant_id=tenant_id, city_id=city_id, n_results=limit)

    def delete_entity(self, tenant_id: str, vector_id: str):
        """Delete entity from tenant's vector collection"""
        collection = self.get_collection(tenant_id)
        collection.delete(ids=[vector_id])
        logger.info(f"Entity {vector_id} deleted from tenant {tenant_id}")

    def delete_tenant_data(self, tenant_id: str):
        """Delete all data for a tenant (GDPR compliance)"""
        try:
            collection_name = f"tenant_{tenant_id.replace('-', '_')}_vectors"
            self.client.delete_collection(collection_name)

            if tenant_id in self.collections:
                del self.collections[tenant_id]

            logger.info(f"All data deleted for tenant {tenant_id}")
        except Exception as e:
            logger.error(f"Failed to delete tenant data: {str(e)}")
            raise

    def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get statistics for tenant's vector database"""
        collection = self.get_collection(tenant_id)
        count = collection.count()

        return {
            "tenant_id": tenant_id,
            "total_vectors": count,
            "collection_name": collection.name,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
        }

    def copy_shared_data_to_tenant(self, tenant_id: str, shared_collection_name: str = "city_knowledge_vectors"):
        """
        Copy shared/global city data to tenant's namespace
        Used during tenant onboarding to give them initial data
        """
        try:
            # Get shared collection
            shared_collection = self.client.get_collection(shared_collection_name)
            tenant_collection = self.get_collection(tenant_id)

            # Get all items from shared collection
            results = shared_collection.get()

            if not results or not results.get('ids'):
                logger.warning("No shared data to copy")
                return

            # Copy to tenant collection
            for i, doc_id in enumerate(results['ids']):
                metadata = results['metadatas'][i]
                metadata['tenant_id'] = tenant_id  # Add tenant_id

                tenant_collection.add(
                    ids=[doc_id],
                    embeddings=[results['embeddings'][i]] if results.get('embeddings') else None,
                    documents=[results['documents'][i]],
                    metadatas=[metadata]
                )

            logger.info(
                f"Copied {len(results['ids'])} shared vectors to tenant {tenant_id}",
                extra={"count": len(results['ids'])}
            )

        except Exception as e:
            logger.error(f"Failed to copy shared data: {str(e)}")
            # Non-fatal - tenant can still function


# Singleton instance
_tenant_vector_db = None

def get_tenant_vector_db() -> TenantVectorDatabase:
    """Get or create tenant vector database instance"""
    global _tenant_vector_db
    if _tenant_vector_db is None:
        persist_dir = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
        _tenant_vector_db = TenantVectorDatabase(persist_directory=persist_dir)
    return _tenant_vector_db

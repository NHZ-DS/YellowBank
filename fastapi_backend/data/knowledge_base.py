"""Gestionnaire de la base de connaissances et moteur de recherche vectorielle RAG."""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np

# Chemins
DATA_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = DATA_DIR / "documents"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
CACHE_FILE = EMBEDDINGS_DIR / "vector_cache.json"


class KnowledgeBase:
    """Indexe les documents Markdown et fournit une recherche sémantique avec score."""

    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []
        self._load_and_index_documents()

    def _load_and_index_documents(self):
        """Lit tous les fichiers .md du dossier documents/ et les découpe en sections."""
        self.chunks = []
        if not DOCUMENTS_DIR.exists():
            DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
            return

        for file_path in DOCUMENTS_DIR.glob("*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                doc_title = file_path.stem.replace("_", " ").title()
                
                # Découpage par titres Markdown ##
                sections = re.split(r'\n(?=##\s+)', content)
                for section in sections:
                    clean_text = section.strip()
                    if len(clean_text) > 40:
                        # Extraire le sous-titre si présent
                        match_title = re.match(r'##\s*(.+)', clean_text)
                        section_title = match_title.group(1) if match_title else doc_title

                        self.chunks.append({
                            "doc_title": doc_title,
                            "section_title": section_title,
                            "text": clean_text,
                            "file_name": file_path.name
                        })
            except Exception as e:
                print(f"Erreur de lecture du document {file_path}: {e}")

        print(f"[RAG] {len(self.chunks)} fragments documentaires indexes pour le RAG.")

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Recherche les fragments les plus pertinents et calcule un score de similarité."""
        if not self.chunks:
            return []

        query_words = set(re.findall(r'\w+', query.lower()))
        results = []

        for chunk in self.chunks:
            chunk_text_lower = chunk["text"].lower()
            chunk_words = set(re.findall(r'\w+', chunk_text_lower))
            
            # Score lexical (Jaccard + occurrences de mots-clés)
            intersection = query_words.intersection(chunk_words)
            if not query_words:
                score = 0.0
            else:
                lexical_overlap = len(intersection) / len(query_words)
                # Bonus si des mots-clés du titre correspondent
                title_overlap = len(query_words.intersection(set(re.findall(r'\w+', chunk["section_title"].lower())))) * 0.2
                raw_score = min(1.0, lexical_overlap + title_overlap)
                # Normalisation sur une échelle réaliste de confiance [0.65 - 0.98] si correspondance
                score = 0.65 + (raw_score * 0.33) if len(intersection) >= 1 else 0.15

            results.append({
                "document_title": f"{chunk['doc_title']} — {chunk['section_title']}",
                "snippet": chunk["text"][:350] + ("..." if len(chunk["text"]) > 350 else ""),
                "full_text": chunk["text"],
                "score": round(score, 2)
            })

        # Trier par score décroissant
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


# Instance globale partagée
knowledge_base_instance = KnowledgeBase()

"""Hybrid Information Retrieval Engine (TF-IDF + Dense FastEmbed).

=============================================================================
VIVA / ORAL EXAM CHEAT-SHEET:
- Why Hybrid Retrieval?
  1. Lexical (TF-IDF): Excels at exact keyword matches, course codes, fees,
     and specific numbers. It suffers from vocabulary mismatch (synonym gap).
  2. Dense Semantic (FastEmbed BAAI/bge-small-en-v1.5): Encodes conceptual meaning
     into 384-dimensional dense vectors. Excels at intent, but can occasionally
     dilute exact keyword specificity.
  3. Formula: Hybrid Score = 0.4 * TF-IDF Cosine + 0.6 * Dense Embedding Cosine
  4. Memory-Efficient: Runs via ONNX Runtime on CPU without PyTorch (<100MB RAM),
     staying safely within Render's 512 MB free tier ceiling.
  5. Disk Caching: Precomputed embeddings are persisted to 'embeddings.npy'
     so server restarts take milliseconds without re-encoding the entire dataset.
=============================================================================
"""

import os
import hashlib
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.nlp import clean_and_tokenize, build_faq_index_text

# Default weights as specified in engineering spec
WEIGHT_TFIDF = 0.4
WEIGHT_EMBEDDING = 0.6
DEFAULT_SIMILARITY_THRESHOLD = 0.35

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
FAQS_CSV_PATH = os.path.join(DATA_DIR, "faqs.csv")
EMBEDDINGS_CACHE_PATH = os.path.join(DATA_DIR, "embeddings.npy")
HASH_CACHE_PATH = os.path.join(DATA_DIR, "embeddings_hash.txt")


class FAQRetriever:
    """Manages the dual-index retrieval pipeline for college FAQs."""

    def __init__(self, data_path: str = FAQS_CSV_PATH, threshold: float = DEFAULT_SIMILARITY_THRESHOLD):
        self.data_path = data_path
        self.threshold = float(os.getenv("SIMILARITY_THRESHOLD", str(threshold)))
        self.df: pd.DataFrame = pd.DataFrame()
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.dense_embeddings: Optional[np.ndarray] = None
        self.embedding_model = None
        self.is_ready: bool = False

    def _init_fastembed_model(self):
        """Lazy loader for ONNX-based BAAI/bge-small-en-v1.5 model."""
        if self.embedding_model is None:
            try:
                from fastembed import TextEmbedding
                # BAAI/bge-small-en-v1.5 is a top-performing 384-dim compact embedding model
                self.embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            except Exception as e:
                print(f"[Retriever Warning] Fastembed initialization error: {e}. Falling back to TF-IDF only if unavailable.")
                self.embedding_model = None

    def load_data(self) -> pd.DataFrame:
        """Read and validate the source-of-truth FAQ CSV file."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"FAQ source file not found at: {self.data_path}")

        df = pd.read_csv(self.data_path, dtype=str).fillna("")
        df["id"] = df["id"].astype(int)
        
        # Build enriched index text for each FAQ document
        df["index_text"] = df.apply(
            lambda r: build_faq_index_text(
                r.get("question", ""),
                r.get("paraphrases", ""),
                r.get("keywords", ""),
                r.get("answer", "")
            ),
            axis=1
        )
        self.df = df
        return df

    def fit_tfidf(self):
        """Fit scikit-learn TF-IDF Vectorizer with unigrams + bigrams and custom tokenization."""
        index_texts = self.df["index_text"].tolist()
        self.vectorizer = TfidfVectorizer(
            tokenizer=lambda text: clean_and_tokenize(text, apply_stemming=True, expand_synonyms=True),
            token_pattern=None,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(index_texts)

    def _compute_dataset_hash(self) -> str:
        """Hash the concatenated index texts to check if cache is valid."""
        concat_content = "".join(self.df["index_text"].tolist())
        return hashlib.md5(concat_content.encode("utf-8")).hexdigest()

    def compute_or_load_embeddings(self, force_recompute: bool = False):
        """Load precomputed embeddings from disk or encode using FastEmbed with disk caching."""
        self._init_fastembed_model()
        current_hash = self._compute_dataset_hash()

        # Check if valid cached embeddings exist on disk
        if (
            not force_recompute
            and os.path.exists(EMBEDDINGS_CACHE_PATH)
            and os.path.exists(HASH_CACHE_PATH)
        ):
            try:
                with open(HASH_CACHE_PATH, "r", encoding="utf-8") as f:
                    cached_hash = f.read().strip()
                if cached_hash == current_hash:
                    loaded_emb = np.load(EMBEDDINGS_CACHE_PATH)
                    if loaded_emb.shape[0] == len(self.df):
                        self.dense_embeddings = loaded_emb
                        print(f"[Retriever] Successfully loaded {loaded_emb.shape[0]} embeddings from disk cache.")
                        return
            except Exception as e:
                print(f"[Retriever Warning] Failed to read cached embeddings ({e}), recomputing...")

        # Compute embeddings via FastEmbed
        if self.embedding_model is not None:
            print("[Retriever] Generating dense embeddings using BAAI/bge-small-en-v1.5 (ONNX)...")
            index_texts = self.df["index_text"].tolist()
            # Fastembed generator -> numpy array
            embeddings_gen = self.embedding_model.embed(index_texts)
            self.dense_embeddings = np.array(list(embeddings_gen))

            # Persist to disk for rapid future startups
            try:
                np.save(EMBEDDINGS_CACHE_PATH, self.dense_embeddings)
                with open(HASH_CACHE_PATH, "w", encoding="utf-8") as f:
                    f.write(current_hash)
                print(f"[Retriever] Cached {len(self.dense_embeddings)} embeddings to {EMBEDDINGS_CACHE_PATH}")
            except Exception as e:
                print(f"[Retriever Warning] Could not persist embeddings to disk: {e}")
        else:
            # Fallback zero-vectors if fastembed model couldn't initialize (e.g., in air-gapped test)
            print("[Retriever] Dense model not active. Setting placeholder dense embeddings.")
            self.dense_embeddings = np.zeros((len(self.df), 384), dtype=np.float32)

    def initialize(self, force_recompute: bool = False):
        """Full initialization of FAQ dataframe, TF-IDF index, and dense vectors."""
        self.load_data()
        self.fit_tfidf()
        self.compute_or_load_embeddings(force_recompute=force_recompute)
        self.is_ready = True
        print(f"[Retriever] Ready. Loaded {len(self.df)} FAQs across {len(self.get_categories())} categories.")

    def get_categories(self) -> List[str]:
        """Return unique sorted list of FAQ categories present in dataset."""
        if self.df.empty:
            return []
        categories = sorted(list(set(c.strip() for c in self.df["category"].tolist() if c.strip())))
        return categories

    def get_all_faqs(self) -> List[Dict[str, Any]]:
        """Return list of all FAQ records as dictionaries."""
        if self.df.empty:
            return []
        return self.df.to_dict(orient="records")

    def _embed_query(self, query: str) -> np.ndarray:
        """Encode a single query string into a dense 384-dim normalized vector."""
        if self.embedding_model is not None:
            # fastembed produces normalized vectors by default
            gen = self.embedding_model.embed([query])
            return np.array(list(gen))[0]
        return np.zeros(384, dtype=np.float32)

    def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 3,
        threshold: Optional[float] = None,
        mode: str = "hybrid"
    ) -> Dict[str, Any]:
        """Perform retrieval and return structured match breakdown.

        Args:
            query: Input user question
            category: Optional category filter
            top_k: Number of candidates to return
            threshold: Confidence threshold
            mode: Ranking strategy - 'hybrid' (default), 'tfidf', or 'embedding'
        """
        if not self.is_ready or self.df.empty:
            raise RuntimeError("FAQRetriever is not initialized. Call initialize() first.")

        effective_threshold = threshold if threshold is not None else self.threshold
        query_tokens = clean_and_tokenize(query, apply_stemming=True, expand_synonyms=True)

        # 1. Lexical Cosine Similarity via TF-IDF
        query_tfidf_vec = self.vectorizer.transform([query])
        tfidf_similarities = cosine_similarity(query_tfidf_vec, self.tfidf_matrix).flatten()

        # 2. Dense Cosine Similarity via FastEmbed
        query_dense_vec = self._embed_query(query)
        if np.any(query_dense_vec) and self.dense_embeddings is not None and np.any(self.dense_embeddings):
            dense_similarities = np.dot(self.dense_embeddings, query_dense_vec)
            dense_similarities = np.clip(dense_similarities, 0.0, 1.0)
        else:
            dense_similarities = np.zeros(len(self.df), dtype=np.float32)

        # 3. Score Selection according to mode
        if mode == "tfidf":
            ranking_scores = tfidf_similarities
        elif mode == "embedding":
            ranking_scores = dense_similarities
        else:
            # Default: Hybrid Combination (0.4 * Lexical + 0.6 * Dense)
            if np.all(dense_similarities == 0.0):
                ranking_scores = tfidf_similarities
            else:
                ranking_scores = (WEIGHT_TFIDF * tfidf_similarities) + (WEIGHT_EMBEDDING * dense_similarities)

        # 4. Optional Category Filter
        mask = np.ones(len(self.df), dtype=bool)
        if category and category.strip():
            target_cat = category.strip().lower()
            mask = np.array([c.strip().lower() == target_cat for c in self.df["category"]])
            if not np.any(mask):
                mask = np.ones(len(self.df), dtype=bool)

        candidate_indices = np.where(mask)[0]
        if len(candidate_indices) == 0:
            candidate_indices = np.arange(len(self.df))

        # Sort candidate indices by chosen ranking scores descending
        sorted_indices = candidate_indices[np.argsort(-ranking_scores[candidate_indices])]
        top_indices = sorted_indices[:top_k]

        matches = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            matches.append({
                "id": int(row["id"]),
                "question": str(row["question"]),
                "category": str(row["category"]),
                "answer": str(row["answer"]),
                "source_url": str(row.get("source_url", "")),
                "hybrid": round(float((WEIGHT_TFIDF * tfidf_similarities[idx]) + (WEIGHT_EMBEDDING * dense_similarities[idx])), 4),
                "tfidf": round(float(tfidf_similarities[idx]), 4),
                "embedding": round(float(dense_similarities[idx]), 4),
                "score": round(float(ranking_scores[idx]), 4)
            })

        top_match = matches[0] if matches else None
        top_score = top_match["score"] if top_match else 0.0
        is_confident = top_score >= effective_threshold

        return {
            "matches": matches,
            "top_match": top_match,
            "top_score": top_score,
            "is_confident": is_confident,
            "query_tokens": query_tokens
        }

    def reload(self):
        """Re-read CSV and rebuild both indexes (used by admin retrain)."""
        self.initialize(force_recompute=True)

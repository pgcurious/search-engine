"""
Indexer Module
Builds an inverted index and calculates TF-IDF scores for documents.
"""

import re
import math
from collections import defaultdict, Counter
from typing import Dict, List, Set
import json


class SearchIndexer:
    """
    Builds and maintains an inverted index with TF-IDF scoring.

    An inverted index maps terms to the documents they appear in,
    enabling fast full-text search.
    """

    def __init__(self):
        """Initialize the indexer."""
        # Inverted index: term -> {doc_id: frequency}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # Document store: doc_id -> document data
        self.documents: Dict[str, Dict] = {}

        # Document lengths for normalization
        self.doc_lengths: Dict[str, int] = {}

        # TF-IDF scores: term -> {doc_id: score}
        self.tfidf_scores: Dict[str, Dict[str, float]] = {}

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into terms.

        Args:
            text: Input text

        Returns:
            List of lowercase tokens
        """
        # Convert to lowercase and split on non-alphanumeric characters
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)

        # Simple stop words removal
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their'
        }

        # Filter out stop words and short tokens
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]

        return tokens

    def add_document(self, doc_id: str, title: str, content: str, url: str = ""):
        """
        Add a document to the index.

        Args:
            doc_id: Unique document identifier
            title: Document title
            content: Document content
            url: Document URL (optional)
        """
        # Store document
        self.documents[doc_id] = {
            'title': title,
            'content': content[:500],  # Store preview
            'url': url
        }

        # Tokenize title and content (title tokens weighted more)
        title_tokens = self.tokenize(title)
        content_tokens = self.tokenize(content)

        # Combine with title weight (title appears 3 times for importance)
        all_tokens = title_tokens * 3 + content_tokens

        # Count term frequencies
        term_frequencies = Counter(all_tokens)

        # Update inverted index
        for term, freq in term_frequencies.items():
            self.inverted_index[term][doc_id] = freq

        # Store document length
        self.doc_lengths[doc_id] = len(all_tokens)

    def calculate_tfidf(self):
        """
        Calculate TF-IDF scores for all terms and documents.

        TF-IDF = Term Frequency × Inverse Document Frequency
        - TF: How often a term appears in a document
        - IDF: How rare a term is across all documents (log(N/df))
        """
        num_docs = len(self.documents)

        if num_docs == 0:
            return

        for term, doc_freqs in self.inverted_index.items():
            # Calculate IDF: log(total_docs / docs_containing_term)
            idf = math.log(num_docs / len(doc_freqs))

            self.tfidf_scores[term] = {}

            for doc_id, term_freq in doc_freqs.items():
                # Calculate TF: term frequency / document length
                tf = term_freq / self.doc_lengths[doc_id] if self.doc_lengths[doc_id] > 0 else 0

                # TF-IDF score
                self.tfidf_scores[term][doc_id] = tf * idf

    def get_index_stats(self) -> Dict:
        """Get statistics about the index."""
        return {
            'num_documents': len(self.documents),
            'num_terms': len(self.inverted_index),
            'avg_doc_length': sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0
        }

    def save_index(self, filepath: str):
        """Save the index to a JSON file."""
        data = {
            'inverted_index': {k: dict(v) for k, v in self.inverted_index.items()},
            'documents': self.documents,
            'doc_lengths': self.doc_lengths,
            'tfidf_scores': self.tfidf_scores
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Index saved to {filepath}")

    def load_index(self, filepath: str):
        """Load the index from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.inverted_index = defaultdict(lambda: defaultdict(int), {
            k: defaultdict(int, v) for k, v in data['inverted_index'].items()
        })
        self.documents = data['documents']
        self.doc_lengths = data['doc_lengths']
        self.tfidf_scores = data['tfidf_scores']

        print(f"Index loaded from {filepath}")


if __name__ == "__main__":
    # Example usage
    indexer = SearchIndexer()

    # Add some sample documents
    indexer.add_document(
        "doc1",
        "Introduction to Search Engines",
        "Search engines are systems that help users find information on the web. "
        "They use crawlers to discover pages and indexing to organize content.",
        "http://example.com/doc1"
    )

    indexer.add_document(
        "doc2",
        "Web Crawlers Explained",
        "Web crawlers, also known as spiders, systematically browse the web to "
        "discover and fetch web pages for search engine indexing.",
        "http://example.com/doc2"
    )

    indexer.add_document(
        "doc3",
        "Understanding TF-IDF",
        "TF-IDF is a numerical statistic used to reflect how important a word is "
        "to a document in a collection. It's widely used in information retrieval.",
        "http://example.com/doc3"
    )

    # Calculate TF-IDF
    indexer.calculate_tfidf()

    # Print stats
    print("Index Statistics:")
    print(indexer.get_index_stats())

    # Show inverted index for a term
    print("\nInverted index for 'search':")
    print(dict(indexer.inverted_index.get('search', {})))

    print("\nTF-IDF scores for 'search':")
    print(indexer.tfidf_scores.get('search', {}))

"""
Search Engine Module
Processes queries and returns ranked results using the inverted index.
"""

from typing import List, Dict, Tuple
from collections import defaultdict
import math


class SearchEngine:
    """
    Query processor that searches the index and ranks results.
    """

    def __init__(self, indexer):
        """
        Initialize search engine with an indexer.

        Args:
            indexer: SearchIndexer instance with built index
        """
        self.indexer = indexer

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Search for documents matching the query.

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of ranked search results
        """
        # Tokenize query
        query_terms = self.indexer.tokenize(query)

        if not query_terms:
            return []

        # Calculate scores for each document
        doc_scores = defaultdict(float)

        for term in query_terms:
            if term in self.indexer.tfidf_scores:
                # Add TF-IDF scores for this term across all documents
                for doc_id, score in self.indexer.tfidf_scores[term].items():
                    doc_scores[doc_id] += score

        # If no documents found, return empty
        if not doc_scores:
            return []

        # Sort documents by score (descending)
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        # Get top K results
        results = []
        for doc_id, score in ranked_docs[:top_k]:
            doc = self.indexer.documents[doc_id]
            results.append({
                'doc_id': doc_id,
                'title': doc['title'],
                'url': doc['url'],
                'snippet': doc['content'],
                'score': round(score, 4),
                'matched_terms': self._get_matched_terms(doc_id, query_terms)
            })

        return results

    def _get_matched_terms(self, doc_id: str, query_terms: List[str]) -> List[str]:
        """Get which query terms matched in the document."""
        matched = []
        for term in query_terms:
            if term in self.indexer.inverted_index:
                if doc_id in self.indexer.inverted_index[term]:
                    matched.append(term)
        return matched

    def search_phrase(self, phrase: str, top_k: int = 10) -> List[Dict]:
        """
        Search for an exact phrase (simplified implementation).

        Args:
            phrase: Exact phrase to search for
            top_k: Number of results to return

        Returns:
            List of documents containing the phrase
        """
        results = []
        phrase_lower = phrase.lower()

        for doc_id, doc in self.indexer.documents.items():
            # Check if phrase exists in content or title
            content = doc['content'].lower()
            title = doc['title'].lower()

            if phrase_lower in content or phrase_lower in title:
                # Calculate a simple score based on frequency
                score = content.count(phrase_lower) + title.count(phrase_lower) * 3

                results.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'url': doc['url'],
                    'snippet': doc['content'],
                    'score': score,
                    'matched_terms': [phrase]
                })

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:top_k]

    def get_suggestions(self, prefix: str, max_suggestions: int = 5) -> List[str]:
        """
        Get search suggestions based on indexed terms.

        Args:
            prefix: Query prefix
            max_suggestions: Maximum number of suggestions

        Returns:
            List of suggested terms
        """
        prefix_lower = prefix.lower()
        suggestions = []

        # Find terms starting with prefix
        for term in self.indexer.inverted_index.keys():
            if term.startswith(prefix_lower):
                # Score by document frequency
                doc_freq = len(self.indexer.inverted_index[term])
                suggestions.append((term, doc_freq))

        # Sort by frequency and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [term for term, _ in suggestions[:max_suggestions]]


if __name__ == "__main__":
    # Example usage with the indexer
    from indexer import SearchIndexer

    indexer = SearchIndexer()

    # Add sample documents
    docs = [
        {
            "id": "1",
            "title": "Python Programming Tutorial",
            "content": "Python is a high-level programming language. It's great for beginners and experts alike. Python web frameworks include Django and Flask.",
            "url": "http://example.com/python"
        },
        {
            "id": "2",
            "title": "Web Development Guide",
            "content": "Web development involves creating websites and web applications. Popular technologies include HTML, CSS, JavaScript, and Python frameworks.",
            "url": "http://example.com/webdev"
        },
        {
            "id": "3",
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence. Python is the most popular language for machine learning with libraries like TensorFlow and scikit-learn.",
            "url": "http://example.com/ml"
        },
        {
            "id": "4",
            "title": "Database Management",
            "content": "Databases store and organize data. SQL is used for relational databases while NoSQL databases like MongoDB offer flexible schemas.",
            "url": "http://example.com/db"
        }
    ]

    for doc in docs:
        indexer.add_document(doc['id'], doc['title'], doc['content'], doc['url'])

    indexer.calculate_tfidf()

    # Create search engine
    engine = SearchEngine(indexer)

    # Test searches
    print("=" * 60)
    print("SEARCH RESULTS FOR: 'python programming'")
    print("=" * 60)
    results = engine.search("python programming")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']} (Score: {result['score']})")
        print(f"   URL: {result['url']}")
        print(f"   Matched terms: {', '.join(result['matched_terms'])}")
        print(f"   {result['snippet'][:100]}...")

    print("\n" + "=" * 60)
    print("SEARCH RESULTS FOR: 'machine learning'")
    print("=" * 60)
    results = engine.search("machine learning")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']} (Score: {result['score']})")
        print(f"   URL: {result['url']}")
        print(f"   Matched terms: {', '.join(result['matched_terms'])}")

    print("\n" + "=" * 60)
    print("SUGGESTIONS FOR: 'prog'")
    print("=" * 60)
    suggestions = engine.get_suggestions("prog")
    print(suggestions)

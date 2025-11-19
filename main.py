#!/usr/bin/env python3
"""
Main Entry Point for Educational Search Engine

This script demonstrates how a basic search engine works by implementing:
1. Web Crawling - Discovering and fetching web pages
2. Indexing - Building an inverted index with TF-IDF scores
3. Searching - Query processing and result ranking
4. Web Interface - Simple Flask-based UI

Usage:
    python main.py crawl <url>     - Crawl and index a website
    python main.py demo            - Run with sample data
    python main.py serve           - Start web interface
    python main.py search <query>  - Command-line search
"""

import sys
import argparse
from crawler import WebCrawler
from indexer import SearchIndexer
from search_engine import SearchEngine


def crawl_and_index(seed_url: str, max_pages: int = 50, same_domain: bool = True):
    """Crawl a website and build the search index."""
    print("=" * 70)
    print("STEP 1: WEB CRAWLING")
    print("=" * 70)
    print(f"Starting crawler with seed URL: {seed_url}")
    print(f"Max pages: {max_pages}")
    print(f"Same domain only: {same_domain}\n")

    crawler = WebCrawler(max_pages=max_pages, delay=0.5)
    pages = crawler.crawl([seed_url], same_domain=same_domain)

    print(f"\n✓ Crawled {len(pages)} pages\n")

    print("=" * 70)
    print("STEP 2: BUILDING INDEX")
    print("=" * 70)

    indexer = SearchIndexer()

    for i, page in enumerate(pages):
        doc_id = f"doc_{i}"
        indexer.add_document(
            doc_id=doc_id,
            title=page['title'],
            content=page['content'],
            url=page['url']
        )
        print(f"Indexed: {page['title'][:60]}...")

    print("\n" + "=" * 70)
    print("STEP 3: CALCULATING TF-IDF SCORES")
    print("=" * 70)

    indexer.calculate_tfidf()
    print("✓ TF-IDF calculation complete\n")

    # Save index
    index_file = 'search_index.json'
    indexer.save_index(index_file)

    # Show statistics
    stats = indexer.get_index_stats()
    print("\n" + "=" * 70)
    print("INDEX STATISTICS")
    print("=" * 70)
    print(f"Total documents: {stats['num_documents']}")
    print(f"Unique terms: {stats['num_terms']}")
    print(f"Average document length: {stats['avg_doc_length']:.1f} tokens")
    print("\n✓ Index saved to", index_file)

    return indexer


def demo_search():
    """Run demo with sample documents."""
    print("=" * 70)
    print("EDUCATIONAL SEARCH ENGINE - DEMO MODE")
    print("=" * 70)
    print("\nCreating sample index with educational content...\n")

    indexer = SearchIndexer()

    # Sample documents about search engines and related topics
    sample_docs = [
        {
            "title": "How Search Engines Work",
            "content": """
                Search engines are complex systems that help users find information on the internet.
                They work through three main processes: crawling, indexing, and ranking.
                Web crawlers discover pages by following links. The indexer processes and stores
                content in a structured format. The ranking algorithm determines which results
                are most relevant to a query using techniques like TF-IDF and PageRank.
            """,
            "url": "https://example.com/how-search-engines-work"
        },
        {
            "title": "Understanding Web Crawlers",
            "content": """
                Web crawlers, also known as spiders or bots, are programs that systematically
                browse the internet. They start from seed URLs and follow links to discover
                new pages. Crawlers must be polite and respect robots.txt files. They face
                challenges like duplicate content, infinite loops, and dynamic content.
            """,
            "url": "https://example.com/web-crawlers"
        },
        {
            "title": "Inverted Index Explained",
            "content": """
                An inverted index is a data structure that maps terms to documents.
                Instead of storing documents and their terms, it stores terms and their documents.
                This enables fast full-text search. For each term, the index stores a list of
                documents containing that term, along with frequency information.
            """,
            "url": "https://example.com/inverted-index"
        },
        {
            "title": "TF-IDF Algorithm",
            "content": """
                TF-IDF stands for Term Frequency-Inverse Document Frequency. It's a numerical
                statistic used to measure how important a word is to a document in a collection.
                Term Frequency measures how often a term appears in a document. Inverse Document
                Frequency measures how rare a term is across all documents. The product gives
                higher scores to terms that are common in a document but rare overall.
            """,
            "url": "https://example.com/tfidf"
        },
        {
            "title": "Introduction to Information Retrieval",
            "content": """
                Information retrieval is the science of searching for information in documents.
                It involves finding material of an unstructured nature that satisfies an
                information need from large collections. Modern search engines use sophisticated
                algorithms including vector space models, probabilistic models, and machine learning.
            """,
            "url": "https://example.com/information-retrieval"
        },
        {
            "title": "PageRank Algorithm",
            "content": """
                PageRank is an algorithm used by Google Search to rank web pages. It measures
                the importance of website pages by counting the number and quality of links.
                The assumption is that more important websites receive more links from other sites.
                PageRank works by counting the number of links to a page to determine an estimate
                of how important the page is.
            """,
            "url": "https://example.com/pagerank"
        },
        {
            "title": "Natural Language Processing for Search",
            "content": """
                Natural Language Processing helps search engines understand queries and content.
                Techniques include tokenization, stemming, lemmatization, and named entity recognition.
                Modern search uses NLP to handle synonyms, understand context, and provide better
                results. Machine learning models can learn patterns from user behavior.
            """,
            "url": "https://example.com/nlp-search"
        },
        {
            "title": "Building a Search Engine",
            "content": """
                Building a search engine involves several components: a crawler to fetch pages,
                an indexer to process content, a ranking algorithm to score results, and a
                query processor to handle searches. Storage systems must handle large amounts
                of data efficiently. The system should be scalable and handle millions of queries.
            """,
            "url": "https://example.com/building-search-engine"
        }
    ]

    for i, doc in enumerate(sample_docs):
        indexer.add_document(
            doc_id=f"doc_{i}",
            title=doc['title'],
            content=doc['content'],
            url=doc['url']
        )
        print(f"✓ Indexed: {doc['title']}")

    print("\nCalculating TF-IDF scores...")
    indexer.calculate_tfidf()

    # Save index
    indexer.save_index('search_index.json')

    stats = indexer.get_index_stats()
    print(f"\n✓ Index created with {stats['num_documents']} documents and {stats['num_terms']} terms")

    # Demo searches
    search_engine = SearchEngine(indexer)

    queries = [
        "search engine algorithm",
        "web crawler spider",
        "TF-IDF ranking",
        "information retrieval"
    ]

    print("\n" + "=" * 70)
    print("DEMO SEARCHES")
    print("=" * 70)

    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 70)
        results = search_engine.search(query, top_k=3)

        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']} (Score: {result['score']})")
            print(f"   {result['url']}")
            print(f"   Matched terms: {', '.join(result['matched_terms'])}")

    print("\n" + "=" * 70)
    print("Demo complete! Run 'python main.py serve' to start the web interface.")
    print("=" * 70)


def search_cli(query: str):
    """Command-line search interface."""
    import os

    if not os.path.exists('search_index.json'):
        print("Error: No index found. Run 'python main.py demo' or 'python main.py crawl <url>' first.")
        return

    indexer = SearchIndexer()
    indexer.load_index('search_index.json')

    engine = SearchEngine(indexer)
    results = engine.search(query, top_k=10)

    print(f"\nSearch results for: '{query}'")
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Score: {result['score']}")
        print(f"   Matched terms: {', '.join(result['matched_terms'])}")
        print(f"   {result['snippet'][:150]}...")


def serve():
    """Start the web interface."""
    import os

    if not os.path.exists('search_index.json'):
        print("Warning: No index found. Creating demo index...")
        demo_search()

    print("\n" + "=" * 70)
    print("Starting web server...")
    print("=" * 70)
    print("\nOpen your browser and navigate to: http://localhost:5000")
    print("Press Ctrl+C to stop the server.\n")

    from web_app import app, initialize_search_engine
    initialize_search_engine()
    app.run(debug=False, host='0.0.0.0', port=5000)


def main():
    parser = argparse.ArgumentParser(
        description='Educational Search Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py demo                                    - Run with sample data
  python main.py crawl https://en.wikipedia.org/wiki/Python  - Crawl Wikipedia
  python main.py search "search algorithm"               - Search from command line
  python main.py serve                                   - Start web interface
        """
    )

    parser.add_argument('command', choices=['crawl', 'demo', 'search', 'serve'],
                        help='Command to execute')
    parser.add_argument('args', nargs='*', help='Arguments for the command')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Maximum pages to crawl (default: 50)')
    parser.add_argument('--all-domains', action='store_true',
                        help='Crawl across different domains')

    args = parser.parse_args()

    if args.command == 'crawl':
        if not args.args:
            print("Error: Please provide a URL to crawl")
            print("Example: python main.py crawl https://example.com")
            sys.exit(1)
        crawl_and_index(args.args[0], max_pages=args.max_pages,
                        same_domain=not args.all_domains)

    elif args.command == 'demo':
        demo_search()

    elif args.command == 'search':
        if not args.args:
            print("Error: Please provide a search query")
            print("Example: python main.py search 'python programming'")
            sys.exit(1)
        search_cli(' '.join(args.args))

    elif args.command == 'serve':
        serve()


if __name__ == '__main__':
    main()

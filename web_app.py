"""
Flask Web Interface for Search Engine
"""

from flask import Flask, render_template, request, jsonify
from search_engine import SearchEngine
from indexer import SearchIndexer
import os

app = Flask(__name__)

# Global search engine instance
search_engine = None
indexer = None


def initialize_search_engine():
    """Initialize or load the search engine index."""
    global search_engine, indexer

    indexer = SearchIndexer()
    index_file = 'search_index.json'

    if os.path.exists(index_file):
        print(f"Loading existing index from {index_file}...")
        indexer.load_index(index_file)
    else:
        print("No index found. Please run 'python main.py crawl' first to build an index.")

    search_engine = SearchEngine(indexer)


@app.route('/')
def home():
    """Render the search homepage."""
    stats = indexer.get_index_stats() if indexer else {}
    return render_template('index.html', stats=stats)


@app.route('/search')
def search():
    """Handle search queries."""
    query = request.args.get('q', '').strip()

    if not query:
        return render_template('results.html', query='', results=[], count=0)

    # Perform search
    results = search_engine.search(query, top_k=20)

    return render_template('results.html', query=query, results=results, count=len(results))


@app.route('/api/search')
def api_search():
    """API endpoint for search."""
    query = request.args.get('q', '').strip()
    top_k = int(request.args.get('limit', 10))

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    results = search_engine.search(query, top_k=top_k)

    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })


@app.route('/api/suggest')
def api_suggest():
    """API endpoint for search suggestions."""
    prefix = request.args.get('q', '').strip()

    if not prefix or len(prefix) < 2:
        return jsonify({'suggestions': []})

    suggestions = search_engine.get_suggestions(prefix, max_suggestions=5)

    return jsonify({'suggestions': suggestions})


@app.route('/stats')
def stats():
    """Show index statistics."""
    if not indexer:
        return "No index loaded", 404

    stats = indexer.get_index_stats()
    return render_template('stats.html', stats=stats)


if __name__ == '__main__':
    initialize_search_engine()
    app.run(debug=True, host='0.0.0.0', port=5000)

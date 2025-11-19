# Educational Search Engine

A fully-functional search engine built from scratch to demonstrate how search engines work. This project implements the core principles of modern search engines including web crawling, indexing, TF-IDF ranking, and a web interface.

## Features

### Core Search Engine Components

1. **Web Crawler** (`crawler.py`)
   - Discovers and fetches web pages by following links
   - Respects politeness policies with configurable delays
   - Extracts HTML content and metadata
   - Supports same-domain or cross-domain crawling

2. **Inverted Index** (`indexer.py`)
   - Maps terms to documents for fast lookup
   - Tokenizes and processes text content
   - Removes stop words and normalizes terms
   - Stores document metadata and statistics

3. **TF-IDF Ranking** (`indexer.py`)
   - **Term Frequency (TF)**: Measures how often a term appears in a document
   - **Inverse Document Frequency (IDF)**: Measures how rare a term is across all documents
   - Combines TF and IDF to score document relevance
   - Boosts title matches for better results

4. **Query Processor** (`search_engine.py`)
   - Processes search queries and returns ranked results
   - Supports multi-term queries
   - Provides search suggestions based on indexed terms
   - Fast retrieval using the inverted index

5. **Web Interface** (`web_app.py`, `templates/`)
   - Clean, modern search interface
   - Real-time search results
   - Index statistics dashboard
   - RESTful API for programmatic access

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd search-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start - Demo Mode

Run the search engine with sample documents:

```bash
python main.py demo
```

This will create an index with educational content about search engines and demonstrate search functionality.

### Crawl a Website

Crawl and index a website (e.g., Wikipedia):

```bash
python main.py crawl https://en.wikipedia.org/wiki/Search_engine --max-pages 20
```

Options:
- `--max-pages N`: Limit crawling to N pages (default: 50)
- `--all-domains`: Allow crawling across different domains (default: same domain only)

### Start Web Interface

Launch the web-based search interface:

```bash
python main.py serve
```

Then open your browser to: `http://localhost:5000`

### Command-Line Search

Search directly from the command line:

```bash
python main.py search "search engine algorithm"
```

## How It Works

### 1. Web Crawling

The crawler starts with seed URLs and:
- Fetches the HTML content
- Extracts text and links
- Follows links to discover new pages
- Continues until max pages reached

```python
from crawler import WebCrawler

crawler = WebCrawler(max_pages=50, delay=0.5)
pages = crawler.crawl(['https://example.com'], same_domain=True)
```

### 2. Indexing

The indexer processes each page:
- Tokenizes text into terms
- Removes stop words
- Builds an inverted index: `term → {doc_id: frequency}`
- Stores document metadata

```python
from indexer import SearchIndexer

indexer = SearchIndexer()
indexer.add_document(doc_id='1', title='Example', content='...', url='...')
indexer.calculate_tfidf()
```

### 3. TF-IDF Scoring

For each term in each document:

```
TF-IDF = (term_freq / doc_length) × log(total_docs / docs_with_term)
```

- **High TF**: Term appears frequently in document
- **High IDF**: Term is rare across all documents
- **High TF-IDF**: Term is important to this specific document

### 4. Searching

When a user searches:
1. Query is tokenized into terms
2. For each term, retrieve documents from inverted index
3. Sum TF-IDF scores across all query terms
4. Sort by total score (descending)
5. Return top K results

```python
from search_engine import SearchEngine

engine = SearchEngine(indexer)
results = engine.search("python programming", top_k=10)
```

## Project Structure

```
search-engine/
├── main.py              # Main entry point
├── crawler.py           # Web crawler implementation
├── indexer.py           # Inverted index and TF-IDF
├── search_engine.py     # Query processor
├── web_app.py           # Flask web application
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   └── stats.html
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

## API Endpoints

### Search API

```bash
GET /api/search?q=<query>&limit=<n>
```

Response:
```json
{
  "query": "search engine",
  "count": 5,
  "results": [
    {
      "doc_id": "doc_0",
      "title": "How Search Engines Work",
      "url": "https://example.com/page",
      "snippet": "Search engines are...",
      "score": 0.8234,
      "matched_terms": ["search", "engine"]
    }
  ]
}
```

### Suggestions API

```bash
GET /api/suggest?q=<prefix>
```

Response:
```json
{
  "suggestions": ["search", "searching", "searchable"]
}
```

## Educational Value

This project demonstrates:

1. **Data Structures**
   - Inverted index (hash map of hash maps)
   - Document store
   - Term frequency counters

2. **Algorithms**
   - TF-IDF scoring
   - Text tokenization and normalization
   - Result ranking

3. **Web Technologies**
   - HTTP requests and HTML parsing
   - RESTful API design
   - Server-side rendering with Flask

4. **Software Engineering**
   - Modular design with separation of concerns
   - Persistence (JSON serialization)
   - Command-line interfaces

## Limitations

This is an educational project and has limitations compared to production search engines:

- No distributed indexing
- No real-time updates
- Simple tokenization (no stemming or lemmatization)
- No PageRank or link analysis
- No query optimization
- Limited scalability
- No caching layer

## Future Enhancements

Possible improvements to learn more:

1. **Better Text Processing**
   - Stemming/lemmatization (using NLTK)
   - N-gram support
   - Language detection

2. **Advanced Ranking**
   - PageRank algorithm
   - BM25 scoring
   - Machine learning ranking

3. **Performance**
   - Database backend (SQLite, PostgreSQL)
   - Caching with Redis
   - Parallel crawling

4. **Features**
   - Autocomplete
   - Spell checking
   - Image search
   - PDF indexing

## Learning Resources

- [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/)
- [How Search Engines Work](https://www.google.com/search/howsearchworks/)
- [TF-IDF Explained](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [Building a Simple Search Engine](https://bart.degoe.de/building-a-full-text-search-engine-150-lines-of-code/)

## License

This project is for educational purposes. Feel free to use and modify for learning.

## Contributing

This is an educational project. Contributions that improve learning value are welcome!

## Author

Built as an educational demonstration of search engine principles.

# Quick Start Guide

Get your search engine up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP client for crawling
- `flask` - Web framework
- `nltk` - Natural language processing (optional)

## Step 2: Run Demo

```bash
python main.py demo
```

This will:
1. Create sample documents about search engines
2. Build an inverted index
3. Calculate TF-IDF scores
4. Run example searches
5. Save the index to `search_index.json`

## Step 3: Start Web Interface

```bash
python main.py serve
```

Open your browser to: **http://localhost:5000**

Now you can:
- Search the indexed documents
- View search statistics
- See how relevance scoring works

## What You'll Learn

### Core Concepts

1. **Web Crawling**
   - How search engines discover content
   - Following links to find new pages
   - Being polite with delays between requests

2. **Inverted Index**
   - Data structure: term → [documents]
   - Enables fast full-text search
   - Example: "python" → [doc1, doc5, doc8]

3. **TF-IDF Ranking**
   - **TF (Term Frequency)**: How often does a term appear in a document?
   - **IDF (Inverse Document Frequency)**: How rare is the term across all documents?
   - **Score = TF × IDF**: Terms that are common in one doc but rare overall rank higher

4. **Query Processing**
   - Breaking queries into terms
   - Looking up terms in the index
   - Scoring and ranking results

## Example Workflow

### Crawl a Real Website

```bash
# Crawl Wikipedia (limited to 20 pages)
python main.py crawl https://en.wikipedia.org/wiki/Python_(programming_language) --max-pages 20

# Start the web interface
python main.py serve
```

### Command-Line Search

```bash
# After building an index
python main.py search "programming language"
```

Output:
```
Search results for: 'programming language'
======================================================================

1. Python Programming Language
   URL: https://en.wikipedia.org/wiki/Python_(programming_language)
   Score: 1.2345
   Matched terms: programming, language
   Python is a high-level programming language...
```

## Architecture Overview

```
┌─────────────┐
│  Web Pages  │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│   Crawler   │────▶│   Documents  │
└─────────────┘     └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Indexer    │
                    │  (TF-IDF)    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │Inverted Index│
                    └──────┬───────┘
                           │
    ┌──────────────────────┴────────────────────┐
    │                                            │
    ▼                                            ▼
┌──────────┐                              ┌──────────┐
│   API    │                              │   Web UI │
└──────────┘                              └──────────┘
```

## Understanding the Code

### 1. Crawler (crawler.py)

```python
crawler = WebCrawler(max_pages=10)
pages = crawler.crawl(['https://example.com'])
# Returns: [{'url': '...', 'title': '...', 'content': '...', 'links': [...]}]
```

### 2. Indexer (indexer.py)

```python
indexer = SearchIndexer()
indexer.add_document('doc1', 'Title', 'Content here...', 'http://url')
indexer.calculate_tfidf()
```

### 3. Search Engine (search_engine.py)

```python
engine = SearchEngine(indexer)
results = engine.search("query here", top_k=10)
# Returns ranked results with scores
```

## Next Steps

1. **Experiment with Crawling**
   - Try different websites
   - Adjust `--max-pages` to control index size
   - Use `--all-domains` to crawl across sites

2. **Understand the Index**
   - Look at `search_index.json` to see the data structure
   - Check `/stats` in the web interface

3. **Modify the Code**
   - Add new stop words in `indexer.py`
   - Change title weight (currently 3x)
   - Improve tokenization

4. **Build Features**
   - Add autocomplete
   - Implement spell checking
   - Create a database backend

## Troubleshooting

**No results found?**
- Make sure you ran `demo` or `crawl` first
- Check that `search_index.json` exists
- Try simpler, more common terms

**Crawler not working?**
- Check your internet connection
- Some sites block crawlers
- Try a different URL

**Port 5000 already in use?**
- Change port in `web_app.py`: `app.run(port=8080)`
- Or stop the process using port 5000

## Have Fun Learning!

This project demonstrates the fundamentals that power modern search engines like Google, Bing, and DuckDuckGo. While production search engines are much more complex, the core principles are the same.

Happy searching!

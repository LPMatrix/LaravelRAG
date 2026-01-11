# Laravel RAG

A Retrieval-Augmented Generation (RAG) system for querying Laravel documentation using Ollama and ChromaDB.

## Overview

This project allows you to chat with the Laravel documentation. It ingests markdown files from the documentation, stores them in a vector database (ChromaDB), and uses a local LLM (via Ollama) to answer questions based on the documentation context.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running.

### Required Ollama Models

You need to pull the following models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

## Installation

1.  Clone the repository.
2.  Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Ingest Documentation

The project expects Laravel documentation markdown files in the `laravel-docs/` directory.

Run the ingestion script to process the documents and create the vector database:

```bash
python ingest.py
```

This script will:
- Read markdown files from `laravel-docs/`.
- Chunk the text.
- Generate embeddings using `nomic-embed-text`.
- Store the embeddings in a local ChromaDB instance (`./chroma_db`).

### 2. Query the Documentation

Start the interactive CLI to ask questions:

```bash
python query.py
```

Type your question when prompted. The system will:
- Search for relevant documentation chunks.
- Use `llama3.2` to generate an answer based on the retrieved context.
- Display the answer and the source files used.

## Project Structure

- `ingest.py`: Script to process documentation and populate the vector database.
- `query.py`: Script to run the interactive query interface.
- `requirements.txt`: Python dependencies.
- `laravel-docs/`: Directory containing the Laravel documentation markdown files.
- `chroma_db/`: (Created after ingestion) Directory storing the vector database.

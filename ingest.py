import os
import ollama
import chromadb
from pathlib import Path

DOCS_PATH = "laravel-docs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def read_markdown_files(docs_path):
    md_files = []
    for filepath in Path(docs_path).rglob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            md_files.append({
                'path': str(filepath),
                'content': content
            })
    return md_files

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def generate_embeddings(text):
    response = ollama.embeddings(model='nomic-embed-text', prompt=text)
    return response['embedding']

def main():
    print("Reading markdown files...")
    docs = read_markdown_files(DOCS_PATH)
    print(f"Found {len(docs)} markdown files")
    
    print("Chunking documents...")
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc['content'])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                'text': chunk,
                'source': doc['path'],
                'chunk_id': i
            })
    print(f"Created {len(all_chunks)} chunks")
    
    print("Generating embeddings and storing in ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        client.delete_collection("laravel_docs")
    except:
        pass
    
    collection = client.create_collection("laravel_docs")
    
    for i, chunk in enumerate(all_chunks):
        if i % 10 == 0:
            print(f"Processing chunk {i}/{len(all_chunks)}")
        
        embedding = generate_embeddings(chunk['text'])
        collection.add(
            embeddings=[embedding],
            documents=[chunk['text']],
            metadatas=[{'source': chunk['source'], 'chunk_id': chunk['chunk_id']}],
            ids=[f"{chunk['source']}_{chunk['chunk_id']}"]
        )
    
    print("Done! Vector database created.")

if __name__ == "__main__":
    main()
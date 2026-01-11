import ollama
import chromadb

def generate_embedding(text):
    response = ollama.embeddings(model='nomic-embed-text', prompt=text)
    return response['embedding']

def retrieve_relevant_chunks(query, n_results=5):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("laravel_docs")
    
    query_embedding = generate_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

def generate_response(query, context_chunks):
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are a helpful assistant that answers questions about Laravel based on the official documentation.

Context from Laravel documentation:
{context}

Question: {query}

Answer the question based on the context provided. If the context doesn't contain enough information to answer the question, say so."""
    
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']

def main():
    print("Laravel Documentation RAG System")
    print("=" * 50)
    
    while True:
        query = input("\nAsk a question (or 'quit' to exit): ")
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        print("\nRetrieving relevant documentation...")
        results = retrieve_relevant_chunks(query)
        
        chunks = results['documents'][0]
        sources = results['metadatas'][0]
        
        print(f"Found {len(chunks)} relevant chunks")
        print("\nSources:")
        for source in sources:
            print(f"  - {source['source']}")
        
        print("\nGenerating response...")
        answer = generate_response(query, chunks)
        
        print("\n" + "=" * 50)
        print("Answer:")
        print(answer)
        print("=" * 50)

if __name__ == "__main__":
    main()
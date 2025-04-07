from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Chunks text into smaller segments
def chunkText(text, maxWords=150, overlap=50):
    words = text.split()
    chunks = []
    
    # Clean and normalize text before chunking
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Create overlapping chunks
    for i in range(0, len(words), maxWords - overlap):
        chunk = " ".join(words[i:i + maxWords])
        # Only include chunks with substantial content
        if len(chunk.split()) > 20:  
            chunks.append(chunk)
    
    return chunks

# Creates embeddings for the text chunks
def createEmbeddings(papers):
    embedder = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
    chunks = []
    
    for idx, paper in enumerate(papers):
        # Split paper into paragraphs first
        paragraphs = re.split(r'\n\s*\n', paper)
        
        for paraIdx, para in enumerate(paragraphs):
            if len(para.strip()) < 50:  # Skip very short paragraphs
                continue
                
            for c in chunkText(para):
                # Normalize metadata and content
                normalizedContent = re.sub(r'\s+', ' ', c).strip()
                chunks.append({
                    "paperId": idx + 1,
                    "paragraphId": paraIdx,
                    "content": normalizedContent,
                    "embedding": embedder.encode(normalizedContent, normalize_embeddings=True)
                })
    
    return chunks

# Retrieves relevant chunks based on the query using cosine similarity
def retrieveRelevantChunks(query, chunks, topK=5, threshold=0.25):
    embedder = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
    
    # Normalize and encode the query
    query = re.sub(r'\s+', ' ', query).strip()
    queryEmb = embedder.encode(query, normalize_embeddings=True)
    
    # Calculate similarities
    similarities = []
    for chunk in chunks:
        simScore = cosine_similarity([queryEmb], [chunk['embedding']])[0][0]
        # Only add chunks that meet the threshold criteria
        if simScore >= threshold:
            similarities.append((chunk, simScore))
    
    # Sort by similarity
    ranked = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    # If we don't have enough results above threshold, adjust the message
    if len(ranked) == 0:
        print(f"Warning: No chunks found with similarity above threshold {threshold}")
        # Fall back to top results but with a higher threshold to avoid completely irrelevant content
        for chunk in chunks:
            simScore = cosine_similarity([queryEmb], [chunk['embedding']])[0][0]
            if simScore >= threshold * 0.6:  # Use slightly lower threshold as fallback
                similarities.append((chunk, simScore))
        ranked = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    # Limit to topK results
    ranked = ranked[:topK]
    
    # Add score to each chunk and store global scores for main.py
    global rankedScores
    rankedScores = [r[1] for r in ranked]
    
    # Add score to each chunk
    resultChunks = []
    for chunk, score in ranked:
        chunkCopy = chunk.copy()  # Create a copy to avoid modifying the original
        chunkCopy['score'] = score
        resultChunks.append(chunkCopy)
    
    # Print some debug info about similarity scores
    print(f"Top similarity scores: {[round(r[1], 2) for r in ranked]}")
    print(f"Number of chunks retrieved: {len(resultChunks)}")
    
    return resultChunks

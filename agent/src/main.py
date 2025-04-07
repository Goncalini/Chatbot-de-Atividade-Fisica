import pickle  # For saving and loading embeddings
from LLMClient import LLMClient
from embeddings import createEmbeddings, retrieveRelevantChunks
import os
import utils

def main():
    
    # Define paths for the original data and its embeddings
    dataPaths = [f"papers/paper{i}.txt" for i in range(1, 6)]
    embeddingsFilePaths = "embeddings/embeddings.pkl" 
    
    # Check if the embeddings file exists
    if os.path.exists(embeddingsFilePaths):
        print("Loading existing embeddings...")
        with open(embeddingsFilePaths, "rb") as f:
            chunks = pickle.load(f)
            
    else:
        print("Generating new embeddings...")
        papers = utils.loadFiles(dataPaths)
        chunks = createEmbeddings(papers)
        
        # Save the embeddings to a file
        with open(embeddingsFilePaths, "wb") as f:
            pickle.dump(chunks, f)
    
    # Read the context prompt from file
    with open("config/contextPrompt.txt", "r", encoding="utf-8") as f:
        contextPrompt= f.read()
    
    # Initialize the LLM client
    llmClient = LLMClient()

    while True:
        # Prompt the user for a question
        prompt = input("\n\nDigite a sua pergunta (ou 'EXIT' para sair): \n>>>")
        if prompt.strip().upper() == "EXIT":
            break
        
        # Retrieve relevant chunks using the embeddings
        relevantChunks = retrieveRelevantChunks(prompt, chunks, topK=5)
        
        # Format the context for the LLM
        context = "\n\n".join([f"Paper {c['paperId']}:\n{c['content']}" for c in relevantChunks])
        
        # Create the final prompt for the LLM
        finalPrompt = (
            f"{contextPrompt}\n\n"
            "### Pergunta:\n"
            f"{prompt}\n\n"
            "### Contexto de artigos:\n"
            f"{context}"
        )

        # Debugging output
        print("\nContexto RAG:")
        print(finalPrompt)
        print("########")
        print("########")
        print("########\n")
        
        
        # Get the LLM response
        response = llmClient.generateResponse(finalPrompt)

        print("Resposta do LLM:")
        print(response)

if __name__ == "__main__":
    main()

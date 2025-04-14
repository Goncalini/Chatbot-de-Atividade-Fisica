import json
import scispacy
import spacy
from transformers import AutoTokenizer

# Carregar modelos
nlp = spacy.load("en_core_sci_lg")
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en")

# Função para dividir texto em chunks
def split_into_chunks(text, max_length=150, max_tokens=512):
    doc = nlp(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sent in doc.sents:
        sent_text = sent.text.strip()
        sent_tokens = len(tokenizer.tokenize(sent_text))
        if sent_tokens > max_length:
            words = sent_text.split()
            sub_chunk = []
            sub_length = 0
            for word in words:
                word_tokens = len(tokenizer.tokenize(word))
                if sub_length + word_tokens <= max_length:
                    sub_chunk.append(word)
                    sub_length += word_tokens
                else:
                    if sub_chunk:
                        chunks.append(" ".join(sub_chunk))
                    sub_chunk = [word]
                    sub_length = word_tokens
            if sub_chunk:
                chunks.append(" ".join(sub_chunk))
        else:
            if current_length + sent_tokens <= max_length and current_length + sent_tokens <= max_tokens:
                current_chunk.append(sent_text)
                current_length += sent_tokens
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sent_text]
                current_length = sent_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Verificar se o número total de tokens não excede o limite
    final_chunks = []
    for chunk in chunks:
        if len(tokenizer.tokenize(chunk)) <= max_tokens:
            final_chunks.append(chunk)

    return final_chunks


def process_pubmed(input_data):
    output = []
    paper_count = 1922

    for item in input_data:
        try:
            chunks = split_into_chunks(item["abstract"])
        except Exception as e:
            print(f"Ignorar entrada com erro: {e}")
            continue

        for idx, chunk in enumerate(chunks):
            output.append({
                "chunk_id": f"Paper{paper_count}Chunk{idx}",
                "chunk_text": chunk,
                "title": item["title"],
                "link": item["link"],
                "year": item["year"],
                "topic": item["topic"],
                "hierarchical_level": 1
            })

        paper_count += 1

    return output


def process_google (data, path):
    output = []
    paper_count = 1922

    for item in data:
        id = item.get("id")
        
        if id is None:
            print(f"ID não encontrado para o item: {item}")
            continue

        pdf_path = f"{path}/{id}.pdf"

        try:
            with open(pdf_path, "r", encoding="utf-8") as pdf_file:
                pdf_text = pdf_file.read()
        except FileNotFoundError:
            print(f"PDF não encontrado para o item: {item}")
            continue

        chunks = split_into_chunks(pdf_text)

        for idx, chunk in enumerate(chunks):
            output.append({
                "chunk_id": f"Paper{paper_count}Chunk{idx}",
                "chunk_text": chunk,
                "title": item["title"],
                "link": item["link"],
                "year": item["year"],
                "topic": item["topic"],
                "hierarchical_level": 1
            })

        paper_count += 1

    return output


# Exemplo de uso
if __name__ == "__main__":
    # PubMed
    with open("../json/pubmed_abstracts.json", "r", encoding="utf-8") as infile:
        data = json.load(infile)

    processed_pubmed = process_pubmed(data)
    
    with open("../chunkedData/pubmed_chunks.json", "w", encoding="utf-8") as outfile:
        json.dump(processed_pubmed, outfile, indent=4)
    
    # Google Scholar
    with open("../json/google_scholar_papers1.json", "r", encoding="utf-8") as infile:
        data = json.load(infile)

    processed_google = process_google(data, "../PDF_Text")

    with open("../chunkedData/google_chunks.json", "w", encoding="utf-8") as outfile:
        json.dump(processed_google, outfile, indent=4)

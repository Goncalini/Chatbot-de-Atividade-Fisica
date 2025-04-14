import json

# Caminho para o ficheiro original
input_file = "google_scholar_papers.json"
output_file = "output_with_ids.json"

# Abrir e carregar o JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Adicionar o campo "id" a cada item
for i, item in enumerate(data, start=1):
    item["id"] = i

# Guardar o novo JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"IDs adicionados com sucesso e guardados em {output_file}")
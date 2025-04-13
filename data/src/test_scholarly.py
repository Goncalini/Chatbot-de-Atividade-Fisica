from scholarly import scholarly

query = scholarly.search_pubs("benefits of physical activity on health")
try:
    paper = next(query)
    print(paper['bib']['title'])
except Exception as e:
    print("Erro:", e)

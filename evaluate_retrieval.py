import json
import chromadb
import ollama

try:
    with open("eval_benchmark.json") as f:
        benchmark = json.load(f)
except FileNotFoundError:
    print("❌ Run generate_eval_dataset.py first!")
    exit()

chroma_client = chromadb.PersistentClient(path="./course_tutor_db")
collection = chroma_client.get_collection(name="pdf_course_materials")

hits = 0
reciprocal_ranks = []

for item in benchmark:
    query = item["query"]
    target_id = item["expected_doc_id"]
    
    q_embed = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    results = collection.query(query_embeddings=[q_embed], n_results=3)
    retrieved_ids = results["ids"][0] if results["ids"] else []
    
    if target_id in retrieved_ids:
        hits += 1
        rank = retrieved_ids.index(target_id) + 1
        reciprocal_ranks.append(1.0 / rank)
    else:
        reciprocal_ranks.append(0.0)

hit_rate = hits / len(benchmark) if benchmark else 0
mrr = sum(reciprocal_ranks) / len(benchmark) if benchmark else 0

print(f"📊 Retrieval Evaluation Results:")
print(f" - Hit Rate @ 3: {hit_rate * 100:.2f}%")
print(f" - MRR @ 3:      {mrr:.4f}")
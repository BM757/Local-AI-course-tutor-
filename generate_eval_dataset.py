import json
import chromadb
import ollama

chroma_client = chromadb.PersistentClient(path="./course_tutor_db")
collection = chroma_client.get_collection(name="pdf_course_materials")

data = collection.get(limit=20)
eval_dataset = []

if data["documents"]:
    for doc, meta in zip(data["documents"], data["metadatas"]):
        prompt = f"""
        You are an academic test designer. Based ONLY on the following course text from Page {meta['page']}:
        ---
        {doc}
        ---
        Generate:
        1. A clear student question.
        2. The exact reference answer.

        Format output strictly as JSON with keys: "query", "ground_truth".
        """
        
        res = ollama.chat(
            model="llama3.2", 
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        
        qa_pair = json.loads(res["message"]["content"])
        qa_pair["expected_doc_id"] = f"{meta['source']}_page_{meta['page']}"
        eval_dataset.append(qa_pair)

    with open("eval_benchmark.json", "w") as f:
        json.dump(eval_dataset, f, indent=2)
    print("✅ Benchmark dataset generated: eval_benchmark.json")
else:
    print("❌ No indexed materials found in ChromaDB.")
import json
import ollama

def judge_answer(query, generated_answer, reference_answer):
    judge_prompt = f"""
    You are an academic evaluator. 
    Evaluate the Candidate Answer against the Reference Answer for the given Query.

    Query: {query}
    Reference Answer: {reference_answer}
    Candidate Answer: {generated_answer}

    Assign a score from 1 to 5 based on semantic accuracy.
    Output strictly in JSON format: {{"score": <number>, "reason": "<string>"}}
    """
    
    res = ollama.chat(
        model="llama3.2", 
        messages=[{"role": "user", "content": judge_prompt}],
        format="json"
    )
    return json.loads(res["message"]["content"])

if __name__ == "__main__":
    sample_eval = judge_answer(
        query="What is Backpropagation?",
        generated_answer="Backpropagation calculates gradient of the loss function.",
        reference_answer="It is an algorithm used to compute gradients in neural networks."
    )
    print("⚖️ Judge Evaluation Result:", sample_eval)
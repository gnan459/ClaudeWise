#Simplify complex legal clauses into plain English.

# clause_simplifier.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class ClauseSimplifier:
    def __init__(self, model_name="google/flan-t5-large"):
        print("[INFO] Loading simplification model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def simplify_clause(self, clause: str, max_length: int = 100) -> str:
        """
        Simplifies a legal clause using a T5-style instruction model.
        """
        prompt = f"simplify: {clause}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

        outputs = self.model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_beams=4,
            early_stopping=True
        )

        simplified_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return simplified_text

    def simplify_clauses(self, clause_list):
        """
        Simplifies a list of clauses and returns a list of simplified outputs.
        """
        return [self.simplify_clause(clause) for clause in clause_list]

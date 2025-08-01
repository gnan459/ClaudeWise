#Break down a large legal document into individual clauses.

from transformers import AutoTokenizer, AutoModel
import torch
import nltk
from sklearn.cluster import KMeans
import numpy as np

# Download NLTK sentence tokenizer
nltk.download('punkt_tab')

class ClauseExtractor:
    def __init__(self, model_name="nlpaueb/legal-bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def _get_cls_embedding(self, sentence):
        """Extract [CLS] token embedding for a given sentence."""
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]  # CLS token
        return cls_embedding.squeeze(0).numpy()

    def extract_clauses(self, document_text, n_clusters=5):
        """Split document into sentences and group similar ones into clauses."""
        # Step 1: Sentence Tokenization
        sentences = nltk.sent_tokenize(document_text)

        # Step 2: Get CLS embeddings for all sentences
        embeddings = np.array([self._get_cls_embedding(sent) for sent in sentences])

        # Step 3: KMeans clustering to group similar sentences (optional)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)

        # Step 4: Group sentences by cluster label
        clauses = {}
        for idx, label in enumerate(labels):
            clauses.setdefault(label, []).append(sentences[idx])

        # Step 5: Format clauses
        extracted_clauses = [" ".join(group) for group in clauses.values()]
        return extracted_clauses

# # Example usage
# if __name__ == "__main__":
#     sample_text = """
#     This Agreement is made effective as of the date signed below.
#     The Parties agree to the terms set forth herein.
#     Confidentiality must be maintained at all times.
#     The recipient shall not disclose any confidential information to third parties.
#     This Agreement shall be governed by the laws of the State of California.
#     """
#     extractor = ClauseExtractor()
#     clauses = extractor.extract_clauses(sample_text, n_clusters=3)

#     for i, clause in enumerate(clauses):
#         print(f"\nClause {i+1}:\n{clause}")

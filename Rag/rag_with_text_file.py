
from google import genai
import numpy as np

client = genai.Client()

# 1. Read content from TXT file
with open("Rag\match.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("Text file loaded successfully!")

# 2. Split text into chunks
def split_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


Documents = split_text(text)

print("Total chunks:", len(Documents))

# 3. Create document embeddings
document_vectors = []

for document in Documents:
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=document
    )

    vector = result.embeddings[0].values
    document_vectors.append(vector)

# 4. Get question from user
question = input("Ask a question about the match: ")

question_result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

ques_vector = question_result.embeddings[0].values

# 5. Cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return np.dot(a, b) / denominator


# 6. Compare question with document chunks
scores = []

for vector, document in zip(document_vectors, Documents):
    score = cosine_similarity(ques_vector, vector)
    scores.append(score)

# 7. Retrieve the best chunk
best_index = np.argmax(scores)
best_doc = Documents[best_index]

#whprint("\nRetrieved Context:")
#print(best_doc)

# 8. Send retrieved context to Gemini
prompt = f"""
Answer the question by giving priority to provided context.
If the answer is not present don't mention "based on content" , If you known answer tell otherwise
do not invent facts.

Context:
{best_doc}

Question:
{question}
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

# 9. Display final answer
print("\nFinal Answer:")
print(response.text)

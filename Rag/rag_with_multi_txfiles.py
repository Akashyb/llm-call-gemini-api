
from google import genai
import numpy as np
import os
import glob

client = genai.Client()

# 1. Get the documents folder path
base_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_path, "documents_text")

# 2. Read all TXT files
Documents = []
document_sources = []

file_paths = glob.glob(os.path.join(folder_path, "*.txt"))

if not file_paths:
    raise FileNotFoundError(
        f"No TXT files found in: {folder_path}"
    )

for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Split each file into chunks
    chunk_size = 500
    overlap = 100
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size].strip()

        if chunk:
            Documents.append(chunk)
            document_sources.append(os.path.basename(file_path))

        start += chunk_size - overlap

print("Files loaded:", len(file_paths))
print("Total chunks:", len(Documents))

# 3. Create embeddings for all chunks
document_vectors = []

for document in Documents:
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=document
    )

    vector = result.embeddings[0].values
    document_vectors.append(vector)

# 4. Cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return np.dot(a, b) / denominator


# 5. Ask questions continuously
while True:
    question = input("\nAsk your question (type 'exit' to stop): ")

    # Stop the program
    if question.lower().strip() == "exit":
        print("Exiting the RAG system. Goodbye!")
        break

    if not question.strip():
        print("Please enter a question.")
        continue

    # 6. Create embedding for the question
    question_result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=question
    )

    ques_vector = question_result.embeddings[0].values

    # 7. Calculate similarity scores
    scores = []

    for vector in document_vectors:
        score = cosine_similarity(ques_vector, vector)
        scores.append(score)

    # 8. Retrieve the best matching chunk
    best_index = np.argmax(scores)

    best_doc = Documents[best_index]
    best_source = document_sources[best_index]

    context = f"""
    Source: {best_source}
    Content: {best_doc}
    """

    # 9. Generate the answer
    prompt = f"""
    Answer the question by giving priority to provided context.
    If the answer is not present don't mention "based on content" , If you known answer tell otherwise
    do not invent facts.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    #print("\nRetrieved source:", best_source)
    print("Final answer:")
    print(response.text)


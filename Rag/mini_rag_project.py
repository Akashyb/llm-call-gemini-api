from google import genai
import numpy as np

client=genai.Client()

Documents=[
          "Refund requests are accepted within 7 days of purchase",
          "Eligible students get minimum 3 interveiw opportunities",
          "Our Data Analyst Course last for 6 months",
          "Python Classess happen Monday to Friday"
          ]

question="How many interviews opportunities provided for eligiable Students?"

### Document embedding

document_vector=[]

for document in Documents:
    result=client.models.embed_content(
        model="gemini-embedding-2",
        contents=document
    )
    vector=result.embeddings[0].values
    document_vector.append(vector)


### question embedding

question_result=client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)
ques_vector=question_result.embeddings[0].values


### comparing embeddings


def cosine_similarity(a,b):
    a=np.array(a)
    b-np.array(b)
    
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))

### score storing

scores=[]
for vector,document in zip(document_vector,Documents):
    score=cosine_similarity(ques_vector,vector)
    scores.append(score)
    #print(score,document)

### Retrieve best chunk

best_index=np.argmax(scores)
best_doc=Documents[best_index]

#print(best_doc)

### send Retrieved chunk to llm

prompt=f"""
Answer the questions based on your information if not found check context then answer
don't say "based on context" for every question
if fetch from context then say "Based on course provider" 
 
Context:{best_doc}

Question:
{question}

"""

### generate final answer

response=client.models.generate_content(
    
    model="gemini-3.5-flash",
    contents=prompt
)

print("\n Final answer")
print(response.text)

from google import genai
import numpy as np

client=genai.Client()

Documents=[
          "Refund requests are accepted within 7 days of purchase",
          "Eligible students get minimum 3 interveiw opportunities",
          "Our Data Analyst Course last for 6 months",
          "Python Classess happen Monday to Friday"
          ]

question="What is the duration of course?"

document_vector=[]

for document in Documents:
    result=client.models.embed_content(
        model="gemini-embedding-2",
        contents=document
    )
    vector=result.embeddings[0].values
    document_vector.append(vector)
    
question_result=client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)
ques_vector=question_result.embeddings[0].values

def cosine_similarity(a,b):
    a=np.array(a)
    b-np.array(b)
    
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))
scores=[]
for vector,document in zip(document_vector,Documents):
    score=cosine_similarity(ques_vector,vector)
    scores.append(score)
    print(score,document)

best_index=np.argmax(scores)
best_doc=Documents[best_index]

print(best_doc)
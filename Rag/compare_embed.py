from google import genai
import numpy as np

client=genai.Client()

text1="Refund request are allowed within 7 days"
text2="Can I get money back after 5 days"
result1 =client.models.embed_content(
    
    model="gemini-embedding-2",
    contents=text1
)
result2 =client.models.embed_content(
    
    model="gemini-embedding-2",
    contents=text2
)

vector1=result1.embeddings[0].values
vector2=result2.embeddings[0].values

print(len(vector1),len(vector2))

def cosine_similarity(a,b):
    a=np.array(a)
    b=np.array(b)
    
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

score=cosine_similarity(vector1,vector2)

print(score)
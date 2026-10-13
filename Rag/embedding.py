from google import genai

client=genai.Client()

result =client.models.embed_content(
    
    model="gemini-embedding-2",
    contents="Refund request are allowed within 7 days"
)
print(result.embeddings)

# convert result as vector

vector=result.embeddings[0].values
print(vector)

### result.embeddings is collection of embedding objects\
    
multiple_embed="""
if content contains multiple chunk
then embeddings[0] for first chunk
llly embbeddings[1] fro second chunk so on

vector=[embeddind.vlues for embedding in result.embeddings]

"""

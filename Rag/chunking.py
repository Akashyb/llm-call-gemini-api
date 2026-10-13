text="""
Our Data Analyst Course last for 6 months.
Students get access to all recorded classess.
Live classess happen from Monday to Friday.
Refund requests are accepted within 7 days of purchase.
Students must complete all assignments before placement support starts.
Eligible students get minimum 3 interveiw opportunities.

"""

lines=text.strip().split("\n") #split by lines
chunks=[]

for i in range(0,len(lines),2):
    chunk=" ".join(lines[i:i+2])
    chunks.append(chunk)

for chun in chunks:
    print("Chunk")
    print(chun)
    print()

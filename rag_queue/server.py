from fastapi import FastAPI, Query
from .queue.connection import queue 
from .queue.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status":"Server is up and running"}

@app.post("/chat")
def chat(query:str=Query(...,description="chat message")):
    #Insert the query to the Queue
    #tell the user your job recieved
    job = queue.enqueue(process_query, query)
    return {"status":"queued","job_id":job.id}

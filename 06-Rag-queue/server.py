from fastapi import FastAPI, Query
from .queue.connection import queue 

app = FastAPI()

@app.get("/")
def root():
    return {"status":"Server is up and running"}

@app.post("/chat")
def chat(query:str=Query(...,description="chat message")):
    #Insert the query to the Queue
    #tell the user your job recieved
    pass

# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from logic import find_similar_logic  
from pro_logic import find_similar_pro_logic  
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/vectorize/")
async def vectorize(request: TextRequest):
    text = request.text
    vector = model.encode(text)

    return {"vector": vector.tolist()}

@app.post("/find_similar/")
async def find_similar(request: TextRequest):
    text = request.text
    input_vector = model.encode(text)
    result = find_similar_logic(input_vector, text)

    return result

@app.post("/find_similar_pro/")
async def find_similar_pro(request: TextRequest):
    text = request.text
    input_vector = model.encode(text)
    result = find_similar_pro_logic(input_vector, text)  

    return result





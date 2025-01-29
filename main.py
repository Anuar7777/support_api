# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from logic import find_similar_logic  
from pro_logic import find_similar_pro_logic  
import numpy as np
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Middleware для ограничения доступа только с localhost
class LocalhostOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host
        if client_host != "127.0.0.1" and client_host != "localhost":
            raise HTTPException(status_code=403, detail="Access denied. Only localhost is allowed.")
        response = await call_next(request)
        return response

model = SentenceTransformer('all-MiniLM-L6-v2')
app = FastAPI()

class BaseTextRequest(BaseModel):
    text: str

class ComplexTextRequest(BaseModel):
    text: str
    created_by: str

@app.post("/vectorize/")
async def vectorize(request: BaseTextRequest):
    text = request.text
    vector = model.encode(text)

    return {"vector": vector.tolist()}

@app.post("/find_similar/")
async def find_similar(request: ComplexTextRequest):
    text = request.text
    created_by = request.created_by
    input_vector = model.encode(text)
    result = find_similar_logic(input_vector, text, created_by)

    return result

@app.post("/find_similar_pro/")
async def find_similar_pro(request: ComplexTextRequest):
    text = request.text
    created_by = request.created_by
    input_vector = model.encode(text)
    result = find_similar_pro_logic(input_vector, text, created_by)  

    return result





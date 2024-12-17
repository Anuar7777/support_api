from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/vectorize/")
async def vectorize(request: TextRequest):
    # Векторизация текста
    text = request.text
    vector = model.encode(text)
    
    # Преобразуем вектор в список для возврата
    return {"vector": vector.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import requests
from fastapi import HTTPException
from logic import find_similar_logic

API_URL = "https://cablyai.com/v1/chat/completions"

def find_similar_pro_logic(input_vector, text, created_by):
    result = find_similar_logic(input_vector, text, created_by)
    
    prompt = (
        f"Вы опытный оператор технической поддержки Platonus - Платон."
        f"Пользователь задал следующий запрос: '{text}'. "
        f"Система ответила: '{result['answer']}'. "
        "Перефразируй ответ системы чтобы звучало как человек,"
        "и не используй никакое Markdown-форматирование, только обычный текст."
    )
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            ai_suggestion = data["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Ошибка: {response.status_code}, {response.text}")

        return {
            "question": result['question'],
            "similarity": result['similarity'],
            "answer": ai_suggestion,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обращении к OpenAI API: {e}")



import requests
from fastapi import HTTPException
from logic import find_similar_logic

API_URL = "https://cablyai.com/v1/chat/completions"

def find_similar_pro_logic(input_vector, text, created_by, max_retries=3):
    result = find_similar_logic(input_vector, text, created_by)
    
    prompt = (
        f"Вы опытный оператор технической поддержки Platonus - Платон."
        f"Пользователь задал следующий запрос: '{text}'. "
        f"Система ответила: '{result.get('answer', 'Ответ не найден')}'. "
        "Перефразируй ответ системы чтобы звучало как человек,"
        "и не используй никакое Markdown-форматирование, только обычный текст."
    )
    
    headers = {
        "Content-Type": "application/json",
    }

    temperature = 0.5 

    for attempt in range(1, max_retries + 1):
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if "choices" in data and data["choices"]:
                    ai_suggestion = data["choices"][0]["message"].get("content", "").strip()
                    
                    if ai_suggestion:  
                        return {
                            "question": result.get("question", ""),
                            "similarity": result.get("similarity", 0),
                            "answer": ai_suggestion,
                        }
            
            temperature = min(temperature + 0.2, 1.0)  

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к API: {e}")

    raise HTTPException(status_code=500, detail="API вернул пустой ответ после нескольких попыток.")



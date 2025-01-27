from fastapi import HTTPException
import numpy as np
from db import get_db_connection
from psycopg2.extras import RealDictCursor
import re

def find_similar_logic(input_vector, text):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if len(text.split(" ")) < 4 or len(text) < 10:
            return {
                "question": "Некорректный запрос",
                "similarity": 100,
                "answer": "Пожалуйста, детализируйте вашу ситуацию", 
                "query": text,
            }

        if any(len(word) > 40 for word in text.split(" ")):
            return {
                "question": "Некорректный запрос",
                "similarity": 100,
                "answer": "Пожалуйста, опишите вашу ситуацию корректно. Не надо писать слишком длинные слова.", 
                "query": text,
            }

        if re.search(r'https?://[^\s]+', text):
            return {
                "question": "Некорректный запрос",
                "similarity": 100,
                "answer": "Пожалуйста, удалите ссылку и попробуйте снова.", 
                "query": text,
            }

        # Получение вопросов и их векторов
        cursor.execute("SELECT question_id, question, question_vector, answer_id FROM questions")
        questions = cursor.fetchall()

        if not questions:
            raise HTTPException(status_code=404, detail="Нет данных в таблице вопросов.")

        # Поиск всех похожих вопросов
        top_match = None
        max_similarity = 0

        for question in questions:
            db_vector = np.array(question['question_vector'], dtype=float)
            similarity = np.dot(input_vector, db_vector) / (np.linalg.norm(input_vector) * np.linalg.norm(db_vector))
            if similarity > max_similarity:
                max_similarity = similarity
                top_match = question

        if not top_match:
            raise HTTPException(status_code=404, detail="Нет похожих вопросов.")

        # Извлечение ответа из таблицы answers
        cursor.execute("SELECT answer FROM answers WHERE answer_id = %s", (top_match['answer_id'],))
        answer_row = cursor.fetchone()

        if not answer_row:
            raise HTTPException(status_code=404, detail="Ответ для данного вопроса не найден.")

        if max_similarity < 0.75:
            return {
                "question": top_match['question'],
                "similarity": max_similarity,
                "answer": "Ваш запрос перенаправлен на оператора",
                "query": text,
            }

        return {
            "question": top_match['question'],
            "similarity": max_similarity,
            "answer": answer_row['answer'],  
            "query": text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {e}")
    finally:
        if conn:
            conn.close()
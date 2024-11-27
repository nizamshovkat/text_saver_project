# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()  # Создаём объект FastAPI

# Подключаем статические файлы для фронтенда
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Text Saver API!"}

# База данных
DB_PATH = "database.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS texts (id INTEGER PRIMARY KEY, content TEXT NOT NULL)"
        )

init_db()

# Модель данных
class Text(BaseModel):
    content: str

@app.post("/texts/")
def create_text(text: Text):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO texts (content) VALUES (?)", (text.content,))
        conn.commit()
        return {"id": cursor.lastrowid, "content": text.content}

@app.get("/texts/", response_model=List[Text])
def get_texts():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM texts")
        rows = cursor.fetchall()
        return [{"content": row[0]} for row in rows]

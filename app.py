from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from models import User  # модель из models.py
import re

app = FastAPI()

# Задание 1.1
@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}



# Задание 1.2 (HTML)
@app.get("/html")
def get_html():
    return FileResponse("index.html")



# Задание 1.3
class Numbers(BaseModel):
    num1: int
    num2: int

@app.post("/calculate")
def calculate(data: Numbers):
    return {"result": data.num1 + data.num2}



# Задание 1.4
user_instance = User(name="Ваше Имя и Фамилия", id=1)

@app.get("/users")
def get_user():
    return user_instance



# Задание 1.5
class UserWithAge(BaseModel):
    name: str
    age: int

@app.post("/user")
def check_user(user: UserWithAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }



# Задание 2.1 и 2.2
feedbacks = []

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    def check_bad_words(cls, value):
        banned_words = ["кринж", "рофл", "вайб"]
        for word in banned_words:
            if re.search(word, value, re.IGNORECASE):
                raise ValueError("Использование недопустимых слов")
        return value

@app.post("/feedback")
def add_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}
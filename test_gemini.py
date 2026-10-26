import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Не найден API-ключ в .env")

client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 20000},
)

print("Отправляю запрос Gemini...", flush=True)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Ответь кратко: API работает."
    )
    print("Ответ Gemini:", response.text, flush=True)
except Exception as error:
    print(f"Ошибка запроса: {type(error).__name__}: {error}", flush=True)
finally:
    client.close()
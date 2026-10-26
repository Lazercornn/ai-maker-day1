import os, json
from dotenv import load_dotenv
from google import genai
from pathlib import Path
from google.genai import types

load_dotenv()

history_file = Path("chat_history.json")

history_file = Path("chat_history.json")

if history_file.exists():
    content = history_file.read_text(encoding="utf-8").strip()

    if content:
        history = json.loads(content)
    else:
        history = []
else:
    history = []

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Не найден GEMINI_API_KEY в файле .env")

client = genai.Client(api_key=api_key)
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    history=[
        types.Content(
            role=item["role"],
            parts=[types.Part(text=item["text"])]
        )
        for item in history
    ]
)

print("AI-ассистент запущен.")
print("Напиши 'выход', чтобы завершить программу.")

while True:
    user_message = input("\nТы: ").strip()

    if user_message.lower() == "выход":
        print("Ассистент завершает работу.")
        break

    if user_message.lower() == "/очистить":
        history = []
        history_file.write_text("[]", encoding="utf-8")

        chat = client.chats.create(
            model="gemini-3.5-flash-lite"
        )

        print("История диалога очищена.")
        continue

    if not user_message:
        continue

    if user_message.lower() == "/помощь":
        print("\nДоступные команды:")
        print("  /очистить — начать новый диалог")
        print("  /помощь — показать список команд")
        print("  выход — завершить программу")
        continue

    try:
        response = chat.send_message(user_message)
        print(f"\nGemini: {response.text}")

        history.append({"role": "user", "text": user_message})
        history.append({"role": "model", "text": response.text})

        history_file.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8"
)

    except Exception as error:
        print(f"\nОшибка при запросе к Gemini: {error}")

client.close()
import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Загружаем настройки из файла окружения.
load_dotenv()

# Получаем ключ API из окружения.
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Не найден GEMINI_API_KEY в файле .env")

# Создаём клиента Gemini и консоль для вывода.
console = Console()


# Показываем название приложения.
def show_welcome():

    console.print(
        Panel(
            "AI-помощник для анализа текста",
            title="Smart CLI Assistant",
            border_style="blue",
        )
    )


# Собираем строки до команды END.
def get_text():
    # Создаём пустой список для хранения строк
    lines = []

    # Продолжаем ввод, пока пользователь не напишет END
    while True:
        line = console.input()

        if line.strip() == "END":
            break

        lines.append(line)

    # Объединяем строки и возвращаем результат
    return "\n".join(lines).strip()


# Просим вставить текст для анализа.
def analyze_text(analysis_type, text):
    """Отправляет текст в Gemini и возвращает ответ."""
    try:
        console.print("[yellow]Отправляю текст в Gemini...[/]")

        # Загружаем настройки из файла окружения.
        load_dotenv()

        # Получаем ключ API из окружения.
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            console.print("[red]Не найден GEMINI_API_KEY в файле .env[/]")
            raise SystemExit(1)

        # Создаём клиента Gemini.
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=(
                f"Ты помощник по анализу текста. "
                f"Проанализируй {analysis_type}. "
                "Выдели основные выводы, сильные стороны, "
                "проблемы и конкретные рекомендации. "
                "Отвечай по-русски, структурированно и кратко.\n\n"
                f"Текст:\n{text}"
            ),
        )

        if not response.text:
            console.print("[red]Gemini вернул пустой ответ.[/]")
            raise SystemExit(1)

        return response.text

    except APIError as error:
        console.print(f"[red]Не удалось получить ответ от Gemini: {error}[/]")
        raise SystemExit(1)


# Выводим результат анализа.
def show_result(analysis_type, result):
    """Показывает результат анализа в таблице."""
    table = Table(title="Результат анализа")
    table.add_column("Тип анализа", style="cyan")
    table.add_column("Результат", style="green")

    table.add_row(
        analysis_type.capitalize(),
        result,
    )

    console.print(table)


def validate_text(text):
    if not text:
        raise ValueError("Текст не должен быть пустым.")

    if len(text) > 10000:
        raise ValueError("Текст слишком длинный. Максимальная длина 10000 символов.")


def main():
    show_welcome()

    analysis_type = Prompt.ask(
        "Что анализируем",
        choices=["резюме", "вакансию", "предложение"],
    )

    console.print(
        "[dim]Вставь текст. Для завершения ввода напиши END на отдельной строке.[/]"
    )

    text = get_text()

    try:
        validate_text(text)
    except ValueError as error:
        console.print(f"[red]{error}[/]")
        raise SystemExit(1)

    result = analyze_text(analysis_type, text)
    show_result(analysis_type, result)


if __name__ == "__main__":
    main()

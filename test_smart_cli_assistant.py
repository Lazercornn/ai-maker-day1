from unittest.mock import patch

import pytest
from google.genai.errors import APIError

import smart_cli_assistant
from smart_cli_assistant import validate_text


def test_validate_text_rejects_empty_text():
    with pytest.raises(ValueError):
        validate_text("")


def test_validate_text_accepts_normal_text():
    validate_text("Резюме Python-разработчика")


def test_validate_text_accepts_max_length():
    validate_text("F" * 10000)


def test_validate_rejects_over_max_text():
    with pytest.raises(ValueError):
        validate_text("f" * 10001)


def test_analyze_text_returns_gemini_response():
    with patch("smart_cli_assistant.genai.Client") as mock_client:
        mock_client.return_value.models.generate_content.return_value.text = (
            "Основные выводы и рекомендации"
        )

        result = smart_cli_assistant.analyze_text(
            "резюме",
            "Опыт работы Python-разработчиком",
        )

        assert result == "Основные выводы и рекомендации"

        mock_client.return_value.models.generate_content.assert_called_once()

        call_args = mock_client.return_value.models.generate_content.call_args

        assert call_args.kwargs["model"] == "gemini-3.5-flash-lite"
        assert "Опыт работы Python-разработчиком" in call_args.kwargs["contents"]


def test_analyze_text_exits_on_empty_response():
    with patch("smart_cli_assistant.genai.Client") as mock_client:
        mock_client.return_value.models.generate_content.return_value.text = ""

        with pytest.raises(SystemExit) as error:
            smart_cli_assistant.analyze_text(
                "резюме",
                "Тестовый текст",
            )

        assert error.value.code == 1


def test_analyze_text_exits_on_api_error():
    with patch("smart_cli_assistant.genai.Client") as mock_client:
        mock_client.return_value.models.generate_content.side_effect = APIError(
            "Test API error",
            {},
        )

        with pytest.raises(SystemExit) as error:
            smart_cli_assistant.analyze_text(
                "резюме",
                "Тестовый текст",
            )

        assert error.value.code == 1

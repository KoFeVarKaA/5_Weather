from functools import wraps

import requests
from django.http import HttpRequest
from django.shortcuts import render

def handle_api_errors(view_func):
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)

        except requests.exceptions.Timeout:
            return _render_error_response(
                request, "Запрос к api занял слишком много времени. Попробуйте позже."
            )

        except requests.exceptions.RequestException as e:
            return _render_error_response(request, f"Ошибка соединения: {str(e)}")

        except Exception as e:
            return _render_error_response(request, f"Произошла ошибка: {str(e)}")

    return wrapper


def _render_error_response(request, message):
    data = {
        "card_header": "Результаты поиска",
        "text_muted": "Не удалось получить данные",
        "messages": [message],
    }
    return render(request, "weather/base_template.html", data)

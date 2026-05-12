from functools import wraps
import requests
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.cache import cache

# def cache_search_result(timeout=3600):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request: HttpRequest, *args, **kwargs):
#             place = request.GET.get('place', '')
#             cache_key = f"search_results_{place.lower()}"
#             cached_data = cache.get(cache_key)
#             if cached_data is not None:
#                 return render(request, 'weather/base_template.html', cached_data)

#             context = view_func(request, place, *args, **kwargs)

#             cache.set(cache_key, context, timeout=timeout)
#             return render(request, 'weather/base_template.html', context)
#         return wrapper
#     return decorator


# Возможно убрать messages
def handle_api_errors(view_func):
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)

        except requests.exceptions.Timeout:
            _render_error_response(
                request, "Запрос к api занял слишком много времени. Попробуйте позже."
            )

        except requests.exceptions.RequestException as e:
            _render_error_response(request, f"Ошибка соединения: {str(e)}")

        except Exception as e:
            _render_error_response(request, f"Произошла ошибка: {str(e)}")

    return wrapper


def _render_error_response(request, message):
    data = {
        "card_header": "Результаты поиска",
        "text_muted": "Не удалось получить данные",
        "messages": [message],
    }
    return render(request, "weather/base_template.html", data)

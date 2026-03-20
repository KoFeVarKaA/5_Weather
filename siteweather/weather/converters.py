# Можно создавать свои собственные конвертеры, валидация данных
class FourDigitYearConverter:
    regex = "[0-9]{4}" #регулярное выражение

    # Преобразуем в нужный тип дынных, строку из URL в Python-объект
    # Когда Django обрабатывает запрос и передаёт в view
    def to_python(self, value):
        return int(value)

    # Python-объект обратно в строку, url
    # Используется при генерации URL
    def to_url(self, value):
        return "%04d" % value
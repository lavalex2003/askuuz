# Руководство по внесению вклада

Спасибо за интерес к разработке компонента askuuz! Это руководство поможет вам внести свой вклад в проект.

## Как начать

### 1. Подготовка окружения

```bash
# Клонируйте репозиторий
git clone https://github.com/lavalex2003/askuuz.git
cd askuuz

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements-dev.txt
```

### 2. Создание ветки

```bash
git checkout -b feature/my-feature  # Для новых функций
git checkout -b fix/my-bug          # Для исправления ошибок
```

## Процесс разработки

### Кодовые стандарты

- **Python**: Следуйте [PEP 8](https://pep8.org/)
- **Черные точки**: Максимум 100 символов в строке
- **Типизация**: Используйте type hints для всех функций
- **Документация**: Документируйте все публичные методы и классы

### Проверка кода

```bash
# Форматирование
black . --line-length=100

# Линтинг
flake8 . --max-line-length=100

# Проверка типов
mypy custom_components/askuuz

# Тесты
pytest tests/
```

### Commit сообщения

Используйте семантические commit сообщения:

```
feat: добавить новую функцию
fix: исправить баг в сенсоре
docs: обновить README
refactor: переработать код API клиента
test: добавить тесты
chore: обновить зависимости
```

Примеры:

```
feat: добавить кнопку для обновления управления
fix: исправить ошибку при неверном пароле
docs: добавить примеры использования автоматизаций
```

## Отправка Pull Request

1. **Форк репозитория** и создание ветки
2. **Внесите изменения** и убедитесь в их качестве
3. **Запустите тесты** и проверку кода
4. **Отправьте PR** с описанием изменений:
   - Четкое описание что было изменено
   - Связанные issues (закрытие через "Fixes #123")
   - Скриншоты или видео (если применимо)
   - Чек-лист:
     - [ ] Код следует стилю проекта
     - [ ] Добавлены комментарии для сложных участков
     - [ ] Обновлена документация
     - [ ] Добавлены/обновлены тесты
     - [ ] Все тесты проходят

## Типы вклада

### Сообщение об ошибке

Используйте шаблон [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)

### Предложение функции

Используйте шаблон [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)

### Улучшение документации

Исправления в README.md, FAQ.md или код-комментариях приветствуются!

### Перевод

Добавляйте переводы новых строк в:
- `translations/ru.json` (русский)
- `translations/en.json` (английский)
- `translations/uz.json` (узбекский)

## Структура проекта

```
askuuz/
├── __init__.py                 # Инициализация компонента
├── config_flow.py              # Конфигурация через UI
├── const.py                    # Константы
├── button.py                   # Кнопки обновления
├── manifest.json               # Метаданные
├── electricity/                # Сервис электричество
│   ├── __init__.py
│   ├── sensor.py
│   ├── button.py
│   └── api.py
├── water/                      # Сервис вода
├── tbo/                        # Сервис ТБО
├── management/                 # Сервис управление
└── translations/               # Переводы
    ├── ru.json
    ├── en.json
    └── uz.json
```

## Добавление новой функции

### Пример: Добавление нового сервиса

1. Создайте новую папку `newservice/`
2. Добавьте `__init__.py`, `sensor.py`, `button.py`
3. Реализуйте `NewServiceApiClient` в `api.py`
4. Добавьте координатор в главный `__init__.py`
5. Добавьте переводы в `translations/*.json`
6. Обновите README.md
7. Добавьте тесты в `tests/`

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием кода
pytest --cov=custom_components/askuuz

# Конкретный тест
pytest tests/test_config_flow.py::test_user_step
```

### Написание тестов

```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_my_feature():
    """Описание теста."""
    # Arrange
    mock_data = {"consumption": 100}
    
    # Act
    result = await fetch_data()
    
    # Assert
    assert result == mock_data
```

## Запросы на функции

Перед тем как потратить время на реализацию, откройте [Issue](https://github.com/lavalex2003/askuuz/issues) с описанием:

- **Проблема**: Что не работает или не нравится
- **Решение**: Ваше предложение реализации
- **Примеры**: Код или скриншоты

## Договор о поведении

Мы придерживаемся [Кодекса поведения](CODE_OF_CONDUCT.md) в этом проекте.

## Вопросы?

- Откройте [Discussion](https://github.com/lavalex2003/askuuz/discussions)
- Напишите в [Issues](https://github.com/lavalex2003/askuuz/issues)
- Контакт: через GitHub

---

Спасибо за ваш вклад! ❤️

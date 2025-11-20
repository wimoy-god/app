# Управление мастер-классами — Минимальное приложение

Это простое приложение на Flask для управления мастер-классами: создание, редактирование, удаление и просмотр.

Технологии
- Python 3.8+
- Flask
- Flask-SQLAlchemy (SQLite)

Коротко: этот репозиторий содержит `app.py` (маршруты и модели), шаблоны в `templates/`, стили в `static/` и файл базы `db.sqlite3`, который создаётся автоматически.

Полные инструкции по запуску (Windows PowerShell)

1) Перейдите в каталог проекта:

```powershell
cd C:\Users\wimoy\Desktop\kyr
```

2) (Опционально) просмотрите текущую структуру и проверьте, нет ли вложенного `.venv`:

```powershell
Get-ChildItem -Force
Test-Path .\.venv
Get-ChildItem .\.venv -Force
```

3) Рекомендованный безопасный способ — удалить старый venv (если он повреждён или вложен) и создать новый:

```powershell
# Удаляет папку .venv (внимание: удаляет всё внутри неё)
Remove-Item -Recurse -Force .\.venv

# Создать новое виртуальное окружение
python -m venv .venv
```

4) Временное разрешение выполнения скриптов (не сохраняет изменение политики) и активация venv:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

После успешной активации приглашение PowerShell обычно будет содержать префикс `(.venv)`.

5) Установка зависимостей и запуск приложения:

```powershell
python -m pip install --upgrade pip
pip install -r .\requirements.txt
python app.py
```

Откройте в браузере: http://127.0.0.1:5000/

Альтернатива — запуск без активации venv (все команды явно используют Python из `.venv`):

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe app.py
```

Диагностика проблем

- Ошибка `ModuleNotFoundError: No module named 'flask'` — значит, вы используете Python, в котором Flask не установлен. Убедитесь, что:
	- активировали правильное виртуальное окружение, или
	- используете `.\.venv\Scripts\python.exe` для установки и запуска.

- Проверка, какой Python используется и установлен ли Flask:

```powershell
python -c "import sys; print(sys.executable)"
python -c "import importlib.util; print('flask installed:', importlib.util.find_spec('flask') is not None)"
# или с явным venv-путём
.\.venv\Scripts\python.exe -c "import flask; print('Flask', flask.__version__)"
```

- Если PowerShell продолжает блокировать активацию (ExecutionPolicy), используйте команду `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` перед активацией — это временно и безопасно для текущей сессии.

VS Code: убрать предупреждения Pylance "Import could not be resolved"

- После создания и установки зависимостей в `.venv`, в VS Code выберите интерпретатор виртуального окружения:
	- Откройте Command Palette (Ctrl+Shift+P) → `Python: Select Interpreter` → выберите `C:\Users\wimoy\Desktop\kyr\.venv\Scripts\python.exe`.
	- Перезагрузите окно (Ctrl+Shift+P → `Developer: Reload Window`).

Seed (sample) данные

При первом запуске `app.py` приложение автоматически создаёт таблицы и, если база пустая, заполнит её примерами мастер-классов (это удобно для демонстрации).

Структура файлов

- `app.py` — основной код, маршруты и модель `Masterclass`.
- `models.py` — дублирует модель (можно убрать/перенести по желанию).
- `templates/` — шаблоны: `index.html`, `form.html`, `detail.html`.
- `static/style.css` — стили.
- `requirements.txt` — список зависимостей.


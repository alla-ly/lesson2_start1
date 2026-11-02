# lesson2_start — общий проверенный старт Lesson 2 «AI in Automation · OpenCode»

Все студенты начинают Lesson 2 **из этой копии**, а не из своего проекта после Lesson 1.
Ваш проект Lesson 1 остаётся у вас. Сегодня нужен одинаковый repository, чтобы agent
(OpenCode) у всех видел одну и ту же кодовую базу.

## Что внутри

| Файл | Зачем на Lesson 2 |
|---|---|
| `config.py` | URL, логин/пароль, headless, timeout — из `.env` |
| `conftest.py` | fixture `driver` (Chrome) + скриншот при падении в `screenshots/` (evidence для debugging) |
| `pages/login_page.py` | `LoginPage` |
| `pages/products_page.py` | `ProductsPage`: add/remove, badge, sort (база для задачи Cart и FLEX sorting) |
| `tests/test_login.py` | login: positive + 3 negative (parametrize) |
| `tests/test_cart.py` | add / remove — сюда добавляется проверка корзины |
| `tests/test_ai_cases.py` | problem_user (known bug, xfail) и sorting z→a |
| `opencode.json` | **обязателен**: OpenCode стартует в агенте plan (правки запрещены); в build каждая правка и команда — с подтверждением. Без файла build меняет файлы без вопроса |
| `check_lesson2_ready.ps1` | проверка готовности (ничего не меняет) |
| `get_edgedriver.ps1` | только если Windows блокирует `selenium-manager.exe` (Smart App Control): скачивает подписанный `msedgedriver` и включает в `.env` `BROWSER=edge` |
| `get_edgedriver.ps1` | только если Windows блокирует `selenium-manager.exe` (Smart App Control): скачивает подписанный `msedgedriver` и включает в `.env` `BROWSER=edge` |

`CartPage` на старте **нет** — он появится на уроке.

## Baseline

```
python -m pytest -q
7 passed, 1 xfailed
```

Всего 8 tests. `xfailed` — это `test_problem_user_remove_from_cart_known_bug` (известный баг учебного сайта).

## Подготовка (PyCharm Terminal, PowerShell, корень проекта)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python -m pytest -q
git init -b main
git add .
git commit -m "lesson2_start baseline"
.\check_lesson2_ready.ps1
npm install -g opencode-ai     # если OpenCode ещё не установлен
opencode                       # в корне проекта
```

`.env` в Git не попадает (см. `.gitignore`). Не отправляйте `.env` в AI.

## Если Windows пишет «An Application Control policy has blocked this file»

Это защита Windows 11 (Smart App Control): она блокирует неподписанные программы, например
`pytest.exe` или `selenium-manager.exe` (через него Selenium ищет драйвер Chrome).

1. Всегда запускайте tests так: `python -m pytest -q` (не просто `pytest`).
2. Если tests всё равно падают с этой ошибкой (`selenium-manager.exe`) — переключаем tests на Microsoft Edge
   с официальным драйвером Microsoft. В корне `lesson2_start`:

```powershell
powershell -ExecutionPolicy Bypass -File .\get_edgedriver.ps1
python -m pytest -q
```

Скрипт скачает `msedgedriver` под вашу версию Edge в папку `drivers\` и сам запишет в `.env`
`BROWSER=edge` и `DRIVER_PATH`. Ожидаемо: `7 passed, 1 xfailed`.
Защиту Windows **не отключайте**. OpenCode этой защитой не блокируется (он подписан).

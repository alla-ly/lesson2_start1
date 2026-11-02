# Проверка готовности к Lesson 2. Запускать из корня lesson2_start (PyCharm Terminal, venv активирован).
# Скрипт ничего не меняет — только читает и печатает OK / FAIL / INFO.
$script:fails = 0
function Check($name, $ok, $hint) {
    if ($ok) { Write-Host "[OK]   $name" -ForegroundColor Green }
    else     { Write-Host "[FAIL] $name  -> $hint" -ForegroundColor Red; $script:fails++ }
}
function Info($text) { Write-Host "[INFO] $text" -ForegroundColor Cyan }

$py = Get-Command python -ErrorAction SilentlyContinue
Check "python найден" ($null -ne $py) "установите Python / активируйте .venv"

$git = Get-Command git -ErrorAction SilentlyContinue
Check "git найден" ($null -ne $git) "установите Git for Windows"

Check "мы в корне lesson2_start (есть conftest.py и pages\products_page.py)" ((Test-Path conftest.py) -and (Test-Path pages\products_page.py)) "cd в папку lesson2_start"
Check "есть .env" (Test-Path .env) "copy .env.example .env"
if (Test-Path pages\cart_page.py) { Info "CartPage есть: это checkpoint после Part 6 (lesson2_after_cart / lesson2_broken / lesson2_final)" } else { Info "CartPage нет: это стартовая копия lesson2_start" }

if ($git) {
    $inside = (git rev-parse --is-inside-work-tree 2>$null)
    Check "проект — Git repository" ($inside -eq "true") "git init -b main"
    if ($inside -eq "true") {
        $root = (git rev-parse --show-toplevel) -replace '/', '\'
        $here = (Get-Location).Path
        Check "git root = текущая папка" ($root -ieq $here) "repository лежит выше: $root"
        Check "есть хотя бы один commit" ($null -ne (git rev-parse --verify HEAD 2>$null)) "git add . ; git commit -m 'lesson2_start baseline'"
        Check "working tree чистый" ([string]::IsNullOrWhiteSpace((git status --porcelain))) "закоммитьте или откатите изменения (git status)"
        git check-ignore -q .env
        Check ".env в .gitignore" ($LASTEXITCODE -eq 0) "добавьте .env в .gitignore"
        $tracked = git ls-files .env
        Check ".env не в Git" ([string]::IsNullOrWhiteSpace($tracked)) "git rm --cached .env"
    }
}

if ($py) {
    $out = python -m pytest --collect-only -q 2>&1 | Select-String "tests collected"
    $expected = if (Test-Path pages\cart_page.py) { 9 } else { 8 }
    Check "pytest собирает $expected tests" ($out -match "^$expected tests collected") "ожидали $expected tests; получили: $out"
}

$opencode = Get-Command opencode -ErrorAction SilentlyContinue
Check "OpenCode установлен" ($null -ne $opencode) "npm install -g opencode-ai, затем НОВЫЙ terminal"
if ($opencode) { Info "OpenCode: $(opencode --version)" }
Check "opencode.json на месте" (Test-Path opencode.json) "не удаляйте opencode.json: без него build меняет файлы без вопроса"

Write-Host ""
if ($script:fails -eq 0) { Write-Host "ОБЯЗАТЕЛЬНАЯ ЧАСТЬ ГОТОВА. Дальше: pytest -q  ->  lesson2_start: 7 passed, 1 xfailed; после Part 6: 8 passed, 1 xfailed" -ForegroundColor Green }
else { Write-Host "Исправьте $($script:fails) пункт(ов) и запустите снова." -ForegroundColor Yellow }

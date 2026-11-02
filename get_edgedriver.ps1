# Нужен ТОЛЬКО если Windows блокирует selenium-manager.exe или pytest:
#   "An Application Control policy has blocked this file" (Smart App Control).
# Скачивает официальный msedgedriver (подписан Microsoft) под установленную версию Edge в папку drivers\
# и дописывает в .env: BROWSER=edge и DRIVER_PATH. Запуск из корня проекта:
#   powershell -ExecutionPolicy Bypass -File .\get_edgedriver.ps1
$ErrorActionPreference = "Stop"
$edge = @("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "C:\Program Files\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { Write-Host "Microsoft Edge не найден. Напишите преподавателю." -ForegroundColor Red; exit 1 }
$ver = (Get-Item $edge).VersionInfo.ProductVersion
Write-Host "Edge $ver"
$url = "https://msedgedriver.microsoft.com/$ver/edgedriver_win64.zip"
New-Item -ItemType Directory -Force drivers | Out-Null
Invoke-WebRequest $url -OutFile "drivers\edgedriver_win64.zip" -UseBasicParsing
Expand-Archive "drivers\edgedriver_win64.zip" "drivers" -Force
Remove-Item "drivers\edgedriver_win64.zip"
$driver = (Resolve-Path "drivers\msedgedriver.exe").Path
$sig = Get-AuthenticodeSignature $driver
Write-Host "msedgedriver: $(& $driver --version)  | подпись: $($sig.Status)"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
$lines = Get-Content .env -Encoding UTF8 | Where-Object { $_ -notmatch '^(BROWSER|DRIVER_PATH)=' }
$lines += "BROWSER=edge"
$lines += "DRIVER_PATH=$driver"
[System.IO.File]::WriteAllLines((Join-Path (Get-Location) ".env"), [string[]]$lines, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Готово: в .env записаны BROWSER=edge и DRIVER_PATH. Проверка: python -m pytest -q" -ForegroundColor Green

# Как загрузить эти файлы на GitHub (подробно)

Этот документ объясняет **три способа** залить репозиторий и **какие файлы
за что отвечают**. Для обычной практики достаточно Способа 1 или 2.

---

## ⚠️ Важно: скрытые папки (начинаются с точки)

В проекте есть папки, имя которых начинается с точки:

- `.github/` — воркфлоу GitHub Actions и настройки Classroom (**обязательно!**)
- `.devcontainer/` — автозапуск среды в Codespaces (**обязательно для Codespaces**)
- `.zap/` — настройки сканера ZAP

> Через веб‑интерфейс «Upload files» перетаскиванием такие папки
> **иногда не загружаются**. Поэтому ниже для веб‑способа отдельно показано,
> как создать эти файлы вручную. Надёжнее всего — Способ 2 (git) или
> Способ 3 (GitHub Desktop): они грузят всё, включая скрытые папки.

---

## Полная структура репозитория и назначение файлов

```
owasp-access-control-lab/
├── README.md                     ← главная инструкция/задание (видна на странице репо)
├── docker-compose.yml            ← локальный запуск мишени
├── LICENSE
├── .gitignore
│
├── .devcontainer/
│   └── devcontainer.json         ← Codespaces: сам запускает Juice Shop на порту 3000
│
├── .github/
│   ├── workflows/
│   │   ├── zap-scan.yml          ← автосканирование безопасности (OWASP ZAP)
│   │   └── classroom.yml         ← автопроверка GitHub Classroom
│   └── classroom/
│       └── autograding.json      ← какие тесты и сколько баллов (для Classroom)
│
├── .zap/
│   └── rules.tsv                 ← настройка правил ZAP (ВАЖНО: там табуляции!)
│
├── requests/                     ← готовые HTTP‑запросы (расширение REST Client)
│   ├── 01_idor_basket.http
│   ├── 02_forced_browsing.http
│   ├── 03_privilege_escalation.http
│   └── 04_jwt_analysis.http
│
├── answers/
│   └── answers.yml               ← СТУДЕНТ заполняет ответы (их читает автопроверка)
│
├── tests/
│   └── check.py                  ← скрипт автопроверки (эталоны хранятся хэшами)
│
├── reports/
│   └── REPORT_TEMPLATE.md        ← шаблон отчёта
│
├── screenshots/
│   └── README.md                 ← сюда класть скриншоты (мин. 5 для автопроверки)
│
└── docs/
    ├── SETUP.md                  ← запуск и устранение неполадок
    ├── HINTS.md                  ← подсказки (без готовых решений)
    ├── ЗАГРУЗКА_НА_GITHUB.md      ← этот файл
    └── ПРЕПОДАВАТЕЛЮ.md           ← настройка Classroom и автопроверки
```

**Минимально обязательны для работы лаборатории:** `README.md`,
`.devcontainer/devcontainer.json`, `requests/*`, `docker-compose.yml`.
**Для автосканера:** `.github/workflows/zap-scan.yml`, `.zap/rules.tsv`.
**Для автопроверки Classroom:** `.github/workflows/classroom.yml`,
`.github/classroom/autograding.json`, `tests/check.py`, `answers/answers.yml`.

---

## Способ 1. Через сайт GitHub (без установки программ)

1. Зайдите на https://github.com и нажмите **+ → New repository**.
2. Имя: например `owasp-access-control-lab`. Поставьте галочку
   **Add a README** → **Create repository**.
3. На странице репозитория нажмите **Add file → Upload files**.
4. Распакуйте архив на компьютере и перетащите в окно **обычные** папки и
   файлы: `requests/`, `answers/`, `tests/`, `reports/`, `docs/`,
   `screenshots/`, `README.md`, `docker-compose.yml`, `LICENSE`, `.gitignore`.
5. Нажмите **Commit changes**.

### Догрузка скрытых папок вручную (если они не загрузились)

Для каждого файла из `.github/`, `.devcontainer/`, `.zap/`:

1. **Add file → Create new file**.
2. В поле имени введите **полный путь**, например:
   `.github/workflows/classroom.yml`
   (как только вы напечатаете `/`, GitHub сам создаст папку).
3. Откройте этот файл из архива текстовым редактором, скопируйте всё
   содержимое и вставьте.
4. **Commit changes**. Повторите для остальных:
   - `.github/workflows/zap-scan.yml`
   - `.github/classroom/autograding.json`
   - `.devcontainer/devcontainer.json`
   - `.zap/rules.tsv` ← **внимание:** вставьте ровно как в файле,
     не заменяйте табуляции пробелами, иначе ZAP не прочитает правила.

---

## Способ 2. Через командную строку (git) — грузит всё сразу

```bash
# 1. Распакуйте архив и зайдите в папку
cd owasp-access-control-lab

# 2. Инициализируйте git
git init
git add .
git commit -m "Практическая работа: Broken Access Control lab"

# 3. Создайте пустой репозиторий на github.com (без README),
#    скопируйте его адрес и подключите:
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/owasp-access-control-lab.git
git push -u origin main
```

Этот способ загружает и скрытые папки (`.github`, `.devcontainer`, `.zap`)
без лишних действий.

---

## Способ 3. Через GitHub Desktop (графическая программа)

1. Установите **GitHub Desktop** (https://desktop.github.com).
2. **File → New repository** или перетащите папку с файлами в окно.
3. Нажмите **Publish repository**. Все файлы, включая скрытые, уедут на GitHub.

---

## Проверка, что всё загрузилось

На странице репозитория включите показ скрытых файлов (они видны в списке
как `.github`, `.devcontainer`, `.zap`). Убедитесь, что присутствуют:

- [ ] `.devcontainer/devcontainer.json`
- [ ] `.github/workflows/zap-scan.yml`
- [ ] `.github/workflows/classroom.yml`
- [ ] `.github/classroom/autograding.json`
- [ ] `.zap/rules.tsv`
- [ ] `answers/answers.yml`, `tests/check.py`
- [ ] папки `requests/`, `reports/`, `screenshots/`, `docs/`

После этого можно запускать Codespace (кнопка **Code → Codespaces**).

# Инструкция по запуску и устранение неполадок

## A. Запуск в GitHub Codespaces (основной способ)

1. Залейте этот репозиторий себе (Use this template → Create a new repository,
   или просто загрузите файлы в новый репозиторий).
2. Кнопка **Code** (зелёная) → вкладка **Codespaces** → **Create codespace on main**.
3. Откроется VS Code в браузере. Дождитесь, пока внизу выполнится
   `postStartCommand` (скачивание образа Juice Shop — 1–2 минуты).
4. Вкладка **PORTS** внизу → строка **3000** → значок 🌐 (Open in Browser).
5. Откроется Juice Shop. Готово.

### Если порт 3000 не появился
Откройте терминал в Codespace и выполните:
```bash
docker ps                 # контейнер juice-shop должен быть в списке
docker logs juice-shop    # посмотреть, запустился ли
```
Если контейнера нет — запустите вручную:
```bash
docker run -d --rm -p 3000:3000 --name juice-shop bkimminich/juice-shop
```
Затем во вкладке PORTS нажмите **Add Port** → введите `3000`.

### Как узнать адрес приложения в Codespace
В Codespace адрес отличается от localhost. В файлах `requests/*.http`
переменная `@host` задана как `http://localhost:3000` — внутри Codespace
REST Client всё равно достучится до проброшенного порта. Для открытия в
браузере используйте ссылку из вкладки PORTS.

## B. Локальный запуск (Docker)

```bash
docker run --rm -p 3000:3000 bkimminich/juice-shop
# или
docker compose up
```
Откройте http://localhost:3000

## C. Работа с .http файлами (REST Client)

1. Откройте любой файл из папки `requests/`.
2. Над запросом появится ссылка **Send Request** — нажмите.
3. Справа откроется ответ сервера.
4. Чтобы провести атаку — измените значение (id, поле role и т.п.) и
   отправьте запрос снова.

Если ссылки **Send Request** нет — установите расширение
**REST Client** (humao.rest-client). В Codespace оно ставится автоматически.

## D. Запуск автосканера ZAP

Вкладка **Actions** репозитория → workflow
«Автоматическое сканирование безопасности (OWASP ZAP)» → **Run workflow**.
После завершения внизу страницы запуска будет артефакт
**zap-baseline-report** — скачайте и откройте HTML-отчёт.

#!/usr/bin/env python3
"""
Автопроверка практической работы (GitHub Classroom).

Использование:
    python tests/check.py <проверка>

Доступные проверки:
    idor | forced | privesc | jwt | category | report | screenshots

Скрипт печатает "PASS: ..." и завершается с кодом 0 при успехе,
иначе печатает "FAIL: ..." и завершается с кодом 1.
"""
import sys
import os
import re
import glob
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSWERS = os.path.join(ROOT, "answers", "answers.yml")
REPORT = os.path.join(ROOT, "reports", "REPORT_TEMPLATE.md")
SHOTS = os.path.join(ROOT, "screenshots")

# sha256 от нормализованных эталонных ответов (чтобы не хранить их открытым текстом)
EXPECT = {
    "idor_admin_email": "6f9073139703211126b225355954f4890c8cd2aef90864856b5e89f222d60f55",
    "privesc_field": "4b168d88dc872a7753c2bc35b36a2d4249487af55baf78f247f38cae2fe962da",
    "privesc_value": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
    "jwt_role_field": "4b168d88dc872a7753c2bc35b36a2d4249487af55baf78f247f38cae2fe962da",
}


def norm(s):
    return re.sub(r"\s+", "", (s or "").strip().lower())


def h(s):
    return hashlib.sha256(norm(s).encode()).hexdigest()


def load_answers():
    try:
        import yaml
        with open(ANSWERS, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return {k: (v if v is not None else "") for k, v in data.items()}
    except FileNotFoundError:
        fail(f"не найден файл {ANSWERS}")
    except Exception as e:
        fail(f"не удалось прочитать answers.yml: {e}")


def ok(msg):
    print("PASS: " + msg)
    sys.exit(0)


def fail(msg):
    print("FAIL: " + msg)
    sys.exit(1)


def check_hash(ans, key, human):
    val = ans.get(key, "")
    if not val:
        fail(f"поле «{key}» не заполнено ({human})")
    if h(val) == EXPECT[key]:
        ok(f"{human}: ответ верный")
    fail(f"{human}: ответ неверный (проверьте «{key}»)")


def check_contains(ans, key, needle, human):
    val = norm(ans.get(key, ""))
    if not val:
        fail(f"поле «{key}» не заполнено ({human})")
    if needle in val:
        ok(f"{human}: ответ верный")
    fail(f"{human}: ответ не содержит ожидаемого ({human})")


def main():
    if len(sys.argv) < 2:
        fail("не указана проверка")
    what = sys.argv[1].lower()

    if what == "idor":
        ans = load_answers()
        # email администратора + корректный эндпоинт
        if not ans.get("idor_endpoint") or "basket" not in norm(ans.get("idor_endpoint", "")):
            fail("IDOR: эндпоинт должен содержать «basket»")
        check_hash(ans, "idor_admin_email", "Сценарий 1 (IDOR)")

    elif what == "forced":
        ans = load_answers()
        check_contains(ans, "admin_route", "administration", "Сценарий 2 (Forced Browsing)")

    elif what == "privesc":
        ans = load_answers()
        if h(ans.get("privesc_field", "")) != EXPECT["privesc_field"]:
            fail("Сценарий 3: неверное поле (privesc_field)")
        check_hash(ans, "privesc_value", "Сценарий 3 (Privilege Escalation)")

    elif what == "jwt":
        ans = load_answers()
        check_hash(ans, "jwt_role_field", "Сценарий 4 (JWT)")

    elif what == "category":
        ans = load_answers()
        val = norm(ans.get("owasp_category", ""))
        if re.search(r"a0?1[:\-]?2025", val) or val in ("a01", "a012025"):
            ok("Классификация OWASP: верно (A01:2025)")
        fail("Классификация OWASP: ожидается A01:2025")

    elif what == "report":
        if not os.path.exists(REPORT):
            fail("не найден reports/REPORT_TEMPLATE.md")
        text = open(REPORT, encoding="utf-8").read()
        required = ["Среда выполнения", "IDOR", "Forced Browsing",
                    "Privilege Escalation", "JWT", "ZAP", "Общий вывод"]
        missing = [s for s in required if s not in text]
        if missing:
            fail("в отчёте нет разделов: " + ", ".join(missing))
        # остались незаполненные плейсхолдеры ФИО/группа?
        placeholders = text.count("___")
        if placeholders > 6:
            fail(f"в отчёте слишком много незаполненных мест (___): {placeholders}")
        if len(text) < 1500:
            fail("отчёт выглядит слишком коротким — дополните выводы")
        ok("Отчёт заполнен и содержит все разделы")

    elif what == "screenshots":
        if not os.path.isdir(SHOTS):
            fail("нет папки screenshots/")
        imgs = []
        for ext in ("png", "jpg", "jpeg", "gif", "webp"):
            imgs += glob.glob(os.path.join(SHOTS, f"*.{ext}"))
            imgs += glob.glob(os.path.join(SHOTS, f"*.{ext.upper()}"))
        if len(imgs) >= 5:
            ok(f"Скриншоты приложены ({len(imgs)} шт.)")
        fail(f"нужно минимум 5 скриншотов, найдено: {len(imgs)}")

    else:
        fail(f"неизвестная проверка: {what}")


if __name__ == "__main__":
    main()

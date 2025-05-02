import csv
import os
import uuid
from datetime import datetime

FILE_NAME = "notes.csv"
DELIMITER = ";"


def init_file():
    """Создаёт файл, если не существует"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            pass


def load_notes():
    """Загружает все заметки из файла"""
    init_file()
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=DELIMITER)
        return [row for row in reader if len(row) == 4]


def save_notes(notes):
    """Сохраняет все заметки в файл"""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerows(notes)


def generate_id():
    """Генерирует уникальный ID"""
    return str(uuid.uuid4())[:8]


def create_note():
    title = input("Введите заголовок заметки: ")
    body = input("Введите текст заметки: ")
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    note_id = generate_id()

    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(f"{note_id}{DELIMITER}{title}{DELIMITER}{body}{DELIMITER}{timestamp}\n")

    print("Заметка успешно сохранена.")


def list_notes():
    notes = load_notes()
    date_filter = input("Введите дату (ДД.ММ.ГГГГ) для фильтрации или Enter для всех: ").strip()

    found = False
    for note in notes:
        if not date_filter or note[3].startswith(date_filter):
            print(f"\nID: {note[0]}\nЗаголовок: {note[1]}\nТело: {note[2]}\nДата: {note[3]}")
            found = True

    if not found:
        print("Заметки не найдены.")


def edit_note():
    note_id = input("Введите ID заметки для редактирования: ")
    notes = load_notes()
    updated = False

    for note in notes:
        if note[0] == note_id:
            print(f"Текущий заголовок: {note[1]}")
            new_title = input("Введите новый заголовок (или Enter для пропуска): ")
            print(f"Текущее тело: {note[2]}")
            new_body = input("Введите новое тело (или Enter для пропуска): ")

            note[1] = new_title if new_title else note[1]
            note[2] = new_body if new_body else note[2]
            note[3] = datetime.now().strftime("%d.%m.%Y %H:%M")
            updated = True
            break

    if updated:
        save_notes(notes)
        print("Заметка успешно обновлена.")
    else:
        print("Заметка с таким ID не найдена.")


def delete_note():
    note_id = input("Введите ID заметки для удаления: ")
    notes = load_notes()
    new_notes = [note for note in notes if note[0] != note_id]

    if len(new_notes) < len(notes):
        save_notes(new_notes)
        print("Заметка удалена.")
    else:
        print("Заметка с таким ID не найдена.")


def main():
    print("Добро пожаловать в приложение 'Заметки'.")

    while True:
        command = input("\nВведите команду (add, list, edit, delete, exit): ").strip().lower()

        if command == "add":
            create_note()
        elif command == "list":
            list_notes()
        elif command == "edit":
            edit_note()
        elif command == "delete":
            delete_note()
        elif command == "exit":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")


if __name__ == "__main__":
    main()
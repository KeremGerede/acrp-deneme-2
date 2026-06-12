"""
merge_test_clean_todo_app.py

Temiz ve düzgün çalışan basit Todo CLI uygulaması.
Merge/code-review testinde zafiyetsiz normal dosya olarak kullanılabilir.

Çalıştırma:
    python merge_test_clean_todo_app.py
"""

from __future__ import annotations


def show_menu() -> None:
    print("\n=== Temiz Todo Uygulaması ===")
    print("1. Görev ekle")
    print("2. Görevleri listele")
    print("3. Görevi tamamlandı işaretle")
    print("4. Görev sil")
    print("5. Çıkış")


def read_int(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"Lütfen {minimum} ile {maximum} arasında bir değer girin.")


def add_task(tasks: list[dict[str, object]]) -> None:
    title = input("Görev başlığı: ").strip()

    if not title:
        print("Görev başlığı boş olamaz.")
        return

    tasks.append({
        "title": title,
        "completed": False,
    })

    print("Görev eklendi.")


def list_tasks(tasks: list[dict[str, object]]) -> None:
    if not tasks:
        print("Henüz görev yok.")
        return

    print("\nGörevler:")

    for index, task in enumerate(tasks, start=1):
        status = "Tamamlandı" if task["completed"] else "Bekliyor"
        print(f"{index}. [{status}] {task['title']}")


def complete_task(tasks: list[dict[str, object]]) -> None:
    if not tasks:
        print("Tamamlanacak görev yok.")
        return

    list_tasks(tasks)
    task_number = read_int("Tamamlanacak görev numarası: ", 1, len(tasks))
    tasks[task_number - 1]["completed"] = True

    print("Görev tamamlandı olarak işaretlendi.")


def delete_task(tasks: list[dict[str, object]]) -> None:
    if not tasks:
        print("Silinecek görev yok.")
        return

    list_tasks(tasks)
    task_number = read_int("Silinecek görev numarası: ", 1, len(tasks))
    removed_task = tasks.pop(task_number - 1)

    print(f"Görev silindi: {removed_task['title']}")


def main() -> None:
    tasks: list[dict[str, object]] = []

    while True:
        show_menu()
        choice = read_int("Seçiminiz: ", 1, 5)

        if choice == 1:
            add_task(tasks)
        elif choice == 2:
            list_tasks(tasks)
        elif choice == 3:
            complete_task(tasks)
        elif choice == 4:
            delete_task(tasks)
        elif choice == 5:
            print("Program sonlandırıldı.")
            break


if __name__ == "__main__":
    main()

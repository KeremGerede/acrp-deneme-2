"""
merge_test_clean_expense_tracker.py

Temiz ve düzgün çalışan basit gider takip CLI uygulaması.
Merge/code-review testinde zafiyetsiz normal dosya olarak kullanılabilir.

Çalıştırma:
    python merge_test_clean_expense_tracker.py
"""

from __future__ import annotations


def show_menu() -> None:
    print("\n=== Temiz Gider Takip Uygulaması ===")
    print("1. Gider ekle")
    print("2. Giderleri listele")
    print("3. Toplam gideri göster")
    print("4. Kategoriye göre filtrele")
    print("5. Çıkış")


def read_positive_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()

        try:
            number = float(value)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        if number > 0:
            return number

        print("Tutar 0'dan büyük olmalıdır.")


def read_choice() -> int:
    while True:
        value = input("Seçiminiz: ").strip()

        try:
            choice = int(value)
        except ValueError:
            print("Lütfen 1 ile 5 arasında bir sayı girin.")
            continue

        if 1 <= choice <= 5:
            return choice

        print("Geçersiz seçim. Lütfen 1 ile 5 arasında bir sayı girin.")


def add_expense(expenses: list[dict[str, object]]) -> None:
    title = input("Gider açıklaması: ").strip()
    category = input("Kategori: ").strip()
    amount = read_positive_float("Tutar: ")

    if not title:
        print("Gider açıklaması boş olamaz.")
        return

    if not category:
        print("Kategori boş olamaz.")
        return

    expenses.append({
        "title": title,
        "category": category,
        "amount": amount,
    })

    print("Gider eklendi.")


def list_expenses(expenses: list[dict[str, object]]) -> None:
    if not expenses:
        print("Henüz gider eklenmedi.")
        return

    print("\nGiderler:")

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['title']} | "
            f"Kategori: {expense['category']} | "
            f"Tutar: {expense['amount']:.2f} TL"
        )


def show_total(expenses: list[dict[str, object]]) -> None:
    total = sum(float(expense["amount"]) for expense in expenses)
    print(f"Toplam gider: {total:.2f} TL")


def filter_by_category(expenses: list[dict[str, object]]) -> None:
    if not expenses:
        print("Filtrelenecek gider yok.")
        return

    category = input("Filtrelenecek kategori: ").strip().lower()

    if not category:
        print("Kategori boş olamaz.")
        return

    filtered_expenses = [
        expense for expense in expenses
        if str(expense["category"]).lower() == category
    ]

    if not filtered_expenses:
        print("Bu kategoriye ait gider bulunamadı.")
        return

    list_expenses(filtered_expenses)


def main() -> None:
    expenses: list[dict[str, object]] = []

    while True:
        show_menu()
        choice = read_choice()

        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            list_expenses(expenses)
        elif choice == 3:
            show_total(expenses)
        elif choice == 4:
            filter_by_category(expenses)
        elif choice == 5:
            print("Program sonlandırıldı.")
            break


if __name__ == "__main__":
    main()

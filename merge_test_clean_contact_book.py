"""
merge_test_clean_contact_book.py

Temiz ve düzgün çalışan basit kişi rehberi CLI uygulaması.
Merge/code-review testinde zafiyetsiz normal dosya olarak kullanılabilir.

Çalıştırma:
    python merge_test_clean_contact_book.py
"""

from __future__ import annotations


def show_menu() -> None:
    print("\n=== Temiz Kişi Rehberi ===")
    print("1. Kişi ekle")
    print("2. Kişileri listele")
    print("3. Kişi ara")
    print("4. Kişi sil")
    print("5. Çıkış")


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


def add_contact(contacts: list[dict[str, str]]) -> None:
    name = input("Ad Soyad: ").strip()
    phone = input("Telefon: ").strip()
    email = input("E-posta: ").strip()

    if not name:
        print("Ad Soyad boş olamaz.")
        return

    if not phone:
        print("Telefon boş olamaz.")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
    })

    print("Kişi eklendi.")


def list_contacts(contacts: list[dict[str, str]]) -> None:
    if not contacts:
        print("Henüz kişi eklenmedi.")
        return

    print("\nKişiler:")

    for index, contact in enumerate(contacts, start=1):
        email_text = contact["email"] if contact["email"] else "-"
        print(
            f"{index}. {contact['name']} | "
            f"Telefon: {contact['phone']} | "
            f"E-posta: {email_text}"
        )


def search_contact(contacts: list[dict[str, str]]) -> None:
    if not contacts:
        print("Aranacak kişi yok.")
        return

    keyword = input("Aranacak isim: ").strip().lower()

    if not keyword:
        print("Arama metni boş olamaz.")
        return

    results = [
        contact for contact in contacts
        if keyword in contact["name"].lower()
    ]

    if not results:
        print("Eşleşen kişi bulunamadı.")
        return

    list_contacts(results)


def delete_contact(contacts: list[dict[str, str]]) -> None:
    if not contacts:
        print("Silinecek kişi yok.")
        return

    list_contacts(contacts)

    while True:
        value = input("Silinecek kişi numarası: ").strip()

        try:
            index = int(value)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        if 1 <= index <= len(contacts):
            removed = contacts.pop(index - 1)
            print(f"Kişi silindi: {removed['name']}")
            return

        print("Geçersiz kişi numarası.")


def main() -> None:
    contacts: list[dict[str, str]] = []

    while True:
        show_menu()
        choice = read_choice()

        if choice == 1:
            add_contact(contacts)
        elif choice == 2:
            list_contacts(contacts)
        elif choice == 3:
            search_contact(contacts)
        elif choice == 4:
            delete_contact(contacts)
        elif choice == 5:
            print("Program sonlandırıldı.")
            break


if __name__ == "__main__":
    main()

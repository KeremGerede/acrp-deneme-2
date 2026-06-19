"""
merge_test_clean_library_manager.py
Temiz ve düzgün çalışan basit kitaplık yönetimi CLI uygulaması.
Çalıştırma: python merge_test_clean_library_manager.py
"""

def show_menu():
    print("\n=== Temiz Kitaplık Yönetimi ===")
    print("1. Kitap ekle")
    print("2. Kitapları listele")
    print("3. Kitap ara")
    print("4. Kitap sil")
    print("5. Çıkış")

def read_choice():
    while True:
        value = input("Seçiminiz: ").strip()
        try:
            choice = int(value)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        if 1 <= choice <= 5:
            return choice

        print("Lütfen 1 ile 5 arasında seçim yapın.")

def add_book(books):
    title = input("Kitap adı: ").strip()
    author = input("Yazar: ").strip()

    if not title or not author:
        print("Kitap adı ve yazar boş olamaz.")
        return

    books.append({"title": title, "author": author})
    print("Kitap eklendi.")

def list_books(books):
    if not books:
        print("Henüz kitap eklenmedi.")
        return

    for index, book in enumerate(books, start=1):
        print(f"{index}. {book['title']} - {book['author']}")

def search_book(books):
    keyword = input("Aranacak kelime: ").strip().lower()

    if not keyword:
        print("Arama kelimesi boş olamaz.")
        return

    results = [
        book for book in books
        if keyword in book["title"].lower() or keyword in book["author"].lower()
    ]

    if not results:
        print("Eşleşen kitap bulunamadı.")
        return

    list_books(results)

def delete_book(books):
    if not books:
        print("Silinecek kitap yok.")
        return

    list_books(books)

    try:
        index = int(input("Silinecek kitap numarası: ").strip())
    except ValueError:
        print("Geçerli bir sayı girin.")
        return

    if 1 <= index <= len(books):
        removed = books.pop(index - 1)
        print(f"Kitap silindi: {removed['title']}")
    else:
        print("Geçersiz kitap numarası.")

def main():
    books = []

    while True:
        show_menu()
        choice = read_choice()

        if choice == 1:
            add_book(books)
        elif choice == 2:
            list_books(books)
        elif choice == 3:
            search_book(books)
        elif choice == 4:
            delete_book(books)
        elif choice == 5:
            print("Program sonlandırıldı.")
            break

if __name__ == "__main__":
    main()

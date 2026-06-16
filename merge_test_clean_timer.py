"""
merge_test_clean_timer.py
Temiz ve düzgün çalışan süre dönüştürücü CLI programı.
Çalıştırma: python merge_test_clean_timer.py
"""

def read_non_negative_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Lütfen geçerli bir tam sayı girin.")
            continue
        if number >= 0:
            return number
        print("Sayı negatif olamaz.")

def seconds_to_hms(total_seconds: int) -> tuple[int, int, int]:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return hours, minutes, seconds

def hms_to_seconds(hours: int, minutes: int, seconds: int) -> int:
    return hours * 3600 + minutes * 60 + seconds

def main() -> None:
    while True:
        print("\n=== Temiz Süre Dönüştürücü ===")
        print("1. Saniyeyi saat/dakika/saniyeye çevir")
        print("2. Saat/dakika/saniyeyi saniyeye çevir")
        print("3. Çıkış")
        choice = read_non_negative_int("Seçiminiz: ")

        if choice == 1:
            total = read_non_negative_int("Toplam saniye: ")
            h, m, s = seconds_to_hms(total)
            print(f"Sonuç: {h} saat, {m} dakika, {s} saniye")
        elif choice == 2:
            h = read_non_negative_int("Saat: ")
            m = read_non_negative_int("Dakika: ")
            s = read_non_negative_int("Saniye: ")
            print(f"Sonuç: {hms_to_seconds(h, m, s)} saniye")
        elif choice == 3:
            print("Program sonlandırıldı.")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()

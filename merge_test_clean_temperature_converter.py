"""
merge_test_clean_temperature_converter.py
Temiz ve düzgün çalışan sıcaklık dönüştürücü CLI uygulaması.
Çalıştırma: python merge_test_clean_temperature_converter.py
"""

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def read_number(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Geçerli bir sayı girin.")

def main():
    while True:
        print("\n=== Sıcaklık Dönüştürücü ===")
        print("1. Celsius -> Fahrenheit")
        print("2. Fahrenheit -> Celsius")
        print("3. Çıkış")

        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            celsius = read_number("Celsius: ")
            print(f"Sonuç: {celsius_to_fahrenheit(celsius):.2f} °F")
        elif choice == "2":
            fahrenheit = read_number("Fahrenheit: ")
            print(f"Sonuç: {fahrenheit_to_celsius(fahrenheit):.2f} °C")
        elif choice == "3":
            print("Program sonlandırıldı.")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()

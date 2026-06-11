"""
merge_test_clean_calculator.py

Düzgün çalışan temiz calculator programı.
Merge testinde zafiyetsiz/normal dosya olarak kullanılabilir.

Çalıştırma:
    python merge_test_clean_calculator.py
"""

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Sıfıra bölme yapılamaz.")
    return a / b

def read_number(label: str) -> float:
    while True:
        value = input(label).strip()
        try:
            return float(value)
        except ValueError:
            print("Geçerli bir sayı girin.")

def read_operation() -> str:
    valid = {"+", "-", "*", "/"}
    while True:
        operation = input("İşlem seçin (+, -, *, /): ").strip()
        if operation in valid:
            return operation
        print("Geçersiz işlem.")

def calculate(a: float, b: float, operation: str) -> float:
    if operation == "+":
        return add(a, b)
    if operation == "-":
        return subtract(a, b)
    if operation == "*":
        return multiply(a, b)
    if operation == "/":
        return divide(a, b)
    raise ValueError("Desteklenmeyen işlem.")

def main() -> None:
    print("=== Temiz Calculator ===")
    while True:
        a = read_number("Birinci sayı: ")
        operation = read_operation()
        b = read_number("İkinci sayı: ")

        try:
            print("Sonuç:", calculate(a, b, operation))
        except ValueError as error:
            print("Hata:", error)

        again = input("Yeni işlem? (e/h): ").strip().lower()
        if again != "e":
            print("Program sonlandırıldı.")
            break

if __name__ == "__main__":
    main()

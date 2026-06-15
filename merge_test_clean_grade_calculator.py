"""
merge_test_clean_grade_calculator.py

Temiz ve düzgün çalışan basit not ortalaması hesaplama CLI uygulaması.
Merge/code-review testinde zafiyetsiz normal dosya olarak kullanılabilir.

Çalıştırma:
    python merge_test_clean_grade_calculator.py
"""

from __future__ import annotations


def read_positive_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Lütfen geçerli bir tam sayı girin.")
            continue

        if number > 0:
            return number

        print("Sayı 0'dan büyük olmalıdır.")


def read_grade(prompt: str) -> float:
    while True:
        value = input(prompt).strip()

        try:
            grade = float(value)
        except ValueError:
            print("Lütfen geçerli bir not girin.")
            continue

        if 0 <= grade <= 100:
            return grade

        print("Not 0 ile 100 arasında olmalıdır.")


def calculate_average(grades: list[float]) -> float:
    if not grades:
        return 0.0

    return sum(grades) / len(grades)


def get_letter_grade(average: float) -> str:
    if average >= 90:
        return "AA"
    if average >= 85:
        return "BA"
    if average >= 80:
        return "BB"
    if average >= 75:
        return "CB"
    if average >= 70:
        return "CC"
    if average >= 60:
        return "DC"
    if average >= 50:
        return "DD"

    return "FF"


def main() -> None:
    print("=== Temiz Not Ortalaması Hesaplayıcı ===")

    course_count = read_positive_int("Kaç ders notu gireceksiniz? ")
    grades: list[float] = []

    for index in range(1, course_count + 1):
        grade = read_grade(f"{index}. ders notu: ")
        grades.append(grade)

    average = calculate_average(grades)
    letter_grade = get_letter_grade(average)

    print("\nSonuç")
    print(f"Ortalama: {average:.2f}")
    print(f"Harf notu: {letter_grade}")


if __name__ == "__main__":
    main()

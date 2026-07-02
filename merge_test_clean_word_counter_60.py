"""
merge_test_clean_word_counter_60.py
Temiz kelime sayacı CLI uygulaması.
Çalıştırma: python merge_test_clean_word_counter_60.py
"""
from __future__ import annotations

def normalize_text(text: str) -> str:
    result: list[str] = []
    for char in text:
        if char.isalnum() or char.isspace():
            result.append(char.lower())
        else:
            result.append(" ")
    return "".join(result)


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in normalize_text(text).split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def read_text() -> str:
    print("Metni girin. Bitirmek için boş satırda Enter basın.")
    input_lines: list[str] = []
    while True:
        line = input("> ")
        if not line:
            break
        input_lines.append(line)
    return "\n".join(input_lines)


def print_summary(counts: dict[str, int]) -> None:
    if not counts:
        print("Kelime bulunamadı.")
        return
    total_words = sum(counts.values())
    unique_words = len(counts)
    print(f"Toplam kelime: {total_words}")
    print(f"Benzersiz kelime: {unique_words}")


def print_top_words(counts: dict[str, int]) -> None:
    sorted_words = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    print("\nEn sık geçen kelimeler:")
    for index, item in enumerate(sorted_words[:5], start=1):
        word, count = item
        print(f"{index}. {word}: {count}")


def main() -> None:
    text = read_text()
    counts = count_words(text)
    print_summary(counts)
    print_top_words(counts)
if __name__ == "__main__":
    main()

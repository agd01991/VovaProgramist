import re
from collections import defaultdict

# Функция для чтения содержимого файла
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

# Функция для очистки текста от пунктуации и приведения к нижнему регистру
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).lower()

# Функция для подсчета частоты слов
def count_words(words):
    word_frequency = defaultdict(int)
    for word in words:
        word_frequency[word] += 1
    return word_frequency

# Функция для сортировки слов по частоте и лексикографически
def sort_words(word_frequency):
    return sorted(word_frequency.items(), key=lambda item: (-item[1], item[0]))

# Функция для записи результата в файл
def write_to_file(sorted_words, filename):
    with open(filename, 'w') as f:
        for word, count in sorted_words:
            f.write(f"{word}: {count}\n")

# Основной блок кода
if __name__ == "__main__":
    # Чтение и очистка текста
    text = read_file('resourse_1.txt')
    clean_text = clean_text(text)
    
    # Разбиение текста на слова и подсчет частоты
    words = clean_text.split()
    word_counts = count_words(words)
    
    # Сортировка слов по частоте и лексикографически
    sorted_words = sort_words(word_counts)
    
    # Запись результата в файл
    write_to_file(sorted_words, 'result_1.txt')
    
    # Опциональный вывод результата на консоль
    for word, count in sorted_words:
        print(f"{word}: {count}")

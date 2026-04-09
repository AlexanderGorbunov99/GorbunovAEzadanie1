import tkinter as tk
from tkinter import scrolledtext
import re
import pymorphy3
from collections import Counter

# Инициализация анализатора для лемматизации
russian_lemmatizer = pymorphy3.MorphAnalyzer()

# Набор стоп-слов (вынесен на уровень модуля, чтобы не создавать его при каждом нажатии)
RUSSIAN_STOP_WORDS = {
    'в', 'на', 'и', 'а', 'но', 'или', 'бы', 'же', 'то', 'вот', 'это',
    'как', 'так', 'что', 'чтобы', 'о', 'об', 'про', 'по', 'за', 'под',
    'над', 'до', 'из', 'с', 'к', 'у', 'от', 'для', 'без', 'через', 'между'
}

def analyze_text_frequencies():
    """Получает текст, лемматизирует его, считает частоту слов и выводит результат."""
    # Получаем текст из поля ввода
    raw_input_text = input_text_area.get("1.0", tk.END).strip()
    
    # Извлекаем слова (кириллица + дефисы), приводим к нижнему регистру
    extracted_words = re.findall(r'[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ]+)*', raw_input_text.lower())
    
    # Фильтрация стоп-слов
    filtered_words = [word for word in extracted_words if word not in RUSSIAN_STOP_WORDS]
    
    # Кэширование лемматизации
    lemmatization_cache = {}
    normalized_words = []
    
    for word in filtered_words:
        if word not in lemmatization_cache:
            lemmatization_cache[word] = russian_lemmatizer.parse(word)[0].normal_form
        normalized_words.append(lemmatization_cache[word])
        
    # Подсчёт частоты и сортировка
    word_frequencies = Counter(normalized_words)
    sorted_frequencies = word_frequencies.most_common()
    
    # Формирование текста результата
    output_content = ""
    if sorted_frequencies:
        top_word, freq = sorted_frequencies[0]
        output_content += f"Наиболее часто встречающееся слово: {top_word} — {freq} раз\n"
        
        rare_word, freq = sorted_frequencies[-1]
        output_content += f"Наиболее редкое слово: {rare_word} — {freq} раз\n"
        
        top_five = sorted_frequencies[:5]
        output_content += "\nТоп-5 самых частых слов:\n"
        for w, f in top_five:
            output_content += f"{w} — {f} раз\n"
            
    # Обновление поля вывода
    output_text_area.delete("1.0", tk.END)
    output_text_area.insert(tk.END, output_content)


# === Создание интерфейса ===
main_window = tk.Tk()
main_window.title("Подсчёт повторяющихся слов")
main_window.geometry("800x600")
main_window.resizable(True, True)

# Поле ввода текста
input_text_area = scrolledtext.ScrolledText(
    main_window, width=80, height=20, wrap=tk.WORD, font=("Arial", 10)
)
input_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
input_text_area.focus()

# Кнопка запуска анализа
analyze_button = tk.Button(
    main_window, text="Подсчитать слова", command=analyze_text_frequencies,
    bg="lightblue", font=("Arial", 10, "bold")
)
analyze_button.pack(pady=5, padx=10, fill=tk.X)

# Поле вывода результатов
output_text_area = scrolledtext.ScrolledText(
    main_window, width=80, height=20, wrap=tk.WORD, font=("Arial", 10), fg="blue"
)
output_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Главное меню
main_menu = tk.Menu(main_window)
main_window.config(menu=main_menu)

file_submenu = tk.Menu(main_menu, tearoff=0)
file_submenu.add_command(label="Очистить поля", command=lambda: input_text_area.delete("1.0", tk.END))
file_submenu.add_separator()
file_submenu.add_command(label="Выход", command=main_window.quit)
main_menu.add_cascade(label="Файл", menu=file_submenu)

main_window.mainloop()

import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def randomized_quick_sort(arr):
    """
    Реалізація рандомізованого алгоритму QuickSort, 
    де опорний елемент обирається випадковим чином.
    """
    # Створюємо копію масиву, щоб не змінювати оригінал
    arr_copy = arr.copy()
    
    # Внутрішня функція для розбиття масиву
    def partition(arr, low, high):
        # Обираємо випадковий опорний елемент і обмінюємо його з останнім елементом
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    # Внутрішня рекурсивна функція для сортування
    def quick_sort_internal(arr, low, high):
        if low < high:
            # Розбиваємо масив і отримуємо індекс опорного елемента
            pivot_idx = partition(arr, low, high)
            
            # Рекурсивно сортуємо підмасиви
            quick_sort_internal(arr, low, pivot_idx - 1)
            quick_sort_internal(arr, pivot_idx + 1, high)
    
    # Викликаємо сортування
    quick_sort_internal(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy

def deterministic_quick_sort(arr, pivot_rule='last'):
    """
    Реалізація детермінованого алгоритму QuickSort, 
    де опорний елемент обирається за фіксованим правилом.
    
    pivot_rule: 'first', 'last', або 'middle' для вибору
    відповідно першого, останнього або середнього елемента.
    """
    # Створюємо копію масиву, щоб не змінювати оригінал
    arr_copy = arr.copy()
    
    # Внутрішня функція для розбиття масиву
    def partition(arr, low, high, pivot_rule):
        # Вибір опорного елемента за вказаним правилом
        if pivot_rule == 'first':
            pivot_idx = low
        elif pivot_rule == 'middle':
            pivot_idx = (low + high) // 2
        else:  # 'last'
            pivot_idx = high
        
        # Обмінюємо опорний елемент з останнім
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    # Внутрішня рекурсивна функція для сортування
    def quick_sort_internal(arr, low, high, pivot_rule):
        if low < high:
            # Розбиваємо масив і отримуємо індекс опорного елемента
            pivot_idx = partition(arr, low, high, pivot_rule)
            
            # Рекурсивно сортуємо підмасиви
            quick_sort_internal(arr, low, pivot_idx - 1, pivot_rule)
            quick_sort_internal(arr, pivot_idx + 1, high, pivot_rule)
    
    # Викликаємо сортування
    quick_sort_internal(arr_copy, 0, len(arr_copy) - 1, pivot_rule)
    return arr_copy

def measure_sorting_time(sorting_function, arr, repeats=5):
    """
    Вимірює середній час виконання функції сортування на масиві.
    
    sorting_function: функція сортування
    arr: масив для сортування
    repeats: кількість повторень для усереднення
    """
    times = []
    
    for _ in range(repeats):
        # Створюємо копію масиву для кожного повторення
        arr_copy = arr.copy()
        
        # Вимірюємо час
        start_time = time.time()
        sorting_function(arr_copy)
        end_time = time.time()
        
        times.append(end_time - start_time)
    
    # Повертаємо середній час
    return sum(times) / repeats

def generate_random_array(size):
    """Генерує масив випадкових цілих чисел вказаного розміру."""
    return [random.randint(0, 1000000) for _ in range(size)]

def plot_comparison_chart(sizes, random_times, deterministic_times):
    """Будує графік порівняння часу виконання алгоритмів."""
    plt.figure(figsize=(10, 6))
    
    plt.plot(sizes, random_times, 'b-', label='Рандомізований QuickSort')
    plt.plot(sizes, deterministic_times, 'orange', label='Детермінований QuickSort')
    
    plt.xlabel('Розмір масиву')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння рандомізованого та детермінованого QuickSort')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('quicksort_comparison.png')
    plt.show()

def main():
    # Розміри масивів для тестування
    array_sizes = [10000, 50000, 100000, 500000]
    
    # Зберігаємо результати
    results = []
    random_times = []
    deterministic_times = []
    
    # Тестуємо на масивах різного розміру
    for size in array_sizes:
        print(f"Генерація масиву розміром {size}...")
        arr = generate_random_array(size)
        
        print(f"Вимірювання часу для масиву розміром {size}...")
        # Вимірюємо час рандомізованого QuickSort
        random_time = measure_sorting_time(randomized_quick_sort, arr)
        random_times.append(random_time)
        
        # Вимірюємо час детермінованого QuickSort
        deterministic_time = measure_sorting_time(lambda x: deterministic_quick_sort(x, 'last'), arr)
        deterministic_times.append(deterministic_time)
        
        # Додаємо результати
        results.append({
            'Розмір масиву': size,
            'Рандомізований QuickSort': random_time,
            'Детермінований QuickSort': deterministic_time
        })
        
        # Виводимо результати для поточного розміру
        print(f"Розмір масиву: {size}")
        print(f"   Рандомізований QuickSort: {random_time:.4f} секунд")
        print(f"   Детермінований QuickSort: {deterministic_time:.4f} секунд")
        print()
    
    # Будуємо графік
    plot_comparison_chart(array_sizes, random_times, deterministic_times)
    
    # Створюємо і виводимо підсумкову таблицю
    df = pd.DataFrame(results)
    print("\nПідсумкова таблиця результатів:")
    print(df.to_string(index=False))
    
    # Аналіз результатів
    print("\nАналіз результатів:")
    faster_count = sum(1 for r, d in zip(random_times, deterministic_times) if r < d)
    if faster_count > len(array_sizes) / 2:
        print("Рандомізований QuickSort в середньому швидший.")
    elif faster_count < len(array_sizes) / 2:
        print("Детермінований QuickSort в середньому швидший.")
    else:
        print("Обидва алгоритми демонструють приблизно однакову продуктивність.")
    
    # Обчислюємо середнє відносне відхилення
    relative_diff = [(d - r) / r * 100 for r, d in zip(random_times, deterministic_times)]
    avg_relative_diff = sum(relative_diff) / len(relative_diff)
    
    if avg_relative_diff > 1:
        print(f"Детермінований QuickSort в середньому на {avg_relative_diff:.2f}% повільніший.")
    elif avg_relative_diff < -1:
        print(f"Рандомізований QuickSort в середньому на {-avg_relative_diff:.2f}% повільніший.")
    else:
        print("Різниця у швидкості виконання незначна (менше 1%).")
    
    # Додатковий висновок щодо масштабування
    print("\nВисновок щодо масштабування:")
    if all(random_times[i]/random_times[i-1] < array_sizes[i]/array_sizes[i-1] * 1.2 
           for i in range(1, len(random_times))):
        print("Обидва алгоритми демонструють очікуване O(n log n) масштабування.")
    else:
        print("Спостерігаються відхилення від очікуваного O(n log n) масштабування.")

if __name__ == "__main__":
    main()
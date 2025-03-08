# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = set(can_teach_subjects)
        self.assigned_subjects = set()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.age} років, email: {self.email}"

def create_schedule(subjects, teachers):
    """
    Використовує жадібний алгоритм для призначення викладачів на предмети.
    
    Args:
        subjects: множина всіх предметів, які потрібно покрити
        teachers: список викладачів
        
    Returns:
        Список призначених викладачів або None, якщо покриття неможливе
    """
    # Створюємо копію множини предметів, щоб не змінювати оригінал
    remaining_subjects = set(subjects)
    
    # Список для зберігання призначених викладачів
    assigned_teachers = []
    
    # Перевіряємо, чи всі предмети можуть бути покриті наявними викладачами
    all_possible_subjects = set()
    for teacher in teachers:
        all_possible_subjects.update(teacher.can_teach_subjects)
    
    if not all_possible_subjects.issuperset(subjects):
        # Якщо деякі предмети не можуть бути покриті, повертаємо None
        return None
    
    # Продовжуємо призначення, поки не покриємо всі предмети
    while remaining_subjects:
        # Знаходимо найкращого викладача за нашими критеріями
        best_teacher = None
        best_coverage = 0
        
        for teacher in teachers:
            # Якщо вчитель вже призначений, пропускаємо його
            if teacher in assigned_teachers:
                continue
            
            # Визначаємо, скільки ще не покритих предметів може викладати цей викладач
            coverage = len(teacher.can_teach_subjects.intersection(remaining_subjects))
            
            if coverage > 0:  # Викладач може покрити хоча б один предмет
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_teacher = teacher
                elif coverage == best_coverage and best_teacher is not None:
                    # Якщо кількість предметів однакова, обираємо молодшого
                    if teacher.age < best_teacher.age:
                        best_teacher = teacher
        
        # Якщо не знайдено жодного викладача, який може покрити залишені предмети
        if best_teacher is None:
            return None
        
        # Призначаємо викладачу предмети
        subjects_to_assign = best_teacher.can_teach_subjects.intersection(remaining_subjects)
        best_teacher.assigned_subjects = subjects_to_assign
        
        # Видаляємо щойно призначені предмети зі списку тих, що залишилися
        remaining_subjects -= subjects_to_assign
        
        # Додаємо викладача до списку призначених
        assigned_teachers.append(best_teacher)
    
    return assigned_teachers

if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    
    # Створення списку викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {'Математика', 'Фізика'}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {'Хімія'}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {'Інформатика', 'Математика'}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {'Біологія', 'Хімія'}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {'Фізика', 'Інформатика'}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {'Біологія'})
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
        
        # Перевірка, чи всі предмети покриті
        covered_subjects = set()
        for teacher in schedule:
            covered_subjects.update(teacher.assigned_subjects)
        
        if covered_subjects == subjects:
            print("Всі предмети успішно розподілені.")
        else:
            missing = subjects - covered_subjects
            print(f"Увага! Не всі предмети розподілені. Відсутні: {', '.join(missing)}")
        
        # Перевірка кількості залучених викладачів
        print(f"Загальна кількість залучених викладачів: {len(schedule)} з {len(teachers)}")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")

    # Додаткове тестування: випадок неможливості покриття
    print("\nТест з неповним набором предметів:")
    test_subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія', 'Астрономія'}
    test_schedule = create_schedule(test_subjects, teachers)
    
    if test_schedule:
        print("Розклад успішно складено.")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
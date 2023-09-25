IGNORED_VALUES = {
    'uk': [
        '🗺 Показати де я зараз 📍', 
        '🔍 Пошук', 
        '🧔 Мій профіль', 
        '➕ Додати предмет'
    ],
    'en': [
        '🗺 Show where I am now 📍', 
        '🔍 Search', 
        '🧔 My Profile', 
        '➕ Add item'
    ],
    'pl': [
        '🗺 Pokaż, gdzie jestem teraz 📍', 
        '🔍 Szukaj', 
        '🧔 Mój profil', 
        '➕ Dodaj przedmiot'
    ],
    'ru': [
        '🗺 Показать, где я сейчас 📍', 
        '🔍 Поиск', 
        '🧔 Мой профиль', 
        '➕ Добавить предмет'
    ]
}

def should_ignore(value, language):
    return value in IGNORED_VALUES.get(language, [])
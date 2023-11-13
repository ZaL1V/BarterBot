IGNORED_VALUES = {
    'uk': [
        '🗺 Показати де я зараз 📍', 
        '🔍 Пошук', 
        '🧔 Мій профіль', 
        '➕ Додати предмет',
        '💾 Зберегти медіа',
        '🔄 Ввести медіа знову',
        '⬅️ Назад до опису'
    ],
    'en': [
        '🗺 Show where I am now 📍', 
        '🔍 Search', 
        '🧔 My Profile', 
        '➕ Add item',
        '💾 Save media',
        '🔄 Enter media again',
        '⬅️ Back to description'
    ],
    'pl': [
        '🗺 Pokaż, gdzie jestem teraz 📍', 
        '🔍 Szukaj', 
        '🧔 Mój profil', 
        '➕ Dodaj przedmiot',
        '💾 Zapisz media',
        '🔄 Wprowadź media ponownie',
        '⬅️ Wróć do opisu'
    ],
    'ru': [
        '🗺 Показать, где я сейчас 📍', 
        '🔍 Поиск', 
        '🧔 Мой профиль', 
        '➕ Добавить предмет',
        '💾 Сохранить медиа',
        '🔄 Ввести медиа заново',
        '⬅️ Назад к описанию'
    ]
}

def should_ignore(value, language):
    return value in IGNORED_VALUES.get(language, [])
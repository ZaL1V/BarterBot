def get_column_by_language(user_language):
    mapper = {
        'uk': 'name_uk',
        'en': 'name_en',
        'pl': 'name_pl',
        'ru': 'name_ru',
    }
    return mapper.get(user_language, None)
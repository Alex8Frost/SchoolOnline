def create_magazine_code(variables):
    """
    Создает код для симуляции издательства с заданными переменными.
    """
    title = variables['title']
    author = variables['author'] 
    year = variables['year']
    word_count = variables['word_count']
    
    # Создаем код динамически
    code = f'''title = {title!r}
author = {author!r}
year = {year}
word_count = {word_count}

separator = "=" * 50
article = f"""
{{separator}}
ИЗДАНИЕ: {title.upper()}
{{separator}}

Автор: {author}
Год публикации: {year}
Объём статьи: {word_count} слов

Описание:
Эта статья "{title}" была написана {author} в году {year}.
Объём статьи составляет {word_count} слов.
Это симуляция работы редактора издательства.
"""

result = article
'''
    return code
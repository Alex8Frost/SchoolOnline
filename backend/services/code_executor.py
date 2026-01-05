import ast
from templates.magazine import create_magazine_code

class MagazineExecutor:
    """
    Класс для безопасного выполнения кода в контексте издательства.
    """
    
    def validate_variables(self, variables: dict) -> tuple[bool, str]:
        """
        Проверяет корректность переменных для задания издательства.
        
        Args:
            variables: словарь с переменными для проверки
            
        Returns:
            tuple: (is_valid, error_message)
        """
        required_fields = ['title', 'author', 'year', 'word_count']
        
        # Проверяем наличие всех обязательных полей
        for field in required_fields:
            if field not in variables:
                return False, f"Отсутствует обязательное поле: {field}"
        
        # Валидация title
        title = variables['title']
        if not isinstance(title, str) or not title.strip():
            return False, "Поле 'title' должно быть непустой строкой"
        
        # Валидация author
        author = variables['author']
        if not isinstance(author, str) or not author.strip():
            return False, "Поле 'author' должно быть непустой строкой"
        
        # Валидация year
        try:
            year = int(variables['year'])
            if not (1900 <= year <= 2100):
                return False, "Поле 'year' должно быть в диапазоне 1900-2100"
        except (ValueError, TypeError):
            return False, "Поле 'year' должно быть числом"
        
        # Валидация word_count
        try:
            word_count = int(variables['word_count'])
            if word_count <= 0:
                return False, "Поле 'word_count' должно быть положительным числом"
        except (ValueError, TypeError):
            return False, "Поле 'word_count' должно быть числом"
        
        return True, ""
    
    def execute(self, variables: dict) -> tuple[bool, str]:
        """
        Безопасно выполняет код по шаблону издательства.
        
        Args:
            variables: словарь с переменными
            
        Returns:
            tuple: (success, result/error_message)
        """
        try:
            # Создаем код из шаблона с подставленными переменными
            code = create_magazine_code(variables)
            
            # Проверяем синтаксис кода
            try:
                ast.parse(code)
            except SyntaxError as e:
                return False, f"Ошибка синтаксиса: {e}"
            
            # Создаем ограниченное окружение для выполнения
            safe_globals = {
                '__builtins__': {}  # Полностью ограничиваем доступ к встроенным функциям
            }
            
            # Создаем локальное окружение
            safe_locals = {}
            
            # Выполняем код в безопасном окружении
            exec(code, safe_globals, safe_locals)
            
            # Получаем результат
            result = safe_locals.get('result', '')
            return True, str(result)
            
        except Exception as e:
            return False, f"Ошибка выполнения: {str(e)}"
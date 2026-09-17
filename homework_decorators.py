import os
from datetime import datetime
from functools import wraps
from typing import Union, Callable

from past_homework import calculate_salary

# =============================================
# УНИВЕРСАЛЬНЫЙ ДЕКОРАТО LOGGER (Задания 1 и 2)
# =============================================

def logger(path_or_func: Union[str, Callable] = 'main.log'):
    """Универсальный декоратор: работает и как @logger, и как @logger('file.log')"""
    
    # Случай 1: вызвали просто @logger (первый аргумент - это сама функция)
    if callable(path_or_func):
        func = path_or_func
        path = 'main.log'
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = func(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                log = f"{stamp}-[{func.__name__}]-<{args=}>-<{kwargs=}>-<{result=}>\n"
                f.write(log)
            return result
            
        return wrapper
    
    # Случай 2: вызвали @logger('путь_к_файлу') (первый аргумент - это строка)
    else:
        path = path_or_func
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                result = func(*args, **kwargs)
                with open(path, 'a', encoding='utf-8') as f:
                    log = f"{stamp}-[{func.__name__}]-<{args=}>-<{kwargs=}>-<{result=}>\n"
                    f.write(log)
                return result
                
            return wrapper
            
        return decorator


# =============================================
# ЗАДАНИЕ 1: Тесты для @logger без аргументов
# =============================================

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# =============================================
# ЗАДАНИЕ 2: Тесты для @logger('путь')
# =============================================

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)  # <-- Теперь используем logger вместо logger_param
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# =============================================
# ЗАДАНИЕ 3: Применение к коду из прошлого ДЗ
# =============================================

if __name__ == '__main__':
    test_1()
    test_2()
    
    if os.path.exists('calculate.log'):
        os.remove('calculate.log')

    # <-- Теперь используем logger вместо logger_param
    logged_generator = logger('calculate.log')(calculate_salary)
    logged_generator()
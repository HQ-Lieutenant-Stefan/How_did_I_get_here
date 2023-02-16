import os
# Gutenberg (gutenberg.org)


def get_dict_file(type_file=''):
    """
    Функция принимает строку обозначающею тип файлов (прим.: ".txt") и возвращает словарь из нужных файлов, где
    type_file = '.txt'
    Ключ     Значение
    1        имя_файла.txt
    2        имя_файла.txt
    3        имя_файла.txt
    :param type_file:
    :return: dict
    """
    if type_file == '':
        return f'\033[31mError! {get_dict_file.__name__}\033[0m'

    from os import listdir, path
    get_file_list = sorted(listdir(path.dirname(__file__)))

    for items in get_file_list[:]:
        if type_file not in items or '_write_all.txt' in items or \
                '_write_only_word.txt' in items or '_write_count_word.txt' in items:
            get_file_list.remove(items)

    get_file_dict = {}
    for index_val, val in enumerate(get_file_list):
        get_file_dict[str(index_val + 1)] = val
    return get_file_dict


def print_dict(dictionary: dict):
    """
    Функция принимает словарь и выводит выравненные значения, где
    Ключ        Значение
      1:        имя_файла.type_file
    ...:
     10:        имя_файла.type_file
    ...:
    100:        имя_файла.type_file
    :param dictionary: dict
    :return:
    """
    from collections import deque
    from os.path import dirname
    print('Cleaning Setting Exit')
    print(f"Все текстовые файле в директории {dirname(__file__)}:")
    for key_print_dict, value_print_dict in dictionary.items():
        print(f'{key_print_dict.rjust(len(deque(dictionary, maxlen=1)[0]))}: {value_print_dict}')


def delete_temporary_files():
    from os import path, listdir
    print(f'Функция очищает директорию от файлов созданных программой. '
          f'Файлы с названием "имя_write_all",\n"имя_write_count_word", "имя_write_only_word".')
    answering = input('Чтобы удалить файлы нажмите "Enter". Чтобы вернуться введите "return": ').lower()
    if answering in ['r', 'return']:
        return

    deleting_path = listdir(path.dirname(__file__))
    for item_delete in deleting_path[:]:
        if '_write_all.txt' not in item_delete and '_write_count_word.txt' not in item_delete\
                and 'write_only_word.txt' not in item_delete:
            deleting_path.remove(item_delete)

    for item_delete in deleting_path:
        os.remove(path.abspath(item_delete))


def setting():
    os.system('cls')
    global value_setting, current_setting
    print('Функция регулирует работу программы.\n'
          f'Текущие настройки {current_setting}   "all" — по умолчанию.')
    for key_setting, val_setting in value_setting.items():
        print(f'{val_setting}: {key_setting:<15}', end='')
        if val_setting == '1':
            print('Программа запишет в новом файле пронумерованный список всех слов и список уникальных слов.')
        elif val_setting == '2':
            print('Программа запишет в новом файле пронумерованный список всех слов.')
        else:
            print('Программа запишет в новом файле список уникальных слов.')
    while True:
        answering = input('Чтобы продолжить нажмите "Enter", чтобы вернуться введите "return": ')
        if answering in ['r', 'return']:
            return
        if answering in value_setting.keys():
            current_setting = value_setting[answering]
            break
        if answering in value_setting.values():
            for key_setting, val_setting in value_setting.items():
                if answering == val_setting:
                    current_setting = value_setting[key_setting]
            break


def exit_from_program():
    quit()


def do_something() -> str:
    while True:
        file_dict = get_dict_file('.txt')
        print_dict(file_dict)

        answer = str(input('Укажите имя или номер файла: '))

        global current_setting

        answer = answer.lower()
        if answer in ['c', 'clean', 'cleaning']:
            delete_temporary_files()
        elif answer in ['й', 'q', 'e', 'exit', 'quit', 'exiting']:
            exit_from_program()
        elif answer in ['s', 'setting']:
            setting()

        if answer in file_dict.keys():
            return file_dict[answer]
        if answer in file_dict.values():
            for key_something, value_something in file_dict.items():
                if answer == value_something or answer + '.txt' == value_something:
                    return value_something

        os.system('cls')


def del_punctuation(lines: list) -> list:
    from string import punctuation
    punctuation += '“”’‘—'
    # print(punctuation)
    for index_punctuation, item_punctuation in enumerate(lines):
        if set(item_punctuation) & set(punctuation):
            # print(f'{item} with punctuation')
            try:
                while item_punctuation[0] in punctuation:
                    item_punctuation = item_punctuation[1:]
                    # print(item)
                while item_punctuation[-1] in punctuation:
                    item_punctuation = item_punctuation[:-1]
                    # print(item)
                lines[index_punctuation] = item_punctuation
            except IndexError:
                pass
    return lines


def count_word_from_list(list_word: list) -> dict:
    count_word_from_list_dict = dict.fromkeys(list_word, 0)
    for item_word in list_word:
        count_word_from_list_dict[item_word] += 1
    return count_word_from_list_dict


def sorted_dict(val_dict: dict) -> dict:
    val_dict = dict(sorted(val_dict.items(), key=lambda items: items[1], reverse=True))
    return val_dict


def creating_new_file(name_files: str):

    def write_all(write_all_files: str):
        from time import time
        start_time = time()
        all_word = []

        with open(write_all_files, 'r', encoding='utf-8') as f:
            line = f.read().lower().strip().split()

            line = del_punctuation(line)

            all_word += line

        print(f'Файл {write_all_files} прочитан.')

        print('Считаем кол-во слов в файле.')
        count_word = count_word_from_list(all_word)
        print('Закончили подсчет.')

        count_word = sorted_dict(count_word)

        max_length_count_word = len(str(max(count_word.values())))
        max_length_only_word = len(str(len(all_word)))

        write_all_files = write_all_files.replace('.txt', '_write_all.txt')
        print(f'Начинаю запись файла {write_all_files}.')
        with open(write_all_files, 'w', encoding='utf-8') as f:
            for index, word in enumerate(all_word):
                f.write(f'{str(index + 1).rjust(max_length_only_word)}: {word}\n')

            f.write(f'--------------------------------------------------\n'
                    f'Всего слов в файле — {len(all_word)}\n'
                    f'--------------------------------------------------\n')

            for word, count in count_word.items():
                f.write(f'{str(count).rjust(max_length_count_word)} : {word}\n')

            f.write(f'--------------------------------------------------\n'
                    f'Всего слов в файле     — {len(all_word)}\n'
                    f'Уникальны слов в файле — {len(count_word.items())}\n'
                    f'Потрачено времени      — {time() - start_time:.3f} секунд\n'
                    f'--------------------------------------------------\n')
        print(f'Запись файла {write_all_files} закончена!')

    def write_only_word(only_word_files: str):
        from time import time
        start_time = time()
        all_word = []

        with open(only_word_files, 'r', encoding='utf-8') as f:
            line = f.read().lower().strip().split()

            line = del_punctuation(line)

            all_word += line

        print(f'Файл {only_word_files} прочитан.')

        max_length_only_word = len(str(len(all_word)))

        only_word_files = only_word_files.replace('.txt', '_write_only_word.txt')
        print(f'Начинаю запись файла {only_word_files}.')
        with open(only_word_files, 'w', encoding='utf-8') as f:
            for index, word in enumerate(all_word):
                f.write(f'{str(index + 1).rjust(max_length_only_word)}: {word}\n')

            f.write(f'--------------------------------------------------\n'
                    f'Всего слов в файле — {len(all_word)}\n'
                    f'Потрачено времени  — {time() - start_time:.3f} секунд\n'
                    f'--------------------------------------------------\n')

        print(f'Запись файла {only_word_files} закончена!')

    def write_count_word(count_word_files: str):
        from time import time
        start_time = time()
        all_word = []

        with open(count_word_files, 'r', encoding='utf-8') as f:
            line = f.read().lower().strip().split()

            line = del_punctuation(line)

            all_word += line

        print(f'Файл {count_word_files} прочитан.')

        print('Считаем кол-во слов в файле.')
        count_word = count_word_from_list(all_word)
        print('Закончили подсчет.')

        count_word = sorted_dict(count_word)

        max_length_count_word = len(str(max(count_word.values())))

        count_word_files = count_word_files.replace('.txt', '_write_count_word.txt')
        print(f'Начинаю запись файла {count_word_files}.')
        with open(count_word_files, 'w', encoding='utf-8') as f:

            for word, count in count_word.items():
                f.write(f'{str(count).rjust(max_length_count_word)} : {word}\n')

            f.write(f'--------------------------------------------------\n'
                    f'Уникальны слов в файле — {len(count_word.items())}\n'
                    f'Потрачено времени      — {time() - start_time:.3f} секунд\n'
                    f'--------------------------------------------------\n')
        print(f'Запись файла {count_word_files} закончена!')

    global current_setting
    if current_setting == '1':
        write_all(name_files)
    elif current_setting == '2':
        write_only_word(name_files)
    else:
        write_count_word(name_files)


if __name__ == '__main__':
    value_setting = {'all': '1', 'only_world': '2', 'count_word': '3'}
    current_setting = value_setting['all']

    while True:
        name_file = do_something()

        print('\nГотово! Ожидайте.')

        creating_new_file(name_file)

        input('Запись закончена, нажмите "Enter", чтобы продолжить: ')
        os.system('cls')

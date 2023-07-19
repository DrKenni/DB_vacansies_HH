from classes.DBManager import DBManager
from classes.Parser_HH import ParserHH
from utils import config


def main():
    name_database = input('Введите название для базы данных: ')

    #Подключение, создание баз данных, таблиц и их заполнение
    params = config('files/database.ini')
    hh = ParserHH()
    db = DBManager(params, name_database)
    db.create_db()
    db.create_tables()
    db.insert_data('employers', hh.get_employers())
    db.insert_data('vacancies', hh.get_vacancies())
    print('-' * 100)
    while True:
        command = input(
            "1 - Cписок всех компаний и количество вакансий у каждой компании;\n"
            "2 - Cписок всех вакансий с указанием названия компании,"
            " названия вакансии и зарплаты и ссылки на вакансию;\n"
            "3 - Cредняя зарплата по вакансиям;\n"
            "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n"
            "5 - Список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”;\n"
            "exit - Завершение работы.\n\n"
        )
        if command.lower() == 'exit':
            print('До свидания!')
            break
        elif command == '1':
            db.get_companies_and_vacancies_count()
        elif command == '2':
            db.get_all_vacancies()
        elif command == '3':
            db.get_avg_salary()
        elif command == '4':
            db.get_vacancies_with_higher_salary()
        elif command == '5':
            keyword = input('Введите слово: ')
            db.get_vacancies_with_keyword(keyword.title())
        else:
            print('Такой команды нет, попробуй снова!\n')
            continue


main()

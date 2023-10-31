from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI
import os.path
import json

DATABASE = 'headhunter'
USER = 'postgres'
PASSWORD = '1'

EMPLOYERS_FILE_PATH = os.path.join('.', 'json', 'employers.json')

main_menu = {
    '1': '1 - создать новую базу данных',
    '2': '2 - вывести количество открытых вакансий для каждой компании',
    '3': '3 - вывести все вакансии',
    '4': '4 - вывести среднюю зарплату среди всех вакансий',
    '5': '5 - вывести вакансии с зарплатой выше средней из всего списка вакансий',
    '6': '6 - вывести вакансии с заданным ключевым словом в названии',
    '7': '7 - выход'
}


def init_program(db: DBManager, hh: HeadHunterAPI):
    if not db.create_db():
        print('База данных с именем "Headhunter" уже существует. Продолжаем работать с ней')
    else:
        print("Будет создана база данных с вакансиями избранных компаний с HeadHunter")
        input("Для продолжения нажмите любую клавишу\n")
        create_new_db(db, hh)


def create_new_db(db: DBManager, hh: HeadHunterAPI):
    db.drop_db()
    db.create_db()

    with open(EMPLOYERS_FILE_PATH, encoding='UTF-8') as f:
        employers_dict = json.load(f)

    employers_list = []
    for employer_id in employers_dict.values():
        print('*', end='')
        employers_list.append(hh.get_employer_info(employer_id))
    db.fill_table_employers(employers_list)

    vacancies_list = []
    for employer_id in employers_dict.values():
        print('*', end='')
        vacancies_list.extend(hh.get_vacancies(employer_id, 2))
    db.fill_table_vacancies(vacancies_list)


def show_menu(menu: dict):
    print('\n')
    for item in menu.values():
        print(item)


def get_companies_and_vacancies_count(db_manager_obj: DBManager):
    lst = db_manager_obj.get_companies_and_vacancies_count()
    for item in lst:
        print(f"{item[0]} - {item[1]}")


def get_all_vacancies(db_manager_obj: DBManager):
    lst = db_manager_obj.get_all_vacancies()
    for item in lst:
        print(f"{item[0]} - {item[1]} - {item[2]}")


def get_avg_salary(db_manager_obj: DBManager):
    avg_salary = db_manager_obj.get_avg_salary()
    print(f"средняя зарплата по всем вакансиям составляет {avg_salary} руб.")


def get_vacancies_with_higher_salary(db_manager_obj: DBManager):
    lst = db_manager_obj.get_vacancies_with_higher_salary()
    for item in lst:
        print(f"{item[0]} - {item[1]} - {item[2]}")


def get_vacancies_with_keyword(db_manager_obj: DBManager):
    keyword = input('введите ключевое слово для поиска\n').strip()
    lst = db_manager_obj.get_vacancies_with_keyword(keyword)
    for item in lst:
        print(f"{item[0]} - {item[1]} - {item[2]}")

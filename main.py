from src.menu import *


def main():

    db = DBManager(DATABASE, USER, PASSWORD)
    hh = HeadHunterAPI()

    init_program(db, hh)

    while True:
        show_menu(main_menu)

        user_cmd = input().strip()

        if user_cmd == '1':
            create_new_db(db, hh)
        elif user_cmd == '2':
            get_companies_and_vacancies_count(db)
        elif user_cmd == '3':
            get_all_vacancies(db)
        elif user_cmd == '4':
            get_avg_salary(db)
        elif user_cmd == '5':
            get_vacancies_with_higher_salary(db)
        elif user_cmd == '6':
            get_vacancies_with_keyword(db)
        elif user_cmd == '7':
            return
        else:
            print('Неизвестная команда\n')


if __name__ == '__main__':
    main()

import requests
from src.vacancy import Vacancy
from src.employer import Employer


class HeadHunterAPI:

    def get_vacancies(self, employer_id: str, pages=10) -> list[Vacancy]:
        page = total_pages = 0
        vacancies = []

        while page <= total_pages:
            vacancies_per_page = []
            params = {
                'page': page,
                'per_page': 100,
                'employer_id': employer_id,
                'only_with_salary': True
            }
            response = requests.get('https://api.hh.ru/vacancies', params).json()

            if response['pages'] > pages:
                total_pages = pages
            else:
                total_pages = response['pages']

            for item in response['items']:
                vacancy = Vacancy(
                    item['alternate_url'],
                    item['id'],
                    item['name'],
                    item['salary']['from'],
                    item['snippet']['responsibility'],
                    item['snippet']['requirement'],
                    item['employer']['id']
                )
                vacancies_per_page.append(vacancy)
            vacancies.extend(vacancies_per_page)
            page += 1

        return vacancies

    def get_employer_info(self, emp_id: str) -> Employer:

        params = {
            'employer_id': emp_id,
        }

        response = requests.get(f"https://api.hh.ru/employers/{emp_id}", params).json()

        employer = Employer(
            response['alternate_url'],
            response['id'],
            response['name'],
            response['open_vacancies']
        )

        return employer

import requests
from src.abstract_api import AbstractAPI
from src.vacancy import Vacancy


class HeadHunterAPI(AbstractAPI):

    def get_vacancies(self, keyword: str, payment: int) -> list:

        params = {
            'page': 1,
            'per_page': 100,
            'text': keyword,
            'salary': payment,
            'currency': 'RUR',
            'only_with_salary': True
        }

        response = requests.get('https://api.hh.ru/vacancies', params).json()

        vacancy_list = []
        for item in response['items']:
            vacancy = Vacancy(
                item['name'],
                item['alternate_url'],
                item['salary']['from'],
                item['snippet']['responsibility'],
                item['snippet']['requirement'],
                'HH'
            )
            vacancy_list.append(vacancy)

        return vacancy_list

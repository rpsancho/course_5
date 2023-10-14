from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get_vacancies(self, keyword, payment):
        pass

class Employer:

    def __init__(
            self,
            alternate_url: str,
            hh_id: str,
            name: str,
            open_vacancies: int
    ):
        self.alternate_url = alternate_url
        self.hh_id = hh_id
        self.name = name
        self.open_vacancies = open_vacancies

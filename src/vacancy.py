class Vacancy:

    def __init__(
            self,
            alternate_url: str,
            hh_id: str,
            name: str,
            salary: int,
            description: str,
            requirements: str,
            employer_id: str
    ):
        self.alternate_url = alternate_url
        self.hh_id = hh_id
        self.name = name
        if salary is None:
            salary = 0
        self.salary = salary
        if description is None:
            self.description = ''
        else:
            self.description = description
        if requirements is None:
            self.requirements = ''
        else:
            self.requirements = requirements
        self.employer_id = employer_id

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def is_str_in_attr(self, string):
        values = self.__dict__.values()
        for value in values:
            if type(value) is str:
                if string in value:
                    return True
        return False

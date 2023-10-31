import psycopg2


class DBManager:

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

    def get_companies_and_vacancies_count(self) -> list:
        employers = self.__fetch_all("SELECT name, open_vacancies FROM employers;")
        return employers

    def get_all_vacancies(self) -> list:
        vacancies = self.__fetch_all("SELECT employers.name, vacancies.name, vacancies.salary_from, "
                                     "vacancies.alternate_url "
                                     "FROM employers RIGHT JOIN vacancies USING (employer_id);")
        return vacancies

    def get_avg_salary(self) -> float:
        avg_salary = self.__fetch_all("SELECT AVG(salary_from) FROM vacancies;")
        return round(avg_salary[0][0])

    def get_vacancies_with_higher_salary(self) -> list:
        vacancies = self.__fetch_all("SELECT employers.name, vacancies.name, vacancies.salary_from, "
                                     "vacancies.alternate_url "
                                     "FROM employers RIGHT JOIN vacancies USING (employer_id) "
                                     "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies);")
        return vacancies

    def get_vacancies_with_keyword(self, keyword) -> list:
        vacancies = self.__fetch_all(f"SELECT employers.name, vacancies.name, vacancies.salary_from, "
                                     f"vacancies.alternate_url "
                                     f"FROM employers RIGHT JOIN vacancies USING (employer_id)"
                                     f"WHERE LOWER(vacancies.name) LIKE '%{keyword.lower()}%';")
        return vacancies

    def __fetch_all(self, query: str) -> list:
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
            # conn.commit()
            # conn.close()
        return data

    def drop_db(self):
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password=self.password,
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {self.database};")
        except(psycopg2.errors.ObjectInUse):
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        f"FROM pg_stat_activity "
                        f"WHERE pg_stat_activity.datname = '{self.database}' "
                        f"AND pid <> pg_backend_pid();")
            cur.execute(f"DROP DATABASE IF EXISTS {self.database};")
        conn.close()

    def create_db(self) -> bool:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password=self.password,
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"CREATE DATABASE {self.database} WITH ENCODING='UTF8';")
        except(psycopg2.errors.DuplicateDatabase):
            return False
        conn.close()

        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
CREATE TABLE employers (
employer_id serial PRIMARY KEY NOT NULL,
alternate_url varchar(100) NOT NULL,
hh_id varchar(10) NOT NULL,
name varchar(100) NOT NULL,
open_vacancies int NOT NULL
);

CREATE TABLE vacancies (
vacancy_id serial PRIMARY KEY NOT NULL,
employer_id smallint REFERENCES employers(employer_id) NOT NULL,
alternate_url varchar(100) NOT NULL,
hh_id varchar(10) NOT NULL,
name varchar(100) NOT NULL,
salary_from int NOT NULL,
responsibility text NOT NULL,
requirement text NOT NULL
);
""")
        conn.close()
        return True

    def fill_table_employers(self, employers_list):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                for item in employers_list:
                    cur.execute(f"INSERT INTO employers "
                                f"(alternate_url, hh_id, name, open_vacancies) VALUES"
                                f"('{item.alternate_url}',"
                                f"'{item.hh_id}',"
                                f"'{item.name}',"
                                f"{item.open_vacancies});")
            conn.commit()

    def fill_table_vacancies(self, vacancies_list):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                for item in vacancies_list:
                    cur.execute(f"INSERT INTO vacancies "
                                f"(employer_id, alternate_url, hh_id, name, salary_from, responsibility, requirement) "
                                f"VALUES ((SELECT employer_id FROM employers WHERE hh_id = '{item.employer_id}'),"
                                f"'{item.alternate_url}',"
                                f"'{item.hh_id}',"
                                f"'{item.name}',"
                                f"{item.salary},"
                                f"'{item.description}',"
                                f"'{item.requirements}');")
            conn.commit()


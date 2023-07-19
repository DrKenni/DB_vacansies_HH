import requests


class ParserHH:
    """Класс для работы с НН.ru"""
    def __init__(self):
        self.employers_id = []

    def get_employers(self) -> list:
        """Получает список компаний с HH.ru"""
        employers = []
        res = requests.get('https://api.hh.ru/employers',
                           {"only_with_vacancies": "true",
                            "per_page": 15}).json()['items']
        for employer in res:
            self.employers_id.append(int(employer['id']))
            company = (employer['id'], employer['name'])
            employers.append(company)
        return employers

    def get_vacancies(self) -> list:
        """Получает список вакансий из полученного списка компаний"""
        vacancies = []
        for employer_id in self.employers_id:
            res = requests.get('https://api.hh.ru/vacancies',
                               {'employer_id': employer_id, 'per_page': 15}).json()['items']
            for item in res:
                vacancy = (
                    item['id'],
                    item['employer']['id'],
                    item['name'],
                    item['alternate_url'],
                    item['salary']['from'],
                    item['salary']['to']
                )
                vacancies.append(vacancy)
        return vacancies

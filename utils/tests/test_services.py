from typing import AnyStr, Dict
from utils.services import AdvertService
import pytest


class TestAdvertService:
    @pytest.fixture
    def item(self) -> Dict[AnyStr, AnyStr]:
        """
        Return one item 
        """
        return {
            "id": "40382875",
            "premium": False,
            "billing_type": {"id": "standard_plus", "name": "Стандарт плюс"},
            "relations": [],
            "name": "Customer Support Engineer (Remote)",
            "insider_interview": None,
            "response_letter_required": False,
            "area": {"id": "1", "name": "Москва", "url": "https://api.hh.ru/areas/1"},
            "salary": {"from": 130000, "to": 130000, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "allow_messages": True,
            "site": {"id": "hh", "name": "hh.ru"},
            "experience": {"id": "between3And6", "name": "От 3 до 6 лет"},
            "schedule": {"id": "remote", "name": "Удаленная работа"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "department": None,
            "contacts": None,
            "description": "<p><strong>Multilogin </strong>helps companies see the Internet through millions of computers. It’s a completely new terrain waiting for you to make an impact.</p> <p>We’re looking for a people-oriented person who’s no stranger to technical topics to help us make our users happy. This is a great opportunity to become a team member of a fast-growing profitable startup company revolving around focused hard work, growth, fun, and adventure.</p> <p>Multilogin is an international all-remote company registered in Estonia. Our team members reside in more than 10 countries from United Kingdom to Indonesia. We focus on developing sophisticated technologies (DeepTech) and pride ourselves for hiring an absolute best performer for every role.</p> <p>Will the next one be you? Apply now and let&#39;s find out!</p> <p> </p> <p><strong>What You’ll do:</strong></p> <ul> <li>Provide technical support to users via email and live chat</li> <li>Investigate user problems and prepare reports for developers</li> <li>Handle payment-related operations</li> <li>Connect with users through TeamViewer and investigate their issues</li> <li>Learn and document information about users</li> <li>Establish personal relationships with key customers</li> <li>Participate in software testing</li> </ul> <p><strong>What we expect: </strong></p> <ul> <li>Have 2 or more years of technical customer support experience</li> <li>Have excellent spoken and written communication skills in Russian</li> <li>Have very good spoken and written communication skills in English</li> <li>Are punctual and attentive to details</li> <li>Are able to multitask</li> <li>Are flexible in your working hours and able to work in mornings, evenings and weekends</li> <li>Have previous experience in compiling and translating documentation from Russian to English and vice versa</li> <li>Preferably have previous experience in working with Jira, Confluence, and TeamViewer</li> <li>Preferably have previous experience working with one of these languages: Python or Java</li> </ul> <p><strong>What we offer: </strong></p> <ul> <li>Culture of Freedom and Responsibility (be trusted to do the best thing without approvals and permission asking)</li> <li>Freedom to work from anywhere</li> <li>Top of the market compensation</li> <li>Benefits including sports membership and professional education compensation</li> <li>Home office equipment and furniture, fully on us</li> <li>Company retreats and meetings with international team members at least twice per year</li> </ul>",
            "branded_description": None,
            "vacancy_constructor_template": None,
            "key_skills": [
                {"name": "Atlassian Jira"},
                {"name": "Английский язык"},
                {"name": "Работа в команде"},
                {"name": "Грамотная речь"},
                {"name": "Грамотность"},
                {"name": "Креативность"},
                {"name": "Техническая поддержка"},
                {"name": "Техническая документация"},
                {"name": "Коммуникативные навыки"},
            ],
            "accept_handicapped": False,
            "accept_kids": False,
            "archived": False,
            "response_url": None,
            "specializations": [
                {
                    "id": "1.82",
                    "name": "Инженер",
                    "profarea_id": "1",
                    "profarea_name": "Информационные технологии, интернет, телеком",
                },
                {
                    "id": "1.211",
                    "name": "Поддержка, Helpdesk",
                    "profarea_id": "1",
                    "profarea_name": "Информационные технологии, интернет, телеком",
                },
            ],
            "code": None,
            "hidden": False,
            "quick_responses_allowed": False,
            "driver_license_types": [],
            "accept_incomplete_resumes": False,
            "employer": {
                "id": "5034722",
                "name": "Multilogin Software Ltd.",
                "url": "https://api.hh.ru/employers/5034722",
                "alternate_url": "https://hh.ru/employer/5034722",
                "logo_urls": {
                    "original": "https://hhcdn.ru/employer-logo-original/793320.jpg",
                    "90": "https://hhcdn.ru/employer-logo/3614167.jpeg",
                    "240": "https://hhcdn.ru/employer-logo/3614168.jpeg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=5034722",
                "trusted": True,
            },
            "published_at": "2020-12-09T17:02:06+0300",
            "created_at": "2020-12-09T17:02:06+0300",
            "negotiations_url": None,
            "suitable_resumes_url": None,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=40382875",
            "has_test": False,
            "test": None,
            "alternate_url": "https://hh.ru/vacancy/40382875",
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
        }
    
    def test_get_city(self, item):
        area = item.get('area')
        advert = AdvertService(item)
        assert area == advert._get_city()


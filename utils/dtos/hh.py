import typing as t

from pydantic import BaseModel


class BillingType(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class InsiderInterview(BaseModel):
    id: t.Optional[int]
    url: t.Optional[str]


class Area(BaseModel):
    id: t.Optional[int]
    name: t.Optional[str]
    url: str


class Salary(BaseModel):
    from_value: t.Optional[int]
    to: t.Optional[int]
    currency: t.Optional[str]
    gross: t.Optional[bool]

    class Config:
        fields = {"from_value": "from"}


class Type(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class Station(BaseModel):
    station_id: t.Optional[str]
    station_name: t.Optional[str]
    line_id: t.Optional[str]
    line_name: t.Optional[str]
    lat: t.Optional[float]
    lng: t.Optional[float]


class Address(BaseModel):
    city: t.Optional[str]
    street: t.Optional[str]
    building: t.Optional[str]
    description: t.Optional[str]
    lat: t.Optional[float]
    lng: t.Optional[float]
    metro_stations: t.Optional[t.List[Station]]


class Experience(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class Schedule(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class Employment(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class Department(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]


class Phone(BaseModel):
    country: t.Optional[str]
    city: t.Optional[str]
    number: t.Optional[str]
    comment: t.Optional[str]


class Contacts(BaseModel):
    name: t.Optional[str]
    email: t.Optional[str]
    phones: t.Optional[t.List[Phone]]


class KeySkill(BaseModel):
    name: t.Optional[str]


class Specializations(BaseModel):
    id: t.Optional[str]
    name: t.Optional[str]
    profarea_id: t.Optional[str]
    profarea_name: t.Optional[str]


class LogoUrls(BaseModel):
    size_90: t.Optional[str]
    size_240: t.Optional[str]
    original: t.Optional[str]

    class Config:
        fields = {"size_90": "90", "size_240": "240"}


class Employer(BaseModel):
    id: t.Optional[int]
    name: t.Optional[str]
    url: t.Optional[str]
    alternate_url: t.Optional[str]
    logo_urls: t.Optional[LogoUrls]
    vacancies_url: t.Optional[str]
    trusted: t.Optional[bool]


class Item(BaseModel):
    id: t.Optional[int]
    premium: t.Optional[bool]
    billing_type: t.Optional[BillingType]
    name: t.Optional[str]
    insider_interview: t.Optional[InsiderInterview]
    response_letter_required: t.Optional[bool]
    area: t.Optional[Area]
    salary: t.Optional[Salary]
    type: t.Optional[Type]
    address: t.Optional[Address]
    allow_messages: t.Optional[bool]
    experience: t.Optional[Experience]
    schedule: t.Optional[Schedule]
    employment: t.Optional[Employment]
    department: t.Optional[Department]
    contacts: t.Optional[Contacts]
    description: t.Optional[str]
    branded_description: t.Optional[str]
    key_skills: t.Optional[t.List[KeySkill]]
    accept_handicapped: t.Optional[bool]
    accept_kids: t.Optional[bool]
    archived: t.Optional[bool]
    response_url: t.Optional[str]
    specializations: t.Optional[t.List[Specializations]]
    hidden: t.Optional[bool]
    employer: t.Optional[Employer]
    published_at: t.Optional[str]
    created_at: t.Optional[str]
    apply_alternate_url: t.Optional[str]
    has_test: t.Optional[bool]
    alternate_url: t.Optional[str]

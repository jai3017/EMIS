from typing import List, Optional
from pydantic import BaseModel, Field
from fhirclient.models.patient import Patient as FHIRPatient
from fhirclient.models.fhirabstractbase import FHIRValidationError
from sqlalchemy import create_engine, Column, Integer, String,JSON
from database import Base


class ValueCoding(BaseModel):
    system: str
    code: str
    display: str


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(JSON, index=True)
    gender = Column(String)
    birthDate = Column(String)


class ExtensionDetail(BaseModel):
    url: str
    valueCoding: Optional[ValueCoding] = None
    valueString: Optional[str] = None
    valueCode: Optional[str] = None
    valueAddress: Optional[dict] = None
    valueDecimal: Optional[float] = None
    extension: Optional[List['ExtensionDetail']] = None


class IdentifierType(BaseModel):
    coding: List[ValueCoding]
    text: str


class Identifier(BaseModel):
    system: str
    value: str
    type: Optional[IdentifierType] = None


class HumanName(BaseModel):
    use: str
    family: str
    given: List[str]
    prefix: Optional[List[str]] = None


class Telecom(BaseModel):
    system: str
    value: str
    use: str


class Address(BaseModel):
    extension: Optional[List[ExtensionDetail]] = None
    line: List[str]
    city: str
    state: str
    country: str


class Coding(BaseModel):
    system: str
    code: str
    display: str


class MaritalStatus(BaseModel):
    coding: List[Coding]
    text: str


class Language(BaseModel):
    coding: List[Coding]
    text: str


class Communication(BaseModel):
    language: Language


class Meta(BaseModel):
    profile: List[str]


class Text(BaseModel):
    status: str
    div: str


class PatientResource(BaseModel):
    resourceType: str
    id: str
    meta: Meta
    text: Text
    extension: List[ExtensionDetail]
    identifier: List[Identifier]
    name: List[HumanName]
    telecom: List[Telecom]
    gender: str
    birthDate: str
    deceasedDateTime: Optional[str] = None
    address: List[Address]
    maritalStatus: MaritalStatus
    multipleBirthBoolean: bool
    communication: List[Communication]


class Entry(BaseModel):
    fullUrl: str
    resource: PatientResource
    request: dict


class FHIRData(BaseModel):
    entry: List[Entry]

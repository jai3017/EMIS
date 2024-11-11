from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from models import PatientResource, Patient
from database import Base, engine, get_session_local, create_data
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.humanname import HumanName
import uvicorn

app = FastAPI(separate_input_output_schemas=False)

Base.metadata.create_all(bind=engine)


@app.post("/patients/", response_model=PatientResource)
def create_patient(patient: PatientResource, db: Session = Depends(get_session_local)):
    try:
        fhir_patient_resource = FHIRPatient(resourceType="Patient",
                                            name=[name.dict() for name in patient.name],
                                            gender=patient.gender, birthDate=patient.birthDate,
                                            meta=patient.meta.dict() if patient.meta else None,
                                            text=patient.text.dict() if patient.text else None,
                                            extension=[ext.dict() for ext in
                                                       patient.extension] if patient.extension else None,
                                            identifier=[id.dict() for id in
                                                        patient.identifier] if patient.identifier else None,
                                            telecom=[tel.dict() for tel in
                                                     patient.telecom] if patient.telecom else None,
                                            deceasedDateTime=patient.deceasedDateTime, address=[addr.dict() for addr in
                                                                                                patient.address] if patient.address else None,
                                            maritalStatus=patient.maritalStatus.dict() if patient.maritalStatus else None,
                                            multipleBirthBoolean=patient.multipleBirthBoolean,
                                            communication=[comm.dict() for comm in
                                                           patient.communication] if patient.communication else None)
        patient_dict = fhir_patient_resource.dict()

        db_patient = Patient(
            name=patient_dict['name'],
            gender=patient_dict['gender'],
            birthDate=patient_dict['birthDate']
        )
        create_data(db, db_patient)

        return patient
    except Exception as d:
        print(d)


@app.get("/patients/{patient_id}", response_model=PatientResource)
def get_patient(patient_id: int, db: Session = Depends(get_session_local)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    fhir_patient_resource = FHIRPatient(resourceType="Patient",
                                        name=db_patient.name,
                                        gender=db_patient.gender,
                                        birthDate=db_patient.birthDate)
    return fhir_patient_resource.dict()


@app.get("/patients/{patient_name}", response_model=PatientResource)
def get_patient(patient_name: int, db: Session = Depends(get_session_local)):
    db_patient = db.query(Patient).filter(Patient.name == patient_name).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    fhir_patient_resource = FHIRPatient(resourceType="Patient",
                                        name=db_patient.name,
                                        gender=db_patient.gender,
                                        birthDate=db_patient.birthDate)
    return fhir_patient_resource.dict()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1, log_level="debug")

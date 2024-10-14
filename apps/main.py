from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import GeneralCompany, SubCompany, PM, Task, GeneralControl
from .database import engine, SessionLocal, Base
from pydantic import BaseModel

app = FastAPI()



def check_status(db: Session):
    
    pms = db.query(PM).all()
    for pm in pms:
        if all(task.status == "done" for task in pm.tasks):
            pm.status = "done"
        else:
            pm.status = "processing"
    
    sub_companies = db.query(SubCompany).all()
    for sub_company in sub_companies:
        if all(pm.status == "done" for pm in sub_company.pms):
            sub_company.status = "done"
        else:
            sub_company.status = "processing"
    

    general_companies = db.query(GeneralCompany).all()
    for general_company in general_companies:
        if all(sub_company.status == "done" for sub_company in general_company.sub_companies):
            general_company.status = "done"
        else:
            general_company.status = "processing"
    
    db.commit()

def general_control_update_status(db: Session, general_company_id: int, new_status: str):
    if new_status not in ["processing", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    general_company = db.query(GeneralCompany).filter(GeneralCompany.id == general_company_id).first()
    if not general_company:
        raise HTTPException(status_code=404, detail="General Company not found")
    
    for sub_company in general_company.sub_companies:
        sub_company.status = new_status
        for pm in sub_company.pms:
            pm.status = new_status
            for task in pm.tasks:
                task.status = new_status
    
    general_company.status = new_status
    db.commit()

def general_control_check_all_statuses(db: Session, general_company_id: int):
    general_company = db.query(GeneralCompany).filter(GeneralCompany.id == general_company_id).first()
    if not general_company:
        raise HTTPException(status_code=404, detail="General Company not found")

    all_done = all(sub_company.status == "done" for sub_company in general_company.sub_companies)
    
    return {"all_done": all_done}





class TaskCreate(BaseModel):
    name: str
    status: str

class PMCreate(BaseModel):
    name: str

class SubCompanyCreate(BaseModel):
    name: str

class GeneralCompanyCreate(BaseModel):
    name: str

class GeneralControlUpdate(BaseModel):
    status: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# GeneralCompany yaratish
@app.post("/general-company/")
def create_general_company(company: GeneralCompanyCreate, db: Session = Depends(get_db)):
    db_company = GeneralCompany(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# SubCompany yaratish
@app.post("/sub-company/")
def create_sub_company(sub_company: SubCompanyCreate, general_company_id: int, db: Session = Depends(get_db)):
    db_sub_company = SubCompany(name=sub_company.name, general_company_id=general_company_id)
    db.add(db_sub_company)
    db.commit()
    db.refresh(db_sub_company)
    return db_sub_company

# PM yaratish
@app.post("/pm/")
def create_pm(pm: PMCreate, sub_company_id: int, db: Session = Depends(get_db)):
    db_pm = PM(name=pm.name, sub_company_id=sub_company_id)
    db.add(db_pm)
    db.commit()
    db.refresh(db_pm)
    return db_pm

# Task yaratish
@app.post("/task/")
def create_task(task: TaskCreate, pm_id: int, db: Session = Depends(get_db)):
    db_task = Task(name=task.name, status=task.status, pm_id=pm_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Barcha statuslarni tekshirish
@app.get("/check-status/")
def update_status(db: Session = Depends(get_db)):
    check_status(db)
    return {"message": "Status updated based on tasks completion"}


@app.post("/general-control/{general_company_id}/update-status/")
def update_general_control_status(general_company_id: int, general_control: GeneralControlUpdate, db: Session = Depends(get_db)):
    general_control_update_status(db, general_company_id, general_control.status)
    return {"message": f"General Company {general_company_id} and all related statuses updated to {general_control.status}"}

@app.get("/general-control/{general_company_id}/check-status/")
def check_general_control_status(general_company_id: int, db: Session = Depends(get_db)):
    status_check = general_control_check_all_statuses(db, general_company_id)
    return status_check

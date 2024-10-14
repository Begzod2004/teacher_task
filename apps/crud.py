from sqlalchemy.orm import Session
from . import models, schemas

# Task uchun CRUD
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate, pm_id: int):
    db_task = models.Task(**task.dict(), pm_id=pm_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# PM uchun CRUD
def update_pm_status(db: Session, pm: models.PM):
    if all(task.status == 'done' for task in pm.tasks):
        pm.status = 'done'
        db.commit()

def update_sub_company_status(db: Session, sub_company: models.SubCompany):
    if all(pm.status == 'done' for pm in sub_company.pms):
        sub_company.status = 'done'
        db.commit()

def update_general_company_status(db: Session, general_company: models.GeneralCompany):
    if all(sub_company.status == 'done' for sub_company in general_company.sub_companies):
        general_company.status = 'done'
        db.commit()

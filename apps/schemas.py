from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    status: str = 'pending'

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    pm_id: int

    class Config:
        orm_mode = True

class PMBase(BaseModel):
    name: str
    status: str = 'in_progress'

class PMCreate(PMBase):
    pass

class PM(PMBase):
    id: int
    sub_company_id: int
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class SubCompanyBase(BaseModel):
    name: str
    status: str = 'in_progress'

class SubCompanyCreate(SubCompanyBase):
    pass

class SubCompany(SubCompanyBase):
    id: int
    general_company_id: int
    pms: list[PM] = []

    class Config:
        orm_mode = True

class GeneralCompanyBase(BaseModel):
    name: str
    status: str = 'in_progress'

class GeneralCompanyCreate(GeneralCompanyBase):
    pass

class GeneralCompany(GeneralCompanyBase):
    id: int
    sub_companies: list[SubCompany] = []

    class Config:
        from_attributes = True

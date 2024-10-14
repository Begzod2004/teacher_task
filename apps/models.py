from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class GeneralCompany(Base):
    __tablename__ = 'general_company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="processing")  # Status is either "processing" or "done"
    sub_companies = relationship("SubCompany", back_populates="general_company")

class SubCompany(Base):
    __tablename__ = 'sub_company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="processing")
    general_company_id = Column(Integer, ForeignKey('general_company.id'))
    general_company = relationship("GeneralCompany", back_populates="sub_companies")
    pms = relationship("PM", back_populates="sub_company")

class PM(Base):
    __tablename__ = 'pm'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="processing")
    sub_company_id = Column(Integer, ForeignKey('sub_company.id'))
    sub_company = relationship("SubCompany", back_populates="pms")
    tasks = relationship("Task", back_populates="pm")

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="processing")  # Task starts in "processing" status
    pm_id = Column(Integer, ForeignKey('pm.id'))
    pm = relationship("PM", back_populates="tasks")
    is_active = Column(Boolean, default=True)

class GeneralControl(Base):
    __tablename__ = 'general_control'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="pending")  # Control status
    general_company_id = Column(Integer, ForeignKey('general_company.id'))
    general_company = relationship("GeneralCompany")

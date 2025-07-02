<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from db import get_engine

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    summary = relationship('ProjectSummary', back_populates='project', uselist=False)
    data = relationship('ProjectData', back_populates='project')

class ProjectSummary(Base):
    __tablename__ = 'project_summaries'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), unique=True)
    total_routes = Column(Integer)
    total_drivers = Column(Integer)
    total_dead_km = Column(Float)
    optimized_dead_km = Column(Float)
    swap_chains = Column(Integer)
    deviations = Column(Integer)
    project = relationship('Project', back_populates='summary')

class ProjectData(Base):
    __tablename__ = 'project_data'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    driver = Column(String(64))
    pickup_point = Column(String(128))
    lat = Column(Float)
    lon = Column(Float)
    original_dead_km = Column(Float)
    optimized_dead_km = Column(Float)
    swap_chain = Column(String(64))
    deviation = Column(Float)
    project = relationship('Project', back_populates='data')
    __table_args__ = (UniqueConstraint('project_id', 'driver', 'pickup_point', name='_project_driver_pickup_uc'),)

def create_tables():
    engine = get_engine()
=======
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from db import get_engine

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    summary = relationship('ProjectSummary', back_populates='project', uselist=False)
    data = relationship('ProjectData', back_populates='project')

class ProjectSummary(Base):
    __tablename__ = 'project_summaries'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), unique=True)
    total_routes = Column(Integer)
    total_drivers = Column(Integer)
    total_dead_km = Column(Float)
    optimized_dead_km = Column(Float)
    swap_chains = Column(Integer)
    deviations = Column(Integer)
    project = relationship('Project', back_populates='summary')

class ProjectData(Base):
    __tablename__ = 'project_data'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    driver = Column(String(64))
    pickup_point = Column(String(128))
    lat = Column(Float)
    lon = Column(Float)
    original_dead_km = Column(Float)
    optimized_dead_km = Column(Float)
    swap_chain = Column(String(64))
    deviation = Column(Float)
    project = relationship('Project', back_populates='data')
    __table_args__ = (UniqueConstraint('project_id', 'driver', 'pickup_point', name='_project_driver_pickup_uc'),)

def create_tables():
    engine = get_engine()
>>>>>>> d3f6fb7d51a260ae1366c1d54cb2e1143dc7d9d3
    Base.metadata.create_all(engine) 
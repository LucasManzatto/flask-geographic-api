from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


# Define the SQLAlchemy model class for the table Trips
class Trips(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    region = Column(String(255))
    origin_coord = Column(Geometry(geometry_type="POINT"))
    destination_coord = Column(Geometry(geometry_type="POINT"))
    datetime = Column(DateTime)
    datasource = Column(String(255))

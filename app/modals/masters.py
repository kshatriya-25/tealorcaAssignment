#OM VIGHNHARTAYE NAMO NAMAH :

from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
from ..database.base_class import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)



class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)


class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))

    role = relationship("Role")
    permission = relationship("Permission")


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., temperature, humidity
    unit = Column(String(20))  # optional: °C, %, etc.
    description = Column(String(255), nullable=True)

    sensor_data = relationship("SensorData", back_populates="parameter")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=False)
    value = Column(Float, nullable=False)
    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    parameter = relationship("Parameter", back_populates="sensor_data")

#OM VIGHNHARTAYE NAMO NAMAH :


from ...modals.masters import Parameter
from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List
from sqlalchemy.orm import Session
from ...database.session import getdb
from pydantic import ValidationError

router = APIRouter(prefix="/parameter", tags=["Parameter"])

@router.post("/create")
def create_parameter(
    name: str = Form(...),
    unit: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(getdb)
):
    existing = db.query(Parameter).filter(Parameter.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Parameter already exists")
    try:
        db_param = Parameter(name=name, unit=unit, description=description)
        db.add(db_param)
        db.commit()
        db.refresh(db_param)
        return db_param
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.get("/get/{param_id}")
def get_parameter_by_id(param_id: int, db: Session = Depends(getdb)):
    parameter = db.query(Parameter).filter(Parameter.id == param_id).first()
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return parameter

@router.get("/all")
def get_all_parameters(db: Session = Depends(getdb)):
    parameters = db.query(Parameter).all()
    return parameters

@router.put("/{param_id}")
def update_parameter(
    param_id: int,
    name: str = Form(...),
    unit: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(getdb)
):
    parameter = db.query(Parameter).filter(Parameter.id == param_id).first()
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")

    existing = db.query(Parameter).filter(Parameter.name == name, Parameter.id != param_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Another parameter with this name already exists")

    parameter.name = name
    parameter.unit = unit
    parameter.description = description
    db.commit()
    db.refresh(parameter)
    return parameter

@router.delete("/{param_id}")
def delete_parameter(param_id: int, db: Session = Depends(getdb)):
    parameter = db.query(Parameter).filter(Parameter.id == param_id).first()
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")
    db.delete(parameter)
    db.commit()
    return {"detail": "Parameter deleted successfully"}

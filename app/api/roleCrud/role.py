#OM VIGHNHARTAYE NAMO NAMAH :


from ...modals.masters import Role
from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List
from sqlalchemy.orm import Session
from ...database.session import getdb
from pydantic import ValidationError

router = APIRouter(prefix="/role", tags=["Role"])

@router.post("/create")
def create_role(name: str = Form(...), db: Session = Depends(getdb)):
    existing = db.query(Role).filter(Role.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    try:
        db_role = Role(name=name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.get("/get/{role_id}")
def get_role_by_id(role_id: int, db: Session = Depends(getdb)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/all")
def get_all_roles(db: Session = Depends(getdb)):
    roles = db.query(Role).all()
    return roles

@router.put("/{role_id}")
def update_role(role_id: int, name: str = Form(...), db: Session = Depends(getdb)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    existing = db.query(Role).filter(Role.name == name, Role.id != role_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Another role with this name already exists")

    role.name = name
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(getdb)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}

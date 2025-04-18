# OM VIGHNHARTAYE NAMO NAMAH :

from ...modals.masters import User, Role
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ...database.session import getdb
from pydantic import ValidationError

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password_hash: str = Form(...),  # Ideally, hash the password before storing
    role_id: int = Form(...),
    db: Session = Depends(getdb),
):
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    try:
        user = User(username=username, email=email, password_hash=password_hash, role_id=role_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


@router.get("/get/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(getdb)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/all")
def get_all_users(db: Session = Depends(getdb)):
    users = db.query(User).all()
    return users


@router.put("/{user_id}")
def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    password_hash: str = Form(...),
    role_id: int = Form(...),
    db: Session = Depends(getdb),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if db.query(User).filter(User.username == username, User.id != user_id).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    if db.query(User).filter(User.email == email, User.id != user_id).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user.username = username
    user.email = email
    user.password_hash = password_hash
    user.role_id = role_id

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(getdb)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

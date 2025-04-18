# OM VIGHNHARTAYE NAMO NAMAH :

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ...modals.masters import Permission, Role, RolePermission
from ...database.session import getdb

router = APIRouter(prefix="/permission", tags=["Permission"])

# Create a permission
@router.post("/create")
def create_permission(name: str = Form(...), db: Session = Depends(getdb)):
    existing = db.query(Permission).filter(Permission.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    perm = Permission(name=name)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm

# Get permission by ID
@router.get("/get/{perm_id}")
def get_permission(perm_id: int, db: Session = Depends(getdb)):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    return perm

# List all permissions
@router.get("/all")
def get_all_permissions(db: Session = Depends(getdb)):
    return db.query(Permission).all()

# Update permission
@router.put("/{perm_id}")
def update_permission(perm_id: int, name: str = Form(...), db: Session = Depends(getdb)):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")

    existing = db.query(Permission).filter(Permission.name == name, Permission.id != perm_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Another permission with this name already exists")

    perm.name = name
    db.commit()
    db.refresh(perm)
    return perm

# Delete permission
@router.delete("/{perm_id}")
def delete_permission(perm_id: int, db: Session = Depends(getdb)):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Delete from RolePermission table first
    db.query(RolePermission).filter(RolePermission.permission_id == perm_id).delete()
    db.delete(perm)
    db.commit()
    return {"detail": "Permission deleted successfully"}

# Assign permission to role
@router.post("/assign")
def assign_permission_to_role(
    role_id: int = Form(...),
    permission_id: int = Form(...),
    db: Session = Depends(getdb)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    existing = db.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already assigned to role")

    role_perm = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(role_perm)
    db.commit()
    return {"detail": f"Permission '{permission.name}' assigned to role '{role.name}'"}

# Remove permission from role
@router.post("/remove")
def remove_permission_from_role(
    role_id: int = Form(...),
    permission_id: int = Form(...),
    db: Session = Depends(getdb)
):
    role_perm = db.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first()
    if not role_perm:
        raise HTTPException(status_code=404, detail="Permission not assigned to this role")

    db.delete(role_perm)
    db.commit()
    return {"detail": "Permission removed from role"}

# Get all permissions of a role
@router.get("/role/{role_id}")
def get_permissions_by_role(role_id: int, db: Session = Depends(getdb)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    perms = (
        db.query(Permission)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .filter(RolePermission.role_id == role_id)
        .all()
    )
    return perms

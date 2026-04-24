from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.crud import crud_users
from app.schemas import user_schemas
from uuid import UUID

router = APIRouter(
    prefix ="/users",
    tags = ['Users']
)



@router.post("/", response_model=user_schemas.UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = crud_users.create_user(user, db)

    return {
        "message" : "User successfully created",
        "user": new_user
    }




@router.get("/", response_model=user_schemas.UsersResponse)
def get_users(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    
    users_data = crud_users.get_all_users(db)

    return {
        "users" : users_data
    }




@router.get("/{id}", response_model=user_schemas.Userout)
def get_user(id: UUID, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    user = crud_users.get_user(id, db)

    return user




@router.put("/{id}", response_model=user_schemas.UserCreateResponse)
def update_user(id: UUID, user: user_schemas.UserCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    
    updated_user = crud_users.update_user(id, user, db)


    return {
        "message" : "user updated successfully",
        "user" : updated_user
    }




@router.delete("/{id}")
def delete_user(id: UUID, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    return crud_users.delete_user(id, db)



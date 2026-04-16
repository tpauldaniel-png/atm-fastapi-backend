from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, oauth2
from app.database import get_db
from app.schemas import atm_schemas
from app.crud import crud_atms

router = APIRouter(
    prefix = "/atms",
    tags = ["ATMS"]
)

@router.post("/", response_model=atm_schemas.CreateATMResponse, status_code=status.HTTP_201_CREATED)
def create_atm(atm: atm_schemas.CreateATM, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    
    new_atm = crud_atms.create_atm(atm, db)

    return {
        "message" : "atm successfully created",
        "atm" : new_atm
    }




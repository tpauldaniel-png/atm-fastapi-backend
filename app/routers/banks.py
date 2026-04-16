from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.crud import crud_banks
from app.schemas import bank_schemas


router = APIRouter(
    prefix = "/banks",
    tags = ["Banks"]
)


@router.post("/", response_model=bank_schemas.BankCreateResponse, status_code=status.HTTP_201_CREATED)
def create_bank(bank: bank_schemas.CreateBank, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
   
   new_bank =crud_banks.create_bank(bank, db)

   return {
      "message" : "bank successfully created",
      "bank" : new_bank
   }


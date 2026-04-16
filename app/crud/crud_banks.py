from app import models
from fastapi import HTTPException, status, Response


def create_bank(bank_data, db):
    try:

        new_bank = models.Bank(**bank_data.model_dump())
        db.add(new_bank)
        db.commit()
        db.refresh(new_bank)

        return new_bank

    except Exception:
        db.rollback()
        raise 


from app import models

def create_atm(atm_data, db):

    try:
        new_atm = models.ATM(**atm_data.model_dump())
        db.add(new_atm)
        db.commit()
        db.refresh(new_atm)

        return new_atm
    
    except Exception:
        db.rollback()
        raise


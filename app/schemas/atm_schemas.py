from pydantic import BaseModel

class CreateATM(BaseModel):
    location: str
    bank_id : int

class ATMout(BaseModel):
    atm_id : int
    location: str
    bank_id: int

    class Config:
        from_attributes = True

class CreateATMResponse(BaseModel):
    message : str
    atm : ATMout


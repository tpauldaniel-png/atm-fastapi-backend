from pydantic import BaseModel


class CreateBank(BaseModel):
    bank_name : str
    city : str
    state : str
    pincode : str

class BankOut(BaseModel):
    bank_id : int
    bank_name : str
    city : str
    state : str
    pincode : str

    class Config:
        from_attributes = True



class BankCreateResponse(BaseModel):
    message : str
    bank : BankOut

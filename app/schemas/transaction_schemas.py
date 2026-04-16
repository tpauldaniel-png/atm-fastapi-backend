from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TransactionOut(BaseModel):
    transaction_id : UUID
    transaction_type : str
    transaction_created_at : datetime
    amount : int
    account_id : UUID
    atm_id : int
    
    class Config:
        from_attributes = True


class TransactionActionResponse(BaseModel):
    message : str
    transaction : TransactionOut



class TransactionsResponse(BaseModel):
    transaction_history : list[TransactionOut]

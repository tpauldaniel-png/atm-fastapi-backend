from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class CreateAccount(BaseModel):
    user_id : UUID
    bank_id : int
    account_type : str


class AccountOut(BaseModel):
    account_id : UUID
    account_no : str
    account_type : str
    balance : Decimal
    user_id : UUID
    bank_id : int

    class Config:
        from_attributes = True

class AccountCreateResponse(BaseModel):
    message : str
    account : AccountOut


class AccountsResponse(BaseModel):
    accounts_data : list[AccountOut]


class CreateDeposit(BaseModel):
    amount_to_deposit : Decimal
    atm_id : int


class CreateWithdraw(BaseModel):
    amount_to_withdraw : Decimal
    atm_id : int

class BalanceResponse(BaseModel):
    balance : Decimal
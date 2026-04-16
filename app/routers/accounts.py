from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.schemas import account_schemas, transaction_schemas
from app.crud import crud_accounts
from uuid import UUID
from decimal import Decimal


router = APIRouter(
    prefix = "/accounts",
    tags = ["Accounts"]
)



@router.post("/",response_model=account_schemas.AccountCreateResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: account_schemas.CreateAccount, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    new_account = crud_accounts.create_account(account, db)

    return {
        "message" : "Account successfully created",
        "account" : new_account
    }



@router.get("/", response_model= account_schemas.AccountsResponse)
def get_accounts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    accounts = crud_accounts.get_accounts(db)

    return {
       "accounts_data" : accounts
    }



@router.get("/{id}", response_model = account_schemas.AccountOut)
def get_account(id: UUID, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    account = crud_accounts.get_account(id, db)

    return account



@router.post("/{account_no}/deposit", response_model = transaction_schemas.TransactionActionResponse)
def deposit(account_no: str, deposit_data : account_schemas.CreateDeposit, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    deposit_transaction = crud_accounts.deposit(account_no, deposit_data, db)

    return {
        "message" : "Deposit action successfull",
        "transaction" : deposit_transaction
    }



@router.post("/{account_no}/withdraw", response_model = transaction_schemas.TransactionActionResponse)
def withdraw(account_no: str, withdraw_data : account_schemas.CreateWithdraw, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):


    withdraw_transaction = crud_accounts.withdraw(account_no, withdraw_data, db)

    return {
        "message" : "Withdraw action successfull",
        "transaction" : withdraw_transaction
    }



@router.get("/{account_no}/balance", response_model = account_schemas.BalanceResponse)
def check_balance(account_no: str, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    balance = crud_accounts.check_balance(account_no, db)

    return {
        "balance" : balance
    }
        

@router.get("/{account_no}/transaction", response_model = transaction_schemas.TransactionsResponse)
def show_transactions(account_no: str, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    transactions = crud_accounts.show_transactions(account_no, db)

    return {
        "transaction_history" : transactions
    }


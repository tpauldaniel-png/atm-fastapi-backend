from app import models
from fastapi import HTTPException, status, Response


def create_account(account_data, db):
    
    try:
        new_account = models.Account(**account_data.model_dump())
        db.add(new_account)
        db.flush()

        atm = db.query(models.ATM).filter(models.ATM.bank_id == new_account.bank_id).first()

        if atm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No atm found for this bank")


        new_transaction = models.Transaction(
            transaction_type = "OPENING ACCOUNT",
            amount = new_account.balance,
            account_id = new_account.account_id,
            atm_id = atm.atm_id
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_account)

        return new_account


    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )




def get_accounts(db):

    try:

        accounts = db.query(models.Account).all()

        return accounts

    except Exception:
        raise 


def get_account(account_id, db):

    account = db.query(models.Account).filter(models.Account.account_id == account_id).first()

    if account is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"account with id:{account_id} not found ")


    return account





def deposit(account_no, deposit_data, db):

    try:
        if deposit_data.amount_to_deposit <= 0:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail ="Invalid amount")

        account = db.query(models.Account).filter(models.Account.account_no == account_no).first()

        if account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Account with account no : {account_no} not found")


        atm = db.query(models.ATM).filter(models.ATM.atm_id == deposit_data.atm_id).first()

        if atm is None:
             raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid atm id")


        if atm.bank_id != account.bank_id:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Atm not found for this bank")


        account.balance += deposit_data.amount_to_deposit

        new_transaction = models.Transaction(
            transaction_type = "DEPOSIT",
            amount = deposit_data.amount_to_deposit,
            account_id = account.account_id,
            atm_id = deposit_data.atm_id
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return new_transaction
    
    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
       



def withdraw(account_no, withdraw_data, db):

    try:
        if withdraw_data.amount_to_withdraw <= 0:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid amount")
        
        account = db.query(models.Account).filter(models.Account.account_no == account_no).first()

        if account is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Account with account no : {account_no} not found" )
        
        atm = db.query(models.ATM).filter(models.ATM.atm_id == withdraw_data.atm_id).first()

        if atm is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid atm id")
        
        if atm.bank_id != account.bank_id:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "atm not found for this bank")
        
        if account.balance < withdraw_data.amount_to_withdraw:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Insufficient funds")
        

        account.balance -= withdraw_data.amount_to_withdraw

        new_transaction = models.Transaction(
            transaction_type = "WITHDRAW",
            amount = withdraw_data.amount_to_withdraw,
            account_id = account.account_id,
            atm_id = withdraw_data.atm_id
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return new_transaction
    
    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    




def check_balance(account_no, db):

    try:
        account = db.query(models.Account).filter(models.Account.account_no == account_no).first()

        if account is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Account with account no : {account_no} not found" )
        

        return account.balance
    
    except Exception:
        raise 




def show_transactions(account_no, db):

    try:
        account = db.query(models.Account).filter(models.Account.account_no == account_no).first()

        if account is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Account with account no : {account_no} not found" )


        transactions = db.query(models.Transaction).filter(models.Transaction.account_id == account.account_id).order_by(models.Transaction.transaction_created_at.desc()).all()

        return transactions
    
    except Exception:
        raise 


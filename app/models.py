from .database import Base
from sqlalchemy import text, String, Date, CheckConstraint, Text, Integer, Sequence, Numeric, ForeignKey, DateTime 
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal



acc_seq = Sequence("acc_seq", start=100000, metadata=Base.metadata)




class User(Base):
    __tablename__= "users"

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    phone_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    corresponding_address: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    accounts: Mapped[list["Account"]] = relationship(back_populates="user")


    __table_args__= (
        CheckConstraint("date_of_birth <= CURRENT_DATE - INTERVAL '18 years'", name="check_age_18"),
    )






class Bank(Base):
    __tablename__= "banks"


    bank_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bank_name: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)


    accounts: Mapped[list["Account"]] = relationship(back_populates="bank")
    atms: Mapped[list["ATM"]] = relationship(back_populates="bank")




class Account(Base):
    __tablename__= "accounts"


    account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    account_no: Mapped[str] = mapped_column(String, unique=True, nullable=False, server_default=text("'ACC' || nextval('acc_seq')"))
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12,2), default=0, nullable=False)

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.bank_id"))


    user: Mapped["User"] = relationship(back_populates="accounts")
    bank: Mapped["Bank"] = relationship(back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")



    __table_args__=(
        CheckConstraint("balance >= 0", name="check_negative_balance"),
    )



class ATM(Base):
    __tablename__="atms"

    atm_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)

    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.bank_id"))


    bank: Mapped["Bank"] = relationship(back_populates="atms")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="atm")




class Transaction(Base):
    __tablename__="transactions"

    transaction_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    transaction_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False, default=0)

    account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("accounts.account_id"))
    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.atm_id"))

    
    account: Mapped["Account"] = relationship(back_populates="transactions")
    atm: Mapped["ATM"] = relationship(back_populates="transactions")



    __table_args__=(
        CheckConstraint("amount >= 0", name="check_negative_amount"),
    )





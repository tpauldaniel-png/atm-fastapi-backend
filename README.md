# ATM Backend Simulation API

A RESTful ATM backend simulation project built using FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, and Argon2 password hashing.

## Features

- User Registration and Login
- JWT Authentication and Authorization
- Secure Password Hashing with Argon2
- Bank and ATM Management
- Account Creation
- Deposit / Withdrawal Operations
- Balance Inquiry
- Transaction History Tracking

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT / OAuth2
- pwdlib + Argon2

## Installation

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```
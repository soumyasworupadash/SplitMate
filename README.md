# SplitMate

## Overview

SplitMate is a full-stack expense-sharing application inspired by Splitwise. It allows users to create groups, add members, record shared expenses, split expenses equally or by exact amounts, track balances, settle debts, and view activity logs. The application is built using FastAPI for the backend, React + Vite for the frontend, PostgreSQL as the database, and JWT-based authentication.

---

# Features

### User Authentication
- User Registration
- User Login
- JWT Authentication
- Protected API Routes

### Group Management
- Create Group
- Delete Group
- Add Members
- Remove Members (only when balance is zero)

### Expense Management
- Add Expense
- Edit Expense
- Delete Expense
- Equal Split
- Exact Split

### Balance Management
- Group Balances
- Simplified Balances
- Overall Balance
- Dashboard Summary

### Settlements
- Record Settlements
- Settlement History

### Activity Logs
- Member Added
- Member Removed
- Expense Added
- Expense Updated
- Expense Deleted
- Settlement Recorded

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT Authentication
- Pydantic

## Frontend

- React
- Vite
- Material UI
- Axios
- React Router

---

# Project Structure

```
SplitMate
│
├── Backend
│   ├── app
│   ├── alembic
│   ├── seed.py
│   ├── requirements.txt
│   └── .env.example
│
├── Frontend
│   ├── src
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SplitMate.git

cd SplitMate
```

---

# Backend Setup

```bash
cd Backend

python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.example`.

Run migrations.

Start server

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# Frontend Setup

```bash
cd Frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# Environment Variables

Create a `.env` file inside Backend.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/splitmate

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Seed Script

To populate the database with sample data:

```bash
python seed.py
```

This creates:

- Two test users
- One shared group
- Two expenses
- Expense splits

Default users:

```
soumya@gmail.com

password123
```

```
kalyani@gmail.com

password123
```

---

# Database Design

## Tables

### User
- id
- email
- password

### Group
- id
- name
- owner_id

### GroupMember
- id
- group_id
- user_id

### Expense
- id
- description
- amount
- paid_by
- group_id

### ExpenseSplit
- id
- expense_id
- user_id
- amount

### Settlement
- id
- payer_id
- receiver_id
- amount

### ActivityLog
- id
- group_id
- user_id
- action
- description
- created_at

---

# Entity Relationships

```
User
│
├── owns
│      │
│      ▼
│    Group
│      │
│      ▼
│  GroupMember
│      │
│      ▼
│    Expense
│      │
│      ▼
│ ExpenseSplit
│
└────────► Settlement

Group
└────────► ActivityLog
```

---

# Money Handling and Rounding

The application stores monetary values as floating-point numbers in PostgreSQL.

Balances are rounded to two decimal places before being displayed.

Equal splits divide the total amount equally among members.

Exact splits require the user to manually enter each member's share.

For production-scale financial systems, using integer paise/cents or Decimal would provide better precision than floating-point values.

---

# Authentication

JWT-based authentication is used.

After login:

- Access Token is generated.
- Token is stored in browser localStorage.
- Every protected request sends:

```
Authorization: Bearer <token>
```

---

# Refresh Token Flow

The current implementation uses JWT Access Tokens only.

Refresh Token functionality has not yet been implemented.

When the access token expires, the user must log in again.

Future versions will support Refresh Tokens for automatic session renewal.

---

# WebSocket Setup

The current implementation does not use WebSockets.

Updates are reflected through API requests after CRUD operations.

Real-time broadcasting of expenses, settlements, balances, and activity logs is planned as a future enhancement using FastAPI WebSockets.

---

# Challenges Faced

Some major challenges encountered during development included:

- Designing the expense splitting algorithm.
- Calculating simplified balances correctly.
- Preventing member removal when outstanding balances exist.
- Handling settlements without corrupting balances.
- Maintaining database relationships.
- Synchronizing frontend updates after CRUD operations.

---

# Known Issues

- Refresh Token authentication is not implemented.
- Real-time WebSocket updates are not implemented.
- Floating-point values are used for monetary amounts.
- Group owners are displayed using IDs in some views instead of names.

---

# Future Improvements

- Refresh Token authentication.
- FastAPI WebSocket integration.
---

# AI Usage

AI tools were used during development for:

- Understanding FastAPI concepts.
- Learning SQLAlchemy relationships.
- Improving React component structure.
- Generating boilerplate code.
- Understanding JWT authentication.

All generated code was reviewed, tested, modified, and integrated manually.

---

# Author

Soumya Sworupa Dash

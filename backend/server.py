from fastapi import FastAPI, HTTPException, Query
from datetime import date, datetime
import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class Expense_Date(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses


@app.get("/expenses_month/", response_model=List[Expense_Date])
def get_expenses_month(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12)
):
    expenses_month = db_helper.fetch_expenses_for_month(year, month)

    if not expenses_month:
        raise HTTPException(status_code=404, detail="No expenses found for the given month and year.")

    return expenses_month

@app.get("/recent_expenses/{limit}", response_model=List[Expense_Date])
def get_recent_expenses(limit: int):
    recent_expenses = db_helper.fetch_recent_expenses(limit)
    if recent_expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense of this month from the database.")

    return recent_expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown


@app.get("/monthly_summary/")
def get_analytics():
    monthly_summary = db_helper.fetch_monthly_expense_summary()
    if monthly_summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expense summary from the database.")

    return monthly_summary

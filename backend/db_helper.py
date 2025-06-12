import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import calendar
from datetime import date
from password import pwd


logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=pwd,
            database="expense_manager"
        )
        cursor = connection.cursor(dictionary=True)
        yield cursor
        if commit:
            connection.commit()
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def fetch_expenses_for_month(year: int, month: int):
    logger.info(f"fetch_expenses_for_month called for {year}-{month:02d}")
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM expenses WHERE expense_date BETWEEN %s AND %s",
            (first_day, last_day)
        )
        expenses_month = cursor.fetchall()
        return expenses_month

def fetch_recent_expenses(limit):
    logger.info(f"fetch_recent_expenses called with limit={limit}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC LIMIT %s", (limit,))
        recent_expenses = cursor.fetchall()
        return recent_expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


def fetch_monthly_expense_summary():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT month(expense_date) as expense_month, 
               monthname(expense_date) as month_name,
               sum(amount) as total FROM expenses
               GROUP BY expense_month, month_name;
            '''
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2025-06-09")
    # print(expenses)
    # # delete_expenses_for_date("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for record in summary:
    #     print(record)
    # print(fetch_monthly_expense_summary())
    print(len(fetch_expenses_for_month(2025,6)))

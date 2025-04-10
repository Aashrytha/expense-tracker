from app import db
from app.models import Category
from datetime import datetime
from sqlalchemy import func
from app import db
from app.models import Expense

def get_default_categories():
    """Get or create default expense categories."""
    default_categories = [
        {"name": "Food", "description": "Groceries, restaurants, etc."},
        {"name": "Housing", "description": "Rent, mortgage, utilities, etc."},
        {"name": "Transportation", "description": "Public transport, gas, car maintenance, etc."},
        {"name": "Entertainment", "description": "Movies, concerts, subscriptions, etc."},
        {"name": "Shopping", "description": "Clothing, electronics, etc."},
        {"name": "Health", "description": "Medical expenses, gym membership, etc."},
        {"name": "Education", "description": "Tuition, books, courses, etc."},
        {"name": "Personal", "description": "Personal care, haircuts, etc."},
        {"name": "Travel", "description": "Flights, hotels, vacation expenses, etc."},
        {"name": "Other", "description": "Miscellaneous expenses"}
    ]
    
    categories = []
    for cat_data in default_categories:
        category = Category.query.filter_by(name=cat_data["name"]).first()
        if not category:
            category = Category(name=cat_data["name"], description=cat_data["description"])
            db.session.add(category)
        categories.append(category)
    
    db.session.commit()
    return categories


def get_monthly_spending(user_id, month, year):
    """Get total spending for a user in a specific month and year."""
    start_date = datetime(year, month, 1)
    
    # Calculate end date (first day of next month)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Query total expenses for the month
    total = db.session.query(func.sum(Expense.amount)) \
        .filter(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date < end_date
        ).scalar() or 0
    
    return total

def get_category_spending(user_id, category_id, month, year):
    """Get total spending for a user in a specific category, month, and year."""
    start_date = datetime(year, month, 1)
    
    # Calculate end date (first day of next month)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Query total expenses for the category in the month
    total = db.session.query(func.sum(Expense.amount)) \
        .filter(
            Expense.user_id == user_id,
            Expense.category_id == category_id,
            Expense.date >= start_date,
            Expense.date < end_date
        ).scalar() or 0
    
    return total
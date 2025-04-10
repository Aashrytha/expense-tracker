from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.models import Expense, Category
from app.forms import ExpenseForm
from calendar import monthrange
from app.models import Budget
from app.forms import BudgetForm
from app.utils import get_category_spending, get_monthly_spending
from calendar import monthrange
from app.forms import ReportForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    form = ExpenseForm()
    # Get all categories for the dropdown
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            description=form.description.data,
            date=form.date.data,
            user_id=current_user.id,
            category_id=form.category_id.data
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!')
        return redirect(url_for('main.expenses'))
    
    # Get all expenses for the current user
    expenses = Expense.query.filter_by(user_id=current_user.id) \
        .order_by(Expense.date.desc()).all()
    
    return render_template('expenses.html', title='Expenses', form=form, expenses=expenses)

@main.route('/expenses/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if the expense belongs to the current user
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense')
        return redirect(url_for('main.expenses'))
    
    form = ExpenseForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.date = form.date.data
        expense.category_id = form.category_id.data
        
        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('main.expenses'))
    
    elif request.method == 'GET':
        # Pre-populate form with existing expense data
        form.amount.data = expense.amount
        form.description.data = expense.description
        form.date.data = expense.date
        form.category_id.data = expense.category_id
    
    return render_template('edit_expense.html', title='Edit Expense', form=form, expense=expense)

@main.route('/expenses/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense')
        return redirect(url_for('main.expenses'))
    
    db.session.delete(expense)
    db.session.commit()
    
    flash('Expense deleted successfully!')
    return redirect(url_for('main.expenses'))


@main.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    form = BudgetForm()
    # Get all categories for the dropdown
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # Check if a budget for this category, month, and year already exists
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category_id=form.category_id.data,
            month=form.month.data,
            year=form.year.data
        ).first()
        
        if existing_budget:
            existing_budget.amount = form.amount.data
            flash('Budget updated successfully!')
        else:
            budget = Budget(
                amount=form.amount.data,
                month=form.month.data,
                year=form.year.data,
                user_id=current_user.id,
                category_id=form.category_id.data
            )
            db.session.add(budget)
            flash('Budget added successfully!')
        
        db.session.commit()
        return redirect(url_for('main.budgets'))
    
    # Get current month and year for default form values
    today = datetime.utcnow()
    form.month.data = form.month.data or today.month
    form.year.data = form.year.data or today.year
    
    # Get all budgets for the selected month and year
    month = request.args.get('month', today.month, type=int)
    year = request.args.get('year', today.year, type=int)
    
    budgets = Budget.query.filter_by(
        user_id=current_user.id,
        month=month,
        year=year
    ).all()
    
    # Get spending for each category with a budget
    budget_data = []
    for budget in budgets:
        spent = get_category_spending(current_user.id, budget.category_id, month, year)
        remaining = budget.amount - spent
        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage
        })
    
    return render_template('budgets.html', 
                          title='Budgets', 
                          form=form, 
                          budget_data=budget_data,
                          month=month,
                          year=year)

@main.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow()
    current_month = today.month
    current_year = today.year
    
    # Get expense summary for current month
    monthly_spending = get_monthly_spending(current_user.id, current_month, current_year)
    
    # Get budget comparison for each category
    categories = Category.query.all()
    category_data = []
    
    for category in categories:
        budget = Budget.query.filter_by(
            user_id=current_user.id,
            category_id=category.id,
            month=current_month,
            year=current_year
        ).first()
        
        spending = get_category_spending(current_user.id, category.id, current_month, current_year)
        
        if budget:
            budget_amount = budget.amount
            percentage = (spending / budget_amount * 100) if budget_amount > 0 else 0
        else:
            budget_amount = 0
            percentage = 0
        
        category_data.append({
            'category': category.name,
            'budget': budget_amount,
            'spent': spending,
            'percentage': percentage
        })
    
    # Get recent expenses
    recent_expenses = Expense.query.filter_by(user_id=current_user.id) \
        .order_by(Expense.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          title='Dashboard',
                          monthly_spending=monthly_spending,
                          category_data=category_data,
                          recent_expenses=recent_expenses)

@main.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    form = ReportForm()
    
    # Set up year choices (from 2020 to current year + 5)
    current_year = datetime.utcnow().year
    form.year.choices = [(y, str(y)) for y in range(2020, current_year + 6)]
    
    # Get current month and year for default values
    today = datetime.utcnow()
    month = request.args.get('month', today.month, type=int)
    year = request.args.get('year', today.year, type=int)
    
    # Set default form values if not already set
    if not form.month.data:
        form.month.data = month
    if not form.year.data:
        form.year.data = year
    
    # Get total spending for the month
    monthly_spending = get_monthly_spending(current_user.id, month, year)
    
    # Get category-wise spending
    categories = Category.query.all()
    category_spending = []
    
    for category in categories:
        spent = get_category_spending(current_user.id, category.id, month, year)
        if spent > 0:  # Only include categories with spending
            budget = Budget.query.filter_by(
                user_id=current_user.id,
                category_id=category.id,
                month=month,
                year=year
            ).first()
            
            budget_amount = budget.amount if budget else 0
            
            category_spending.append({
                'category': category.name,
                'spent': spent,
                'budget': budget_amount,
                'percentage': round((spent / monthly_spending * 100), 1) if monthly_spending > 0 else 0
            })
    
    # Sort categories by spending (highest first)
    category_spending.sort(key=lambda x: x['spent'], reverse=True)
    
    # Get daily spending for the month
    days_in_month = monthrange(year, month)[1]
    daily_spending = []
    
    for day in range(1, days_in_month + 1):
        date = datetime(year, month, day)
        expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            Expense.date >= datetime(year, month, day, 0, 0, 0),
            Expense.date < datetime(year, month, day, 23, 59, 59)
        ).all()
        
        daily_amount = sum(e.amount for e in expenses)
        
        daily_spending.append({
            'day': day,
            'amount': daily_amount,
            'date': date.strftime('%Y-%m-%d')
        })
    
    # Get month-over-month data (previous 6 months)
    months_data = []
    for i in range(6):
        # Calculate month and year
        report_month = month - i
        report_year = year
        while report_month <= 0:
            report_month += 12
            report_year -= 1
        
        # Get spending for this month
        month_spending = get_monthly_spending(current_user.id, report_month, report_year)
        
        # Add to list
        months_data.append({
            'month': report_month,
            'year': report_year,
            'month_name': form.month.choices[report_month-1][1],
            'spending': month_spending
        })
    
    # Reverse so it's chronological order
    months_data.reverse()
    
    return render_template('reports.html',
                          title='Reports',
                          form=form,
                          month=month,
                          year=year,
                          month_name=form.month.choices[month-1][1],
                          monthly_spending=monthly_spending,
                          category_spending=category_spending,
                          daily_spending=daily_spending,
                          months_data=months_data)
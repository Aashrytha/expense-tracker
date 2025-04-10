# Expense Tracker Application

A full-featured expense tracking application built with Flask that helps users manage their finances, set budgets, and analyze spending patterns.

## Features

- **User Authentication**
  - Secure registration and login
  - Password hashing for security

- **Expense Management**
  - Add, edit, and delete expenses
  - Categorize expenses
  - Track expense date and description

- **Budget Management**
  - Set monthly budgets for each category
  - Different budgets for different months
  - Visual indicators for budget status

- **Detailed Reports**
  - Monthly spending summaries
  - Category-wise spending analysis
  - Day-by-day expense tracking
  - Month-over-month spending trends
  - Visual charts and graphs

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript, Chart.js
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Deployment**: Docker-ready

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/Aashrytha/expense-tracker.git
   cd expense-tracker
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   # Create a .env file with the following variables
   SECRET_KEY=your_secret_key
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///expense_tracker.db
   ```

5. Initialize the database
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application
   ```bash
   flask run
   ```

7. Access the application at http://localhost:5000

## Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build
```

## Usage

1. Register a new account
2. Add expense categories
3. Set monthly budgets for categories
4. Start tracking expenses
5. View reports to analyze spending patterns

Thank You!

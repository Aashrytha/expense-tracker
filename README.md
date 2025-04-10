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
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker

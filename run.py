from app import create_app, db
from app.models import User, Category, Expense, Budget, Group, Alert
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Category': Category, 
        'Expense': Expense, 
        'Budget': Budget, 
        'Group': Group, 
        'Alert': Alert
    }

@app.before_first_request
def initialize_app():
    from app.utils import get_default_categories
    # Create default categories if they don't exist
    get_default_categories()

if __name__ == '__main__':
    app.run(debug=True)
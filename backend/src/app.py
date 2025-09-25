from flask import Flask
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db


app = Flask(__name__)
setup_db(app)

CORS(app, resources={r"/*": {"origins": [
    "https://accountableweb.netlify.app",
    "http://localhost:3000"
]}})

with app.app_context():
    db_drop_and_create_all()
    print("Database initialized.")

# Register blueprints
from routes.groups import group_endpoints
from routes.tasks import tasks_endpoints
from routes.user_groups import user_groups_endpoints
from routes.users import users_endpoints

app.register_blueprint(group_endpoints)
app.register_blueprint(tasks_endpoints)
app.register_blueprint(user_groups_endpoints)
app.register_blueprint(users_endpoints)

# TEST ROUTE
@app.route('/hello')
def hello():
    return "hello world"
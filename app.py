import sys
from flask import Flask, render_template
from flask_login import LoginManager
from blueprints.home import home_page
from blueprints.users import users
from blueprints.recipe import recipes
from blueprints.errors import errors
from config import Config
from models import db, User

app = Flask(__name__)
login = LoginManager(app)
app.secret_key = 'much secret' # for some reason flask_login needs a secret key?
app.config.from_object(Config)
db.init_app(app)

@login.user_loader
def load_user(id): # setting users to sessions
    return User.query.get(int(id))

app.register_blueprint(home_page)
app.register_blueprint(users)
app.register_blueprint(recipes)
app.register_blueprint(errors)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

def main():
    if (len(sys.argv)==2):
        if sys.argv[1] == 'createdb':
            db.create_all()
            print("Created database.")
        elif sys.argv[1] == 'delusertable':
            User.__table__.drop(db.engine)

if __name__ == "__main__":
    with app.app_context():
        main()
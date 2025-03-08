from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('localapp.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
 
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(os.getenv('DATABASE_PW')).decode("utf-8")

        from . import models
        db.create_all()

        user_exists = User.query.filter_by(email=os.getenv('DATABASE_EMAIL')).first()
        if not user_exists:
            new_user = User(username=os.getenv('DATABASE_USER'), email=os.getenv('DATABASE_EMAIL'), password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            print("User created successfully!")
        else:
            print("User already exists. Skipping insert.")

    return app
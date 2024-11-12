from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from flask_migrate import Migrate
from flask_login import  LoginManager
from flask_ckeditor import  CKEditor
import  os

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'image_fold')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def create_app():

    app = Flask(__name__, template_folder="templates")
    app.config["SECRET_KEY"] = "reterthvfjhuj345"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///website.db"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    login_manager.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)

    from blueprints.main import main_bp
    from blueprints.introduce.route import introduce
    from blueprints.course.route import course
    from blueprints.library.route import library
    from blueprints.register.route import register


    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(introduce, url_prefix="/introduce")
    app.register_blueprint(course, url_prefix="/course")
    app.register_blueprint(library, url_prefix="/library")
    app.register_blueprint(register, url_prefix="/register")

    migrate = Migrate(app, db)

    return app

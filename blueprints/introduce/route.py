from flask import Blueprint, render_template
from blueprints.register.models import SchoolDisplay, StructureDisplay, ClassDisplay

introduce = Blueprint("introduce", __name__, template_folder="templates")


@introduce.route("/")
def index():
    schoolintroduce = SchoolDisplay.query.first()
    structures = StructureDisplay.query.all()
    classes = ClassDisplay.query.all()
    return render_template("introduce.html",schoolintroduce=schoolintroduce,
                           structures=structures,classes=classes)

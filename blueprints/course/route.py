from flask import Blueprint, render_template, request,flash,redirect,url_for,session
from flask_login import current_user
from blueprints.register.models import Course, UserData, ClassDisplay, CourseFrom,db
import  os
course = Blueprint("course", __name__, template_folder="templates")


@course.route("/", methods=["GET", "POST"])
def index():
    allclass = [item.class_name for item in ClassDisplay.query.all()]
    page = request.args.get("page", 1, type=int)
    posts = Course.query.filter_by(class_="全園活動").paginate(page=page, per_page=1, error_out=False)
    return render_template("course.html", posts=posts.items,
                           pagination=posts, current_page=posts.page, total_pages=posts.total, allclass=allclass)


@course.route("/<string:class_name>", methods=["GET", "POST"])
def class_page(class_name):
    allclass = [item.class_name for item in ClassDisplay.query.all()]
    page = request.args.get("page", 1, type=int)
    posts = Course.query.filter_by(class_=class_name).paginate(page=page, per_page=10, error_out=False)
    return render_template("individual.html", posts=posts.items,
                           pagination=posts, current_page=posts.page, total_pages=posts.pages, allclass=allclass)


@course.route("/delete/<string:post_id>", methods=["GET", "POST"])
def course_delete(post_id):
    post = Course.query.filter_by(id=post_id).first()
    if post:
        for picture_path in [post.picture_path1, post.picture_path2, post.picture_path3]:
            if picture_path and os.path.exists(picture_path):
                os.remove(picture_path)
        db.session.delete(post)
        db.session.commit()
        flash("刪除成功")
    return redirect(url_for("course.index"))

@course.route("/edit/<string:post_id>", methods=["GET", "POST"])
def course_edit(post_id):
    classname = ClassDisplay.query.all()
    post = Course.query.filter_by(id=post_id).first()
    courseform = CourseFrom(classname=classname)
    if courseform.validate_on_submit():
        post.class_ = courseform.class_.data
        post.title = courseform.title.data
        post.context = courseform.context.data
        post.picture_path1 = courseform.picture_path1.data
        post.picture_path2 = courseform.picture_path2.data
        post.picture_path3 = courseform.picture_path3.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for("course.index"))
    return render_template("course_edit.html",post=post,courseform=courseform)

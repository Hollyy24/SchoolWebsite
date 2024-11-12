from flask import Blueprint, render_template, session, url_for, redirect, flash, request, current_app
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from blueprints.register.models import User, UserLogin,UserData, db, SchoolIntroduce, SchoolDisplay, SchoolStructure, \
    StructureDisplay, ClassData, ClassDisplay, Course, CourseFrom, AddBook, Library
from blueprints.app import login_manager, ckeditor
from blueprints import app
from werkzeug.utils import secure_filename
import os,datetime

register = Blueprint("register", __name__, template_folder="templates")


def find_bookid():
    allbook = Library.query.all()
    id = 0
    for item in allbook:
        if item.id == id:
            id += 1
        else:
            return id
    return id


@register.before_app_request
def create_admin_user():
    if not UserData.query.filter_by(user_name="admin").first():
        admin = UserData(user_name="admin", user_password="admin", user_account="admin")
        db.session.add(admin)
        db.session.commit()
        print("預設管理者帳號已建立：admin / admin")


@login_manager.user_loader
def load_user(id):
    return db.session.get(UserData, int(id))


@register.route("/", methods=["POST", "GET"])
def index():
    userform = UserLogin()
    if userform.validate_on_submit():
        useraccount = userform.useraccount.data
        userpassword = userform.userpassword.data
        user = UserData.query.filter_by(user_account=useraccount).first()
        if user and user.user_password == userpassword:
            login_user(user)
            flash("成功登入")
            session["user"] = True
            return redirect(url_for("register.manager"))
        else:
            flash("輸入錯誤")
            print("fault")
            return redirect(url_for("register.index"))

    return render_template("register.html", userform=userform)


@register.route("/manager", methods=["GET", "POST"])
@login_required
def manager():
    userform = User()
    if userform.validate_on_submit():
        existing_user = UserData.query.filter_by(user_name=userform.username.data).first()
        if existing_user:
            flash("此使用者名稱已存在，請選擇其他名稱", "error")
        else:
            user = UserData(
                user_name=userform.username.data,
                user_password=userform.userpassword.data,
                user_account=userform.useraccount.data
            )
            try:
                db.session.add(user)
                db.session.commit()
                flash("使用者已成功新增", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"發生錯誤：{str(e)}", "error")
    users = UserData.query.all()
    return render_template("manager.html", userform=userform, users=users)


@register.route("/manager/introduce/1", methods=["GET", "POST"])
@login_required
def introduce_1():
    schooldisplay = SchoolDisplay.query.order_by(SchoolDisplay.id.desc()).first()
    if schooldisplay:
        schoolform = SchoolIntroduce(
            title=schooldisplay.title,
            content=schooldisplay.content
        )
    else:
        schoolform = SchoolIntroduce()
    if schoolform.validate_on_submit():
        title_data = schoolform.title.data
        content_data = schoolform.content.data
        schooldisplay = SchoolDisplay(
            title=title_data,
            content=content_data
        )
        db.session.add(schooldisplay)
        db.session.commit()
        flash("修改成功！")
        return redirect(url_for("register.introduce_1"))
    return render_template("school_introduce/introduce_1.html", schoolform=schoolform, schooldisplay=schooldisplay)


@register.route("/manager/introduce/2", methods=["GET", "POST"])
@login_required
def introduce_2():
    teachername = UserData().query.all()
    structuredisplay = StructureDisplay.query.all()
    schoolstructure = SchoolStructure(teachername=teachername)

    if schoolstructure.validate_on_submit():
        structure = StructureDisplay(
            team_name=schoolstructure.team_name.data,
            teacher_name=schoolstructure.teacher_name.data)
        db.session.add(structure)
        db.session.commit()
        flash("新增成功！")
        return redirect(url_for("register.introduce_2"))
    return render_template("school_introduce/introduce_2.html", schoolstructure=schoolstructure,
                           structuredisplay=structuredisplay, total=len(structuredisplay))


@register.route("/manager/introduce/3", methods=["GET", "POST"])
@login_required
def introduce_3():
    teachername = UserData().query.all()
    classdata = ClassData(teachername=teachername)
    classdisplay = ClassDisplay.query.all()
    if classdata.validate_on_submit():
        classes = ClassDisplay(class_name=classdata.class_name.data,
                               class_teacher1=classdata.teacher_name1.data,
                               class_teacher2=classdata.teacher_name2.data)
        db.session.add(classes)
        db.session.commit()
        return redirect(url_for("register.introduce_3"))
    return render_template("school_introduce/introduce_3.html", classdata=classdata, classdisplay=classdisplay)


@register.route("/manager/librarybook_add", methods=["GET", "POST"])
@login_required
def librarybook_add():
    id = find_bookid()
    books = Library.query.all()
    addbook = AddBook(id=find_bookid())
    if addbook.validate_on_submit():
        book = Library(id=addbook.id.data, book_title=addbook.book_title.data,
                       author=addbook.author.data, ISBN_number=addbook.ISBN_number.data)
        db.session.add(book)
        db.session.commit()
        flash("新增成功！")
        return redirect(url_for("register.librarybook_add"))
    return render_template("library_add/library_add.html", addbook=addbook, books=books)


@register.route("/manager/course_add", methods=["GET", "POST"])
@login_required
def course_add():
    classname = ClassDisplay().query.all()
    courseform = CourseFrom(classname=classname)
    if courseform.validate_on_submit():
        picture_paths = []
        for field in [courseform.picture_path1, courseform.picture_path2, courseform.picture_path3]:
            if field.data:
                filename = secure_filename(field.data.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                field.data.save(filepath)
                picture_paths.append(f'image_fold/{filename}')
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        course = Course(class_=courseform.class_.data,
                        title=courseform.title.data,
                        posttime =time,
                        context=courseform.context.data,
                        picture_path1=picture_paths[0] if len(picture_paths) > 0 else None,
                        picture_path2=picture_paths[1] if len(picture_paths) > 1 else None,
                        picture_path3=picture_paths[2] if len(picture_paths) > 2 else None
                        )
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("register.course_add"))
    else:
        print("None")
    return render_template("course_add/course_add.html", courseform=courseform)


@register.route("/manager/account_delete/<string:user_id>", methods=["GET", "POST"])
@login_required
def account_delete(user_id):
    user = UserData.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("已刪除成功")
    return redirect(url_for("register.manager"))


@register.route("/manager/account_edit/<string:user_id>", methods=["GET", "POST"])
@login_required
def account_edit(user_id):
    user = UserData.query.filter_by(id=user_id).first()
    userform = User(username=user.user_name, useraccount=user.user_account,
                    userpassword=user.user_password)
    if userform.validate_on_submit():
        user.user_name = userform.username.data
        user.user_account = userform.useraccount.data
        user.user_password = userform.userpassword.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for("register.manager"))
    return render_template("edit/account_edit.html", userform=userform)


@register.route("/manager/team_delete/<string:teamname>", methods=["GET", "POST"])
@login_required
def team_delete(teamname):
    team = StructureDisplay.query.filter_by(team_name=teamname).first()
    if team:
        db.session.delete(team)
        db.session.commit()
        flash("已刪除成功")
    return redirect(url_for("register.introduce_2"))


@register.route("/manager/team_edit/<string:teamname>", methods=["GET", "POST"])
@login_required
def team_edit(teamname):
    teachername = UserData.query.all()
    team = StructureDisplay.query.filter_by(team_name=teamname).first()
    teamform = SchoolStructure(teachername=teachername)
    if teamform.validate_on_submit():
        team.team_name = teamform.team_name.data
        team.teacher_name = teamform.teacher_name.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for("register.introduce_2"))
    return render_template("edit/team_edit.html", teamform=teamform, team=team)


@register.route("/manager/class_delete/<string:class_name>", methods=["GET", "POST"])
@login_required
def class_delete(class_name):
    class_ = ClassDisplay.query.filter_by(class_name=class_name).first()
    if class_:
        db.session.delete(class_)
        db.session.commit()
        flash("已刪除成功")
    return redirect(url_for("register.introduce_3"))


@register.route("/manager/class_edit/<string:class_name>", methods=["GET", "POST"])
@login_required
def class_edit(class_name):
    teachername = UserData.query.all()
    class_ = ClassDisplay.query.filter_by(class_name=class_name).first()
    classform = ClassData(teachername=teachername)
    if classform.validate_on_submit():
        class_.class_name = classform.class_name.data
        class_.class_teacher1 = classform.teacher_name1.data
        class_.class_teacher2 = classform.teacher_name1.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for("register.introduce_3"))
    return render_template("edit/class_edit.html", classform = classform, class_ = class_)


@register.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("user", None)
    return redirect(url_for("main.index"))
